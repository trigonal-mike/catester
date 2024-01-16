import json
import os
import datetime
import pytest
from enum import Enum
from pathlib import Path
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

reportfile_key = pytest.StashKey[str]()
metadata_key = pytest.StashKey[dict]()
report_key = pytest.StashKey[dict]()
testcases_key = pytest.StashKey[list]()
testsuite_key = pytest.StashKey[CodeAbilityTestSuite]()
specification_key = pytest.StashKey[CodeAbilitySpecification]()

def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--specyamlfile",
        default="",
        help="please provide a specification yamlfile",
    )
    parser.addoption(
        "--testyamlfile",
        default="",
        help="please provide a test yamlfile",
    )
    parser.addoption(
        "--reportfile",
        default="report.json",
        help="please provide a json report filename",
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

    specyamlfile = config.getoption("--specyamlfile")
    testyamlfile = config.getoption("--testyamlfile")
    reportfile = config.getoption("--reportfile")

    # parse specification yaml-file, set paths to absolute, create directories
    specification = parse_spec_file(specyamlfile)
    root = os.path.abspath(os.path.dirname(specyamlfile))
    for directory in DIRECTORIES:
        _dir = getattr(specification.testInfo, directory)
        if not os.path.isabs(_dir):
            _dir = os.path.join(root, _dir)
            setattr(specification.testInfo, directory, _dir)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
    if not os.path.isabs(reportfile):
        reportfile = os.path.join(specification.testInfo.outputDirectory, reportfile)

    # parse testsuite yaml-file, populate testcases, generate report-skeleton
    testsuite = parse_test_file(testyamlfile)
    testcases = []
    main_tests = []
    for idx_main, main in enumerate(testsuite.properties.tests):
        sub_tests = []
        for idx_sub, sub in enumerate(main.tests):
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
        "summary": {
            "total": len(testsuite.properties.tests),
            "success": 0,
            "failed": 0,
            "skipped": 0,
        },
        "tests": main_tests,
    }
    config.stash[reportfile_key] = reportfile
    config.stash[report_key] = report
    config.stash[testcases_key] = testcases
    config.stash[testsuite_key] = testsuite
    config.stash[specification_key] = specification

def pytest_generate_tests(metafunc):
    metafunc.parametrize("testcases", metafunc.config.stash[testcases_key])

def get_item(haystack: list[tuple[str, object]], needle, default):
    for x, y in enumerate(haystack):
        s, o = y
        if s == needle:
            return o
    return default

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    out = yield
    _report: pytest.TestReport = out.get_result()
    if _report.when == 'call':
        idx_main, idx_sub = item.callspec.params["testcases"]
        report = item.config.stash[report_key]
        test = report["tests"][idx_main]["tests"][idx_sub]
        test["result"] = _report.outcome.upper()
        test["status"] = TestStatus.completed
        test["executionDurationReference"] = get_item(item.user_properties, "exec_time_reference", 0)
        test["executionDurationStudent"] = get_item(item.user_properties, "exec_time_student", 0)

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

# Following 3 hooks form JSON-Report
# https://pypi.org/project/pytest-json-report/
def pytest_json_runtest_stage(report):
    pass

def pytest_json_runtest_metadata(item, call):
    pass

def pytest_json_modifyreport(json_report):
    pass

def pytest_sessionfinish(session):
    json_report = session.config._json_report.report
    indent = session.config.option.json_report_indent
    reportfile = session.config.stash[reportfile_key]
    environment = session.config.stash[metadata_key]
    report = session.config.stash[report_key]
    testsuite: CodeAbilityTestSuite = session.config.stash[testsuite_key]

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
        main["executionDurationReference"] = sub_time_r
        main["executionDurationStudent"] = sub_time_s
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
    report["duration"] = json_report['duration']
    report['exit_code'] = str(json_report['exitcode'])
    report['json_report'] = json_report

    with open(reportfile, 'w', encoding='utf-8') as file:
        json.dump(report,file,default=str,indent=indent)

    print('\nexited with', json_report['exitcode'])
    """exit codes:
    https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.ExitCode
    OK = 0, Tests passed.
    TESTS_FAILED = 1, Tests failed.
    INTERRUPTED = 2, pytest was interrupted.
    INTERNAL_ERROR = 3, An internal error got in the way.
    USAGE_ERROR = 4, pytest was misused.
    NO_TESTS_COLLECTED = 5, pytest could not find tests.
    """

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    terminalreporter.ensure_newline()
    terminalreporter.section('My custom section', sep='#', blue=True, bold=True)
    terminalreporter.line("...something else...")
    pass
    #reports = terminalreporter.getreports('')
    #content = os.linesep.join(text for report in reports for secname, text in report.sections)
    #if content:
    #    terminalreporter.ensure_newline()
    #    terminalreporter.section('My custom section', sep='#', blue=True, bold=True)
    #    terminalreporter.line(content)
    #    terminalreporter.line("...something else...")

@pytest.fixture(scope="function")
def monkeymodule():
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()
