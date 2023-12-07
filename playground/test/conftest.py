import random
import pytest

"""
def pytest_generate_tests(metafunc):
    testcases = []
    for idx_main in range(5):
        for idx_sub in range(random.randint(1, 5)):
            testcases.append((idx_main, idx_sub))
    metafunc.parametrize("testcases", testcases)

@pytest.fixture(scope="function")
def testcase(testcases):
    idx_main, idx_sub = testcases
    main = f"main-{idx_main}"
    sub = f"main-{idx_main}-sub-{idx_sub}"
    return (main, sub)
"""


def custom_fixture_factory(name):
    testcases = []
    for idx_main in range(5):
        for idx_sub in range(random.randint(1, 5)):
            testcases.append((idx_main, idx_sub))

    def custom_fixture(fixture_function):
        @pytest.fixture(params=testcases)
        def inner_fixture(request):
            #idx_main, idx_sub = request.param.testcases
            print(request.param)
            print(f"Running fixture {name} {idx_main} {idx_sub}")
            return fixture_function()

        return inner_fixture

    return custom_fixture

# Using the custom fixture factory
@custom_fixture_factory("my_custom_fixture")
def testcase():
    main = f"main"
    sub = f"main-sub"
    return (main, sub)
