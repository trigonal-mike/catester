import os
import pytest
from matplotlib import pyplot as plt
from model import parse_yaml_file

def execute_file(filename, namespace):
    with open(filename, 'r') as file:
        exec(compile(file.read(), filename, 'exec'), namespace)

def pytest_addoption(parser):
    parser.addoption("--yamlfile", default="", help="please provide a valid yamlfile", )

def pytest_generate_tests(metafunc):
    yamlfile = metafunc.config.getoption('--yamlfile')
    config = parse_yaml_file(yamlfile)
    testcases = []
    for idx_main, test in enumerate(config["properties"]["tests"]):
        for idx_sub, sub_test in enumerate(test["subTests"]):
            testcases.append((idx_main, idx_sub))
    metafunc.parametrize('testcases', testcases)

@pytest.fixture
def testsuite(request):
    yamlfile = request.config.getoption('--yamlfile')
    config = parse_yaml_file(yamlfile)
    return config

@pytest.fixture
def testcase(testsuite, testcases):
    properties = testsuite["properties"]
    test_info = testsuite["testInfo"]
    student_dir = test_info["studentDirectory"]
    reference_dir = test_info["referenceDirectory"]
    idx_main, idx_sub = testcases
    tests = properties["tests"]
    main = tests[idx_main]
    sub_tests = main["subTests"]
    sub = sub_tests[idx_sub]
    return (main, sub)

@pytest.fixture(scope='function')
def monkeymodule():
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()

@pytest.fixture(scope='function')
def namespace_student(request, monkeymodule, testsuite, testcase):
    yamlfile = request.config.getoption('--yamlfile')
    dirabs = os.path.abspath(os.path.dirname(yamlfile))
    test_info = testsuite["testInfo"]
    dir = test_info["studentDirectory"]

    main, sub = testcase
    entry_point = main["entryPoint"]
    file = os.path.join(dirabs, dir, entry_point)

    monkeymodule.setattr(plt, "show", lambda: None)

    namespace = {}
    execute_file(file, namespace)
    return namespace

@pytest.fixture(scope='function')
def namespace_reference(request, monkeymodule, testsuite, testcase):
    yamlfile = request.config.getoption('--yamlfile')
    dirabs = os.path.abspath(os.path.dirname(yamlfile))
    test_info = testsuite["testInfo"]
    dir = test_info["referenceDirectory"]

    main, sub = testcase
    entry_point = main["entryPoint"]
    file = os.path.join(dirabs, dir, entry_point)

    monkeymodule.setattr(plt, "show", lambda: None)

    namespace = {}
    if os.path.exists(file):
        execute_file(file, namespace)
    return namespace
