import pytest

# Fixture function factory
def custom_fixture_factory(name):
    def custom_fixture(fixture_function):
        @pytest.fixture
        def inner_fixture():
            print(f"Running fixture {name}")
            return fixture_function()

        return inner_fixture

    return custom_fixture

# Using the custom fixture factory
@custom_fixture_factory("my_custom_fixture")
def my_fixture():
    return 42

def test_custom_fixture(my_fixture):
    assert my_fixture == 421

def test_custom_fixture(testcase):
    main, sub = testcase
    assert main == sub
