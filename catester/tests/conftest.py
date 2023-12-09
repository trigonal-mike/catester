import os
import pytest
#from matplotlib import pyplot as plt
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



"""
def execute_file(filename, namespace):
    with open(filename, "r") as file:
        exec(compile(file.read(), filename, "exec"), namespace)

@pytest.fixture(scope="function")
def testcase(config, testcases):
    idx_main, idx_sub = testcases
    main = config["testsuite"]["properties"]["tests"][idx_main]
    sub = main["tests"][idx_sub]
    return (main, sub)

@pytest.fixture(scope="function")
def namespace_student(monkeymodule, config, testcase):
    dirabs = config["abs_path_to_yaml"]
    test_info = config["testsuite"]["testInfo"]
    dir = test_info["studentDirectory"]

    main, sub = testcase
    entry_point = main["entryPoint"]
    if entry_point is not None:
        file = os.path.join(dirabs, dir, entry_point)
        monkeymodule.setattr(plt, "show", lambda: None)
        namespace = {}
        if os.path.exists(file):
            execute_file(file, namespace)
        return namespace

    return {}

@pytest.fixture(scope="function")
def namespace_reference(monkeymodule, config, testcase):
    dirabs = config["abs_path_to_yaml"]
    test_info = config["testsuite"]["testInfo"]
    dir = test_info["referenceDirectory"]

    main, sub = testcase
    entry_point = main["entryPoint"]
    if entry_point is not None:
        file = os.path.join(dirabs, dir, entry_point)
        monkeymodule.setattr(plt, "show", lambda: None)
        namespace = {}
        if os.path.exists(file):
            execute_file(file, namespace)
        return namespace

    return {}
"""
