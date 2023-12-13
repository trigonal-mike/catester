import os
import datetime
import pytest
from model import parse_yaml_file

def pytest_addoption(parser):
    parser.addoption("--yamlfile", default="", help="please provide a valid yamlfile", )

# all testcases will be parametrized here
# List of Tuples [(0, 0), (0, 1), (0, 2), (1, 0), ...]
# meaning the test function using the fixture "testcases"
# is being called with each of the tuples (seperately)
def pytest_generate_tests(metafunc):
    yamlfile = metafunc.config.getoption("--yamlfile")
    config = parse_yaml_file(yamlfile)
    testcases = []
    for idx_main, main_test in enumerate(config["properties"]["tests"]):
        for idx_sub, sub_test in enumerate(main_test["tests"]):
            testcases.append((idx_main, idx_sub))
    metafunc.parametrize("testcases", testcases)

# this fixture is called once for all tests
@pytest.fixture(scope="class")
def config(request):
    yamlfile = request.config.getoption("--yamlfile")
    dirabs = os.path.abspath(os.path.dirname(yamlfile))
    dict = {}
    dict["abs_path_to_yaml"] = dirabs
    dict["testsuite"] = parse_yaml_file(yamlfile)
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
    yamlfile = config.getoption("--yamlfile")

    metadata["yamlfile"] = yamlfile

    xxx = dict()
    xxx["testsuite"] = parse_yaml_file(yamlfile)
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

    type = xxx["testsuite"]["type"]
    version = xxx["testsuite"]["version"]
    name = xxx["testsuite"]["name"]
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
    json_report['_type'] = type
    json_report['_version'] = version
    json_report['_name'] = name
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