import json
import os
import datetime
import pytest
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
testcases_key = pytest.StashKey[list]()
testsuite_key = pytest.StashKey[CodeAbilityTestSuite]()
specification_key = pytest.StashKey[CodeAbilitySpecification]()

def pytest_addoption(parser):
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

    # parse specification yaml-file, set paths to absolute, create directories
    specyamlfile = config.getoption("--specyamlfile")
    specification = parse_spec_file(specyamlfile)
    root = os.path.abspath(os.path.dirname(specyamlfile))
    for directory in DIRECTORIES:
        _dir = getattr(specification.testInfo, directory)
        if not os.path.isabs(_dir):
            _dir = os.path.join(root, _dir)
            setattr(specification.testInfo, directory, _dir)
        if not os.path.exists(_dir):
            os.makedirs(_dir)

    # parse testsuite yaml-file, populate testcases, generate report-skeleton
    testyamlfile = config.getoption("--testyamlfile")
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
            })
        main_tests.append({
            "type": main.type,
            "name": main.name,
            "description": main.description,
            "setup": main.setUpCode,
            "teardown": main.tearDownCode,
            "status": TestStatus.scheduled,
            "result": None,
            "summary": {
                "total": len(main.tests),
                "success": 0,
                "failed": 0,
                "skipped": 0,
            },
            "tests": sub_tests,
        })
    report = {
        "type": testsuite.type,
        "version": testsuite.version,
        "name": testsuite.name,
        "description": testsuite.description,
        "status": TestStatus.scheduled,
        "result": None,
        "summary": {
            "total": len(testsuite.properties.tests),
            "success": 0,
            "failed": 0,
            "skipped": 0,
        },
        "tests": main_tests,
    }
    config.stash[report_key] = report
    config.stash[testcases_key] = testcases
    config.stash[testsuite_key] = testsuite
    config.stash[specification_key] = specification

def pytest_generate_tests(metafunc):
    metafunc.parametrize("testcases", metafunc.config.stash[testcases_key])

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
    _report.session = item.session
    _report.testcase = item.callspec.params["testcases"]

def pytest_runtest_logreport(report: pytest.TestReport):
    pass
    #if report.when == 'call':
    #    oc = {}
    #    oc[f"{report.testcase[0]}-{report.testcase[1]}"] = report.passed
    #    #report.session.config.stash[outcomes].update(oc)

def pytest_report_teststatus(report: pytest.TestReport, config):
    pass
    #line = f'{report.nodeid}:\t"{report.when}"'
    #report.sections.append(('My custom section', line))
    #if report.when == 'call' and report.passed:
    #    short_outcome = "#"
    #    long_outcome = "TEST PASSED"
    #    return report.outcome, short_outcome, long_outcome

def pytest_terminal_summary(terminalreporter, exitstatus, config):
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

def pytest_runtest_setup(item: pytest.Item) -> None:
    pass

def pytest_runtest_call(item: pytest.Item) -> None:
    pass

def pytest_runtest_teardown(item, nextitem) -> None:
    pass

def pytest_json_runtest_stage(report):
    """This hook is for changing setup, call and teardown fields of the report,
    see: https://pypi.org/project/pytest-json-report/"""
    pass
    #return {'oooooooooo': report.outcome}
    #if report.when != 'call':
    #    return {'oooooooooo': report.outcome}

def pytest_json_runtest_metadata(item, call):
    return
    if call.when == 'call':
       sss = item.config.stash[some_str_key]
       sss1 = sss + "."
       item.config.stash[some_str_key] = sss1

    return {'zzz': {"ddd": 123}}
    if call.when != 'call':
        return {}
    return {'xxx': call.start, 'stop': call.stop}
    #pass

def pytest_json_modifyreport(json_report):
    converted_main = []
    for test in json_report['tests']:
        converted = dict()
        converted["name"] = test["metadata"]["main_name"]
        converted["variable"] = test["metadata"]["sub_name"]
        converted["status"] = "COMPLETED"
        converted["result"] = str(test["outcome"]).upper()
        if test["outcome"] == "passed":
            converted["details"] = test["metadata"]["success_message"]
        elif test["outcome"] == "failed":
            converted["details"] = test["metadata"]["failure_message"]
        converted_main.append(converted)

    #ts = time.gmtime(float(json_report['created']))
    #timestamp = time.strftime("%Y-%m-%d %H:%M:%S.", ts)

    dobj = datetime.datetime.fromtimestamp(json_report['created'])
    timestamp = dobj.strftime("%Y-%m-%d %H:%M:%S.%f")
    #timestamp = dobj.isoformat()

    json_report['_duration'] = json_report['duration']
    json_report['_timestamp'] = timestamp
    json_report['_status'] = "COMPLETED"
    json_report['_result'] = str(json_report['exitcode'])
    json_report['_tests'] = converted_main

    # delete other entries:
    #del json_report['created']
    #del json_report['duration']
    #del json_report['exitcode']
    #del json_report['root']
    #del json_report['environment']
    #del json_report['summary']
    #del json_report['collectors']
    #del json_report['tests']


def pytest_sessionfinish(session):
    json_report = session.config._json_report.report

    metadata = session.config.stash[metadata_key]
    report = session.config.stash[report_key]
    report["environment"] = metadata

    total = report["summary"]["total"]
    success = 0
    failed = 0
    skipped = 0
    for idx_main, main in enumerate(report["tests"]):
        sub_total = main["summary"]["total"]
        sub_success = 0
        sub_failed = 0
        sub_skipped = 0
        for idx_sub, sub in enumerate(main["tests"]):
            if sub["result"] == TestResult.passed:
                sub_success = sub_success + 1
            elif sub["result"] == TestResult.failed:
                sub_failed = sub_failed + 1
            elif sub["result"] == TestResult.skipped:
                sub_skipped = sub_skipped + 1

        main["summary"]["success"] = sub_success
        main["summary"]["failed"] = sub_failed
        main["summary"]["skipped"] = sub_skipped
        if sub_success == sub_total:
            main["result"] = TestResult.passed
            success = success + 1
        elif sub_skipped > 0:
            main["result"] = TestResult.skipped
            skipped = skipped + 1
        else:
            main["result"] = TestResult.failed
            failed = failed + 1

    report["summary"]["success"] = success
    report["summary"]["skipped"] = skipped
    report["summary"]["failed"] = failed
    report["status"] = TestStatus.completed
    if success == total:
        report["result"] = TestResult.passed
    elif skipped == total:
        report["result"] = TestResult.skipped
    else:
        report["result"] = TestResult.failed

    json_report['_report'] = report

    with open("xxx.json", 'w', encoding='utf-8') as file:
        json.dump(
            json_report,
            file,
            default=str,
            indent=session.config.option.json_report_indent,
        )

    print('\nexited with', json_report['exitcode'])


"""
exit codes:
https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.ExitCode
OK = 0
Tests passed.

TESTS_FAILED = 1
Tests failed.

INTERRUPTED = 2
pytest was interrupted.

INTERNAL_ERROR = 3
An internal error got in the way.

USAGE_ERROR = 4
pytest was misused.

NO_TESTS_COLLECTED = 5
pytest could not find tests.
"""