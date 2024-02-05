import json
import os
import datetime
import time
import pytest
from _pytest.terminal import TerminalReporter
from enum import Enum
from model import DIRECTORIES
from model import parse_spec_file, parse_test_file
from model import CodeAbilityTestSuite, CodeAbilitySpecification

class TestStatus(str, Enum):
    scheduled = "SCHEDULED"
    completed = "COMPLETED"
    timedout = "TIMEDOUT"
    crashed = "CRASHED"
    cancelled = "CANCELLED"
    # following not used yet:
    failed = "FAILED"
    pending = "PENDING"
    running = "RUNNING"

class TestResult(str, Enum):
    passed = "PASSED"
    failed = "FAILED"
    skipped = "SKIPPED"

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

    specification = parse_spec_file(specyamlfile)
    testsuite = parse_test_file(testyamlfile)

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

    reportfile = specification.testOutputName
    if not os.path.isabs(reportfile):
        reportfile = os.path.join(specification.outputDirectory, reportfile)
    dir = os.path.dirname(reportfile)
    os.makedirs(dir, exist_ok=True)

    testcases = []
    main_tests = []
    subfields = [
        "qualification",
        "relativeTolerance",
        "absoluteTolerance",
        "allowedOccuranceRange",
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
        sub_tests = []
        for idx_sub, sub in enumerate(main.tests):
            parent_property(subfields, sub, main)
            testcases.append((idx_main, idx_sub))
            sub_tests.append({
                "name": sub.name,
                "status": TestStatus.scheduled,
                "result": None,
                "resultMessage": None,
                "details": None,
            })
        main_tests.append({
            "type": main.type,
            "name": main.name,
            "description": main.description,
            "setup": main.setUpCode,
            "teardown": main.tearDownCode,
            "status": TestStatus.scheduled,
            "result": None,
            "statusMessage": None,
            "resultMessage": None,
            "details": None,
            "duration": None,
            "executionDuration": None,
            "summary": {
                "total": len(main.tests),
                "success": 0,
                "failed": 0,
                "skipped": 0,
            },
            "tests": sub_tests,
        })
    report = {
        "timestamp": timestamp,
        "type": testsuite.type,
        "version": testsuite.version,
        "name": testsuite.name,
        "description": testsuite.description,
        "status": TestStatus.scheduled,
        "result": None,
        "statusMessage": None,
        "resultMessage": None,
        "details": None,
        "duration": None,
        "executionDuration": None,
        "environment": None,
        "properties": None,
        "debug": None,
        "exitcode": None,
        "summary": {
            "total": len(testsuite.properties.tests),
            "success": 0,
            "failed": 0,
            "skipped": 0,
        },
        "tests": main_tests,
    }
    report = {
        "report": report,
        "testcases": testcases,
        "testsuite": testsuite,
        "specification": specification,
        "reportfile": reportfile,
        "indent": indent,
        "created": time.time(),
        "started": 0,
    }
    config.stash[report_key] = report

def pytest_generate_tests(metafunc: pytest.Metafunc):
    report = metafunc.config.stash[report_key]
    metafunc.parametrize("testcases", report["testcases"])

def get_item(haystack: list[tuple[str, object]], needle, default):
    for x, y in enumerate(haystack):
        s, o = y
        if s == needle:
            return o
    return default

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    #item.add_report_section("x", "y", "report section contents\nfds")
    out = yield
    _report: pytest.TestReport = out.get_result()
    if _report.when == "call":
        idx_main, idx_sub = item.callspec.params["testcases"]
        rep = item.config.stash[report_key]
        report = rep["report"]
        testsuite: CodeAbilityTestSuite = rep["testsuite"]
        main = testsuite.properties.tests[idx_main]
        sub = main.tests[idx_sub]

        timeout = get_item(item.user_properties, "timeout", False)
        if timeout:
            status = TestStatus.timedout
        else:
            status = TestStatus.completed
        test = report["tests"][idx_main]["tests"][idx_sub]
        test["status"] = status
        test["result"] = _report.outcome.upper()
        test["executionDurationReference"] = get_item(item.user_properties, "exec_time_reference", 0)
        test["executionDurationStudent"] = get_item(item.user_properties, "exec_time_student", 0)
        test["details"] = {
            "longrepr": _report.longrepr,
            "timestamp": time.time(),
        }
        _report.nodeid = f"{main.name}\\{sub.name}"

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
    report = _report["report"]
    reportfile = _report["reportfile"]
    indent = _report["indent"]
    started = _report["started"]
    testsuite: CodeAbilityTestSuite = _report["testsuite"]

    duration = time.time() - started

    total = report["summary"]["total"]
    success = 0
    failed = 0
    skipped = 0
    time_r = 0.0
    time_s = 0.0
    for idx_main, main in enumerate(report["tests"]):
        test_main = testsuite.properties.tests[idx_main]
        sub_total = main["summary"]["total"]
        sub_success = 0
        sub_failed = 0
        sub_skipped = 0
        sub_time_r = 0.0
        sub_time_s = 0.0
        for idx_sub, sub in enumerate(main["tests"]):
            test_sub = test_main.tests[idx_sub]
            if "executionDurationReference" in sub and "executionDurationStudent" in sub:
                sub_time_r = sub_time_r + sub["executionDurationReference"]
                sub_time_s = sub_time_s + sub["executionDurationStudent"]
                del sub["executionDurationReference"]
                del sub["executionDurationStudent"]
            if sub["result"] == TestResult.passed:
                sub_success = sub_success + 1
                result_message = test_sub.successMessage
            elif sub["result"] == TestResult.failed:
                sub_failed = sub_failed + 1
                result_message = test_sub.failureMessage
            elif sub["result"] == TestResult.skipped:
                sub_skipped = sub_skipped + 1
                result_message = "Test skipped"
            else:
                result_message = "...unknown..."
            sub["resultMessage"] = result_message
        time_r = time_r + sub_time_r
        time_s = time_s + sub_time_s
        main["details"] = {
            "executionDurationReference": sub_time_r,
            "executionDurationStudent": sub_time_s,
        }
        main["duration"] = sub_time_s
        main["executionDuration"] = sub_time_s
        main["summary"]["success"] = sub_success
        main["summary"]["failed"] = sub_failed
        main["summary"]["skipped"] = sub_skipped
        main["status"] = TestStatus.completed
        if sub_success == sub_total:
            success = success + 1
            main["result"] = TestResult.passed
            result_message = test_main.successMessage
        elif sub_skipped > 0:
            skipped = skipped + 1
            main["result"] = TestResult.skipped
            result_message = "Tests skipped"
        else:
            failed = failed + 1
            main["result"] = TestResult.failed
            result_message = test_main.failureMessage
        main["resultMessage"] = result_message
    report["summary"]["success"] = success
    report["summary"]["skipped"] = skipped
    report["summary"]["failed"] = failed

    if exitcode == pytest.ExitCode.INTERRUPTED:
        report["status"] = TestStatus.cancelled
    else:
        report["status"] = TestStatus.completed

    if success == total:
        report["result"] = TestResult.passed
        result_message = testsuite.properties.successMessage
    elif skipped == total:
        report["result"] = TestResult.skipped
        result_message = "Tests skipped"
    else:
        report["result"] = TestResult.failed
        result_message = testsuite.properties.failureMessage

    report["resultMessage"] = result_message
    report["environment"] = environment
    report["duration"] = duration
    report["executionDuration"] = time_s
    report["exitcode"] = str(exitcode)
    report["details"] = {
        "executionDurationReference": time_r,
        "executionDurationStudent": time_s,
    }

    with open(reportfile, "w", encoding="utf-8") as file:
        json.dump(report, file, default=str, indent=indent)

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
    verbosity = config.getoption("verbose")
    return [
        "==========================",
        "CodeAbility Python Testing",
        f"verbosity: {verbosity}",
        "==========================",
    ]

def pytest_terminal_summary(terminalreporter: TerminalReporter, exitstatus: pytest.ExitCode, config: pytest.Config):
    return
    verbosity = config.getoption("verbose")
    if verbosity >= 0:
        _report = config.stash[report_key]
        report = _report["report"]
        testsuite: CodeAbilityTestSuite = _report["testsuite"]

        total = report["summary"]["total"]
        success = report["summary"]["success"]
        failed = report["summary"]["failed"]
        skipped = report["summary"]["skipped"]
        terminalreporter.ensure_newline()
        terminalreporter.section(f"{testsuite.name} - Summary", sep="~", purple=True, bold=True)
        terminalreporter.line(f"Total Test Collections: {total}")
        terminalreporter.line(f"PASSED: {success} ", green=True)
        terminalreporter.line(f"FAILED: {failed} ", red=True)
        terminalreporter.line(f"SKIPPED: {skipped} ", yellow=True)
        for idx_main, main in enumerate(report["tests"]):
            test_main = testsuite.properties.tests[idx_main]
            sub_total = main["summary"]["total"]
            sub_success = main["summary"]["success"]
            sub_failed = main["summary"]["failed"]
            sub_skipped = main["summary"]["skipped"]
            testtext = "Test" if sub_total == 1 else "Tests"
            terminalreporter.write_sep("*", f"Testcollection {idx_main + 1}")
            terminalreporter.line(f"{test_main.name} ({sub_total} {testtext})")
            if sub_success > 0:
                terminalreporter.line(f"PASSED: {sub_success} ", green=True)
            if sub_failed > 0:
                terminalreporter.line(f"FAILED: {sub_failed} ", red=True)
            if sub_skipped > 0:
                terminalreporter.line(f"SKIPPED: {sub_skipped} ", yellow=True)
            for idx_sub, sub in enumerate(main["tests"]):
                test_sub = test_main.tests[idx_sub]
                outcome = sub["result"]
                terminalreporter.line(
                    f"Test {idx_sub + 1} ({test_sub.name}): {outcome} ",
                    green=outcome == TestResult.passed,
                    red=outcome == TestResult.failed,
                    yellow=outcome == TestResult.skipped,
                )

@pytest.fixture(scope="function")
def monkeymodule():
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()
