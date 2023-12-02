import os
import yaml
import pytest
from matplotlib import pyplot as plt

def parse_test_suite(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

config_data = parse_test_suite('tests.yaml')

def execute_file(filename, namespace):
    with open(filename, 'r') as file:
        exec(compile(file.read(), filename, 'exec'), namespace)


@pytest.fixture(scope='module')
def monkeymodule():
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()

@pytest.fixture(scope='module')
def namespace_user(monkeymodule):
    monkeymodule.setattr(plt, "show", lambda: None)
    namespace = {}
    execute_file(config_data["entryPoint"], namespace)
    return namespace

for test_data in config_data["tests"]:
    for var_data in test_data["variables"]:
        var_name = var_data["name"]
        var_value = var_data["value"]
        var_type = type(var_value)

        def create_test_fn(name, value, v_type):
            def test_variable(namespace_user):
                # Check if variable exists in the namespace
                assert name in namespace_user, f"Variable {name} not found in the namespace"

                # Check if variable has the correct type
                assert type(namespace_user[name]) == v_type, f"Variable {name} has incorrect type"
                #assert isinstance(namespace_user[name], v_type), f"Variable {name} has incorrect type"

                # Check if variable value matches the expected value
                assert namespace_user[name] == value, f"Variable {name} has incorrect value"

            return test_variable

        test_name = f"test_{test_data['name']}_{var_name}"
        globals()[test_name] = create_test_fn(var_name, var_value, var_type)

