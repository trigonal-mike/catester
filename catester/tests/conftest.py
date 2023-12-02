import os
from catester.helpers import execute_file, parse_yaml_file

def pytest_addoption(parser):
    parser.addoption("--yamlfile", default="", help="provide a valid yamlfile", )

#yet not working, hmmm?
"""
def pytest_configure(config):
    yamlfile = config.getoption('--yamlfile')
    dirabs = os.path.abspath(os.path.dirname(yamlfile))
    config = parse_yaml_file(yamlfile)
    properties = config["properties"]
    test_info = config["testInfo"]
    student_dir = test_info["studentDirectory"]
    reference_dir = test_info["referenceDirectory"]

    for test in properties["tests"]:
        entry_point = test["entryPoint"]
        file_student = os.path.join(dirabs, student_dir, entry_point)
        file_reference = os.path.join(dirabs, reference_dir, entry_point)
        namespace_user = {}
        namespace_reference = {}
        execute_file(file_student, namespace_user)
        execute_file(file_reference, namespace_reference)

        for subtest in test["subTests"]:
            var_name = subtest["name"]
            var_value = None
            var_type = None
            if "value" in subtest:
                var_value = subtest["value"] 
                var_type = type(var_value)

            def create_test_fn(name, value, v_type):
                def test_variable():
                    # Check if variable exists in the namespace
                    assert name in namespace_user, f"Variable {name} not found in the namespace_user"
                    assert name in namespace_reference, f"Variable {name} not found in the namespace_user"

                    # Check if variable has the correct type
                    #assert type(namespace_user[name]) == v_type, f"Variable {name} has incorrect type"
                    #assert isinstance(namespace_user[name], v_type), f"Variable {name} has incorrect type"
                    assert type(namespace_user[name]) == type(namespace_reference[name]), f"Variable {name} has incorrect type"

                    # Check if variable value matches the expected value
                    #assert namespace_user[name] == value, f"Variable {name} has incorrect value"
                    assert namespace_user[name] == namespace_reference[name], f"Variable {name} has incorrect value"

                return test_variable

            test_name = f"test_{test['name']}_{var_name}"
            globals()[test_name] = create_test_fn(var_name, var_value, var_type)
"""

