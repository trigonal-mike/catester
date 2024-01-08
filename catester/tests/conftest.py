import os
import datetime
import pytest
from model import DIRECTORIES, parse_spec_file, parse_test_file, CodeAbilityTestSuite

def pytest_addoption(parser):
    parser.addoption("--specyamlfile", default="", help="please provide a valid specification yamlfile", )
    parser.addoption("--testyamlfile", default="", help="please provide a valid test yamlfile", )

def pytest_generate_tests(metafunc):
    """
    all testcases are parametrized here\n
    List of Tuples [(0, 0), (0, 1), (0, 2), (1, 0), ...]\n
    meaning the test function using the fixture "testcases"\n
    is being called with each of the tuples (seperately)
    """
    testyamlfile = metafunc.config.getoption("--testyamlfile")
    config = parse_test_file(testyamlfile)
    testcases = []
    for idx_main, main_test in enumerate(config.properties.tests):
        for idx_sub, sub_test in enumerate(main_test.tests):
            testcases.append((idx_main, idx_sub))
    metafunc.parametrize("testcases", testcases)

@pytest.fixture(scope="class")
def config(request):
    """ this fixture is called once for all tests """
    specyamlfile = request.config.getoption("--specyamlfile")
    testyamlfile = request.config.getoption("--testyamlfile")
    dirabs = os.path.abspath(os.path.dirname(specyamlfile))
    dict = {}
    dict["abs_path_to_yaml"] = dirabs
    dict["specification"] = parse_spec_file(specyamlfile)
    dict["testsuite"] = parse_test_file(testyamlfile)
    for directory in DIRECTORIES:
        _dir = getattr(dict["specification"].testInfo, directory)
        if not os.path.isabs(_dir):
            _dir = os.path.join(dirabs, _dir)
            setattr(dict["specification"].testInfo, directory, _dir)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
    yield dict
    print("teardown")

# this fixture is called for each test
@pytest.fixture(scope="function")
def monkeymodule():
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()

def pytest_metadata(metadata, config):
    specyamlfile = config.getoption("--specyamlfile")
    testyamlfile = config.getoption("--testyamlfile")

    metadata["specyamlfile"] = specyamlfile
    metadata["testyamlfile"] = testyamlfile

    xxx = dict()
    xxx["specification"] = parse_spec_file(specyamlfile)
    xxx["testsuite"] = parse_test_file(testyamlfile)
    xxx["metadata"] = metadata

    globals()["_xxx_"] = xxx
    pass

def pytest_json_runtest_stage(report):
    pass

def pytest_json_runtest_metadata(item, call):
    pass

def pytest_json_modifyreport(json_report):
    xxx = globals()["_xxx_"]
    metadata = xxx["metadata"]
    testsuite: CodeAbilityTestSuite = xxx["testsuite"]

    #json_report['name'] = config()["testsuite"]["name"]
    #json_report['xxxxxx'] = 'xxxxxxxxxxxxxx'
    #x = len(globals()["solutions"])
    #json_report['xxxxxx'] = f'xxxxxxxxxxxxxx:{x}'

    converted_tests = []
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
        converted_tests.append(converted)

    #ts = time.gmtime(float(json_report['created']))
    #timestamp = time.strftime("%Y-%m-%d %H:%M:%S.", ts)

    dobj = datetime.datetime.fromtimestamp(json_report['created'])
    timestamp = dobj.strftime("%Y-%m-%d %H:%M:%S.%f")
    #timestamp = dobj.isoformat()

    #json_report['_xxx'] = xxx
    json_report['_duration'] = json_report['duration']

    json_report['_metadata'] = metadata
    json_report['_timestamp'] = timestamp
    json_report['_type'] = testsuite.type
    json_report['_version'] = testsuite.version
    json_report['_name'] = testsuite.name
    json_report['_status'] = "COMPLETED"
    json_report['_result'] = str(json_report['exitcode'])
    json_report['_tests'] = converted_tests

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
    report = session.config._json_report.report
    print('\nexited with', report['exitcode'])


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