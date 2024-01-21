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
    pending = "PENDING"
    running = "RUNNING"
    cancelled = "CANCELLED"
    completed = "COMPLETED"
    failed = "FAILED"
    crashed = "CRASHED"

class TestResult(str, Enum):
    failed = "FAILED"
    passed = "PASSED"
    skipped = "SKIPPED"
    timedout = "TIMEDOUT"

metadata_key = pytest.StashKey[dict]()
report_key = pytest.StashKey[dict]()

def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--specification",
        default="specification.yaml",
        help="specification yaml input file",
    )
    parser.addoption(
        "--test",
        default="test.yaml",
        help="test yaml input file",
    )
    parser.addoption(
        "--output",
        default="report.json",
        help="json report output file",
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
    reportfile = config.getoption("--output")
    indent = int(config.getoption("--indent"))

    specification = parse_spec_file(specyamlfile)
    testsuite = parse_test_file(testyamlfile)

    """root-directory is always the location of the test.yaml file
    if relative directories are calculated from that root directory,
    however, all paths can be absolute as well 
    """
    root = os.path.abspath(os.path.dirname(testyamlfile))

    for directory in DIRECTORIES:
        dir = getattr(specification.testInfo, directory)
        if not os.path.isabs(dir):
            dir = os.path.join(root, dir)
            setattr(specification.testInfo, directory, dir)
        if not os.path.exists(dir):
            os.makedirs(dir)
    if not os.path.isabs(reportfile):
        reportfile = os.path.join(specification.testInfo.outputDirectory, reportfile)
    dir = os.path.dirname(reportfile)
    if not os.path.exists(dir):
        os.makedirs(dir)

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
        "storeGraphicsArtefacts",
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
            "resultMessage": None,
            "details": None,
            "executionDurationReference": None,
            "executionDurationStudent": None,
            "summary": {
                "total": len(main.tests),
                "success": 0,
                "failed": 0,
                "skipped": 0,
                "timedout": 0,
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
        "resultMessage": None,
        "details": None,
        "duration": None,
        "executionDurationReference": None,
        "executionDurationStudent": None,
        "environment": None,
        "properties": None,
        "debug": None,
        "exitcode": None,
        "summary": {
            "total": len(testsuite.properties.tests),
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "timedout": 0,
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

def pytest_generate_tests(metafunc):
    metafunc.parametrize("testcases", metafunc.config.stash[report_key]["testcases"])

def get_item(haystack: list[tuple[str, object]], needle, default):
    for x, y in enumerate(haystack):
        s, o = y
        if s == needle:
            return o
    return default

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    item.add_report_section("x", "y", "report section contents\nfds")
    out = yield
    _report: pytest.TestReport = out.get_result()
    if _report.when == 'call':
        idx_main, idx_sub = item.callspec.params["testcases"]
        report = item.config.stash[report_key]["report"]
        timeout = get_item(item.user_properties, "timeout", False)
        if timeout:
            result = TestResult.timedout
        else:
            result = _report.outcome.upper()
        test = report["tests"][idx_main]["tests"][idx_sub]
        test["result"] = result
        test["status"] = TestStatus.completed
        test["executionDurationReference"] = get_item(item.user_properties, "exec_time_reference", 0)
        test["executionDurationStudent"] = get_item(item.user_properties, "exec_time_student", 0)
        test["longrepr"] = _report.longrepr
        #_report.longrepr = f"Test ({idx_main},{idx_sub}) failed"

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

# Following 3 hooks form JSON-Report, see: https://pypi.org/project/pytest-json-report/
#def pytest_json_runtest_stage(report):
#    pass

#def pytest_json_runtest_metadata(item, call):
#    pass

#def pytest_json_modifyreport(json_report):
#    pass

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
    timedout = 0
    time_r = 0.0
    time_s = 0.0
    for idx_main, main in enumerate(report["tests"]):
        test_main = testsuite.properties.tests[idx_main]
        sub_total = main["summary"]["total"]
        sub_success = 0
        sub_failed = 0
        sub_skipped = 0
        sub_timedout = 0
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
            elif sub["result"] == TestResult.timedout:
                sub_timedout = sub_timedout + 1
                result_message = "Test timedout"
            else:
                result_message = "...unknown..."
            sub["resultMessage"] = result_message
        time_r = time_r + sub_time_r
        time_s = time_s + sub_time_s
        main["executionDurationReference"] = sub_time_r
        main["executionDurationStudent"] = sub_time_s
        main["summary"]["success"] = sub_success
        main["summary"]["failed"] = sub_failed
        main["summary"]["skipped"] = sub_skipped
        main["summary"]["timedout"] = sub_timedout
        main["status"] = TestStatus.completed
        if sub_success == sub_total:
            success = success + 1
            main["result"] = TestResult.passed
            result_message = test_main.successMessage
        elif sub_skipped > 0:
            skipped = skipped + 1
            main["result"] = TestResult.skipped
            result_message = "Tests skipped"
        elif sub_timedout > 0:
            timedout = timedout + 1
            main["result"] = TestResult.timedout
            result_message = "Tests timedout"
        else:
            failed = failed + 1
            main["result"] = TestResult.failed
            result_message = test_main.failureMessage
        main["resultMessage"] = result_message
    report["summary"]["success"] = success
    report["summary"]["skipped"] = skipped
    report["summary"]["failed"] = failed
    report["summary"]["timedout"] = timedout

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
    report["executionDurationReference"] = time_r
    report["executionDurationStudent"] = time_s
    report["duration"] = duration
    report["exitcode"] = str(exitcode)
    if hasattr(session.config, "_json_report"):
        report['_json_report'] = session.config._json_report.report

    with open(reportfile, 'w', encoding='utf-8') as file:
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


def pytest_report_header(config):
    verbosity = config.getoption("verbose")
    return ["CodeAbility Python Testing", f"verbosity: {verbosity}"]

def pytest_terminal_summary(terminalreporter: TerminalReporter, exitstatus: pytest.ExitCode, config: pytest.Config):
    verbosity = config.getoption("verbose")
    if verbosity > 0:
        terminalreporter.ensure_newline()
        terminalreporter.section('My custom section', sep='#', black=True, Purple=True, light=True)
        terminalreporter.line("...something else...")

@pytest.fixture(scope="function")
def monkeymodule():
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()
