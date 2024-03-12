import json
import os
import datetime
import shutil
import time
import pytest
from _pytest.terminal import TerminalReporter
from colorama import Fore, Back, Style
from enum import Enum
from typing import List
from model.model import DIRECTORIES
from model.model import parse_spec_file, parse_test_file
from model.model import CodeAbilityTestSuite, CodeAbilitySpecification
from model.model import StatusEnum, ResultEnum
from model.model import CodeAbilityReport, CodeAbilityReportMain, CodeAbilityReportSub, CodeAbilityReportSummary
from .helper import get_property_as_list

class Solution(str, Enum):
    student = "student"
    reference = "reference"

metadata_key = pytest.StashKey[dict]()
report_key = pytest.StashKey[dict]()

def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--specification",
        default="",
        help="specification yaml input file",
    )
    parser.addoption(
        "--test",
        default="test.yaml",
        help="test yaml input file",
    )
    parser.addoption(
        "--indent",
        default=2,
        help="json report output indentation in spaces",
    )
    parser.addoption(
        "--catverbosity",
        default="",
        help="catester-verbosity level",
    )
    parser.addoption(
        "--pytestflags",
        default="",
        help="pytestflags",
    )

def pytest_metadata(metadata, config):
    """metadata contains information about the environment\n
    see: https://pypi.org/project/pytest-metadata/
    """
    config.stash[metadata_key] = metadata

def pytest_configure(config: pytest.Config) -> None:
    """Testcases are parametrized here\n
    Generates a list of Tuples with the indices of the given testcases\n
    for example: [(0, 0), (0, 1), (0, 2), (1, 0), ...]\n
    During test phase the function using the fixture "testcases"\n
    will be called with each of the generated tuples (seperately)\n
    The report is initialized here as well
    """
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    #timestamp = now.isoformat()

    specyamlfile = config.getoption("--specification")
    testyamlfile = config.getoption("--test")
    indent = int(config.getoption("--indent"))
    catverbosity = int(config.getoption("--catverbosity"))
    pytestflags = config.getoption("--pytestflags")

    specification: CodeAbilitySpecification = parse_spec_file(specyamlfile)
    testsuite: CodeAbilityTestSuite = parse_test_file(testyamlfile)

    """root-directory is always the location of the test.yaml file,
    relative directories are calculated from that root directory,
    however, all paths can be absolute as well 
    """
    root = os.path.abspath(os.path.dirname(testyamlfile))

    for directory in DIRECTORIES:
        dir = getattr(specification, directory)
        if not os.path.isabs(dir):
            dir = os.path.join(root, dir)
            dir = os.path.abspath(dir)
            setattr(specification, directory, dir)
        os.makedirs(dir, exist_ok=True)

    reportfile = specification.outputName
    if not os.path.isabs(reportfile):
        reportfile = os.path.join(specification.outputDirectory, reportfile)
    dir = os.path.dirname(reportfile)
    os.makedirs(dir, exist_ok=True)

    testcases = []
    main_tests: List[CodeAbilityReportMain] = []
    subfields = [
        "qualification",
        "relativeTolerance",
        "absoluteTolerance",
        "allowedOccuranceRange",
        "occuranceType",
        "verbosity",
    ]
    mainfields = subfields.copy();
    mainfields.extend([
        "storeGraphicsArtifacts",
        "competency",
        "timeout",
    ])
    def parent_property(properties, this, parent):
        for idx, property in enumerate(properties):
            if getattr(this, property) == None:
                setattr(this, property, getattr(parent, property))

    for idx_main, main in enumerate(testsuite.properties.tests):
        parent_property(mainfields, main, testsuite.properties)
        sub_tests: List[CodeAbilityReportSub] = []
        for idx_sub, sub in enumerate(main.tests):
            parent_property(subfields, sub, main)
            testcases.append((idx_main, idx_sub))
            sub_tests.append(CodeAbilityReportSub(name=sub.name))
        setup = None if main.setUpCode is None else "\n".join(get_property_as_list(main.setUpCode))
        teardown = None if main.tearDownCode is None else "\n".join(get_property_as_list(main.tearDownCode))
        main_tests.append(CodeAbilityReportMain(
            type=main.type,
            name=main.name,
            description=main.description,
            setup=setup,
            teardown=teardown,
            status=StatusEnum.scheduled,
            summary=CodeAbilityReportSummary(total=len(main.tests)),
            tests=sub_tests,
            timestamp=0,
        ))
    report = CodeAbilityReport(
        timestamp=timestamp,
        type=testsuite.type,
        version=testsuite.version,
        name=testsuite.name,
        description=testsuite.description,
        status=StatusEnum.scheduled,
        summary=CodeAbilityReportSummary(total=len(testsuite.properties.tests)),
        tests=main_tests,
    )
    report = {
        "report": report,
        "testcases": testcases,
        "testsuite": testsuite,
        "specification": specification,
        "reportfile": reportfile,
        "indent": indent,
        "created": time.time(),
        "started": 0,
        "solutions": {},
        "root": root,
        "testyamlfile": testyamlfile,
        "specyamlfile": specyamlfile,
        "catverbosity": catverbosity,
        "pytestflags": pytestflags,
    }
    config.stash[report_key] = report

def pytest_generate_tests(metafunc: pytest.Metafunc):
    report = metafunc.config.stash[report_key]
    metafunc.parametrize("testcases", report["testcases"])

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    out = yield
    _report: pytest.TestReport = out.get_result()
    if _report.when == "call":
        idx_main, idx_sub = item.callspec.params["testcases"]
        rep = item.config.stash[report_key]
        testsuite: CodeAbilityTestSuite = rep["testsuite"]
        main = testsuite.properties.tests[idx_main]
        sub = main.tests[idx_sub]
        _report.nodeid = f"{main.name}\\{sub.name}"

        report: CodeAbilityReport = rep["report"]
        testmain: CodeAbilityReportMain = report.tests[idx_main]
        testsub: CodeAbilityReportSub = testmain.tests[idx_sub]

        testsub.result = _report.outcome.upper()
        if _report.longrepr is not None:
            if testsub.result == ResultEnum.skipped:
                try:
                    # the actual skipped message is the third element in the list
                    # when skipped -> getting something like this:
                    # "longrepr": [
                    #     "I:\\PYTHON\\catester\\catester\\tests\\test_class.py",
                    #     263,
                    #     "Skipped: Success-Dependency `[1]` not satisfied"
                    # ],
                    # pytest -> BaseReport -> longrepr: Union[None, ExceptionInfo[BaseException], Tuple[str, int, str], str, TerminalRepr]
                    # see:
                    # https://github.com/pytest-dev/pytest/blob/main/src/_pytest/reports.py#L63
                    testsub.details = str(_report.longrepr[2])
                except:
                    testsub.details = str(_report.longrepr)
            else:
                testsub.details = str(_report.longrepr)
        testsub.debug = {
            "longrepr": _report.longrepr,
            "timestamp": time.time(),
        }
        testmain.timestamp = time.time()

def pytest_collection_modifyitems(session: pytest.Session, config: pytest.Config, items: List[pytest.Item]) -> None:
    pass

def pytest_runtest_logreport(report: pytest.TestReport):
    pass

def pytest_report_teststatus(report: pytest.TestReport, config):
    pass

def pytest_runtest_setup(item: pytest.Item) -> None:
    pass

def pytest_runtest_call(item: pytest.Item) -> None:
    pass

def pytest_runtest_teardown(item: pytest.Item, nextitem: pytest.Item) -> None:
    pass

def pytest_keyboard_interrupt(excinfo: pytest.ExceptionInfo) -> None:
    pass

def pytest_sessionstart(session: pytest.Session):
    _report = session.config.stash[report_key]
    _report["started"] = time.time()

def pytest_sessionfinish(session: pytest.Session):
    exitcode = session.exitstatus
    environment = session.config.stash[metadata_key]
    _report = session.config.stash[report_key]
    testyamlfile = _report["testyamlfile"]
    specyamlfile = _report["specyamlfile"]
    pytestflags = _report["pytestflags"]
    report: CodeAbilityReport = _report["report"]
    reportfile = _report["reportfile"]
    indent = _report["indent"]
    started = _report["started"]
    solutions = _report["solutions"]
    testsuite: CodeAbilityTestSuite = _report["testsuite"]
    duration = time.time() - started
    total = report.summary.total
    passed = 0
    failed = 0
    skipped = 0
    time_s = 0.0
    time_r = 0.0

    _teststarted = started
    for idx_main, main in enumerate(report.tests):
        _testended = float(main.timestamp)
        del main.timestamp
        _testduration = _testended - _teststarted
        _teststarted = _testended

        test_main = testsuite.properties.tests[idx_main]
        sub_time_s = 0
        sub_time_r = 0
        status = StatusEnum.completed
        idx = str(idx_main)
        tb = None
        errs = []
        if idx in solutions:
            solution_s = solutions[idx][Solution.student]
            solution_r = solutions[idx][Solution.reference]
            errs = solution_s["errors"]
            tb = solution_s["traceback"]
            sub_time_s = solution_s["exectime"]
            sub_time_r = solution_r["exectime"]
            status = solution_s["status"]
        sub_total = main.summary.total
        sub_passed = 0
        sub_failed = 0
        sub_skipped = 0
        for idx_sub, sub in enumerate(main.tests):
            test_sub = test_main.tests[idx_sub]
            if sub.result == ResultEnum.passed:
                sub_passed += 1
                result_message = test_sub.successMessage
            elif sub.result == ResultEnum.failed:
                sub_failed += 1
                result_message = test_sub.failureMessage
            elif sub.result == ResultEnum.skipped:
                sub_skipped += 1
                #todo: result_message needed in this case?
                #maybe add test_sub.skippedMessage for convenience?
                result_message = "Test skipped"
            else:
                result_message = "...unknown..."
            sub.resultMessage = result_message
        time_s += sub_time_s
        time_r += sub_time_r
        main.debug = {
            "executionDurationStudent": sub_time_s,
            "executionDurationReference": sub_time_r,
            "traceback": tb,
            "lintingErrors": errs,
        }
        main.duration = _testduration
        main.executionDuration = sub_time_s
        main.summary.passed = sub_passed
        main.summary.failed = sub_failed
        main.summary.skipped = sub_skipped
        main.status = status
        if sub_passed == sub_total:
            passed += 1
            main.result = ResultEnum.passed
            result_message = test_main.successMessage
        elif sub_skipped > 0:
            #todo: check if this is ok
            # if one subtest is skipped, set the collection to skipped
            skipped += 1
            main.result = ResultEnum.skipped
            #todo: result_message needed in this case?
            #maybe add test_main.skippedMessage for convenience?
            result_message = "Tests skipped"
        else:
            failed += 1
            main.result = ResultEnum.failed
            result_message = test_main.failureMessage
        main.resultMessage = result_message
    report.summary.passed = passed
    report.summary.skipped = skipped
    report.summary.failed = failed

    if exitcode == pytest.ExitCode.INTERRUPTED:
        report.status = StatusEnum.cancelled
    else:
        report.status = StatusEnum.completed

    if total == 0:
        report.result = ResultEnum.skipped
        result_message = "No Tests specified"
    elif passed == total:
        report.result = ResultEnum.passed
        result_message = testsuite.properties.successMessage
    elif skipped == total:
        report.result = ResultEnum.skipped
        #todo: result_message needed in this case?
        #maybe add testsuite.properties.skippedMessage for convenience?
        result_message = "Tests skipped"
    else:
        report.result = ResultEnum.failed
        result_message = testsuite.properties.failureMessage

    report.resultMessage = result_message
    report.environment = environment
    report.duration = duration
    report.executionDuration = time_s
    report.debug = {
        "executionDurationStudent": time_s,
        "executionDurationReference": time_r,
    }
    report.properties = {
        "test": testyamlfile,
        "specification": specyamlfile,
        "pytestflags": pytestflags,
        "exitcode": str(exitcode),
    }

    with open(reportfile, "w", encoding="utf-8") as file:
        json.dump(report.model_dump(exclude_none=True), file, default=str, indent=indent)

    """exit codes:
    https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.ExitCode
    OK = 0, Tests passed.
    TESTS_FAILED = 1, Tests failed.
    INTERRUPTED = 2, pytest was interrupted.
    INTERNAL_ERROR = 3, An internal error got in the way.
    USAGE_ERROR = 4, pytest was misused.
    NO_TESTS_COLLECTED = 5, pytest could not find tests.
    """

@pytest.hookimpl(trylast=True)
def pytest_report_header(config):
    _report = config.stash[report_key]
    root = _report["root"]
    testyamlfile = _report["testyamlfile"]
    specyamlfile = _report["specyamlfile"]
    pytestflags = _report["pytestflags"]
    catverbosity = _report["catverbosity"]
    verbosity = config.getoption("verbose")
    if specyamlfile == "":
        specyamlfile = "not set"

    tw, _ = shutil.get_terminal_size(fallback=(80, 24))
    full = "=" * tw
    return [
        f"{full}",
        f"{Fore.CYAN}CodeAbility Python Testing Engine{Style.RESET_ALL}",
        f"{full}",
        f"{Fore.CYAN}testroot:      {Style.RESET_ALL} {root}",
        f"{Fore.CYAN}testsuite:     {Style.RESET_ALL} {testyamlfile}",
        f"{Fore.CYAN}specification: {Style.RESET_ALL} {specyamlfile}",
        f"{Fore.CYAN}pytestflags:   {Style.RESET_ALL} {pytestflags}",
        f"{Fore.CYAN}catverbosity:  {Style.RESET_ALL} {catverbosity}",
        f"{Fore.CYAN}verbosity:     {Style.RESET_ALL} {verbosity}",
        f"{full}",
    ]

def pytest_terminal_summary(terminalreporter: TerminalReporter, exitstatus: pytest.ExitCode, config: pytest.Config):
    _report = config.stash[report_key]
    catverbosity = _report["catverbosity"]
    if catverbosity > 2:
        report: CodeAbilityReport = _report["report"]
        testsuite: CodeAbilityTestSuite = _report["testsuite"]

        total = report.summary.total
        passed = report.summary.passed
        failed = report.summary.failed
        skipped = report.summary.skipped
        terminalreporter.ensure_newline()
        terminalreporter.section(f"{testsuite.name} - Summary", sep="~", purple=True, bold=True)
        terminalreporter.line(f"Total Test Collections: {total}")
        terminalreporter.line(f"PASSED: {passed} ", green=True)
        terminalreporter.line(f"FAILED: {failed} ", red=True)
        terminalreporter.line(f"SKIPPED: {skipped} ", yellow=True)
        for idx_main, main in enumerate(report.tests):
            test_main = testsuite.properties.tests[idx_main]
            sub_total = main.summary.total
            sub_passed = main.summary.passed
            sub_failed = main.summary.failed
            sub_skipped = main.summary.skipped
            testtext = "Test" if sub_total == 1 else "Tests"
            terminalreporter.write_sep("*", f"Testcollection {idx_main + 1}")
            terminalreporter.line(f"{test_main.name} ({sub_total} {testtext})")
            if sub_passed > 0:
                terminalreporter.line(f"PASSED: {sub_passed} ", green=True)
            if sub_failed > 0:
                terminalreporter.line(f"FAILED: {sub_failed} ", red=True)
            if sub_skipped > 0:
                terminalreporter.line(f"SKIPPED: {sub_skipped} ", yellow=True)
            for idx_sub, sub in enumerate(main.tests):
                test_sub = test_main.tests[idx_sub]
                outcome = sub.result
                terminalreporter.line(
                    f"Test {idx_sub + 1} ({test_sub.name}): {outcome} ",
                    green=outcome == ResultEnum.passed,
                    red=outcome == ResultEnum.failed,
                    yellow=outcome == ResultEnum.skipped,
                )

@pytest.fixture(scope="function")
def monkeymodule():
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()
