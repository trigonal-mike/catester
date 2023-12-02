import os
import numpy as np
import pytest
from matplotlib import pyplot as plt
from catester.helpers import execute_file, parse_yaml_file
from pytest import approx

yamlfile = "I:/PYTHON/catester/examples/ex1/test.yaml"
dirabs = os.path.abspath(os.path.dirname(yamlfile))
config = parse_yaml_file(yamlfile)
properties = config["properties"]
relative_tolerance = properties["relativeTolerance"]
absolute_tolerance = properties["absoluteTolerance"]

test_info = config["testInfo"]
student_dir = test_info["studentDirectory"]
reference_dir = test_info["referenceDirectory"]

for test in properties["tests"]:
    entry_point = test["entryPoint"]
    file_student = os.path.join(dirabs, student_dir, entry_point)
    file_reference = os.path.join(dirabs, reference_dir, entry_point)

    @pytest.fixture(scope='module')
    def monkeymodule():
        from _pytest.monkeypatch import MonkeyPatch
        mpatch = MonkeyPatch()
        yield mpatch
        mpatch.undo()

    @pytest.fixture(scope='module')
    def namespace_student(monkeymodule):
        monkeymodule.setattr(plt, "show", lambda: None)
        namespace = {}
        execute_file(file_student, namespace)
        return namespace

    @pytest.fixture(scope='module')
    def namespace_reference(monkeymodule):
        monkeymodule.setattr(plt, "show", lambda: None)
        namespace = {}
        execute_file(file_reference, namespace)
        return namespace
    
    for subtest in test["subTests"]:
        var_name = subtest["name"]
        var_value = None
        var_type = None
        if "value" in subtest:
            var_value = subtest["value"] 
            var_type = type(var_value)

        def create_test_fn(name, value, v_type):
            def test_variable(namespace_student, namespace_reference):
                assert name in namespace_student, f"Variable {name} not found in the namespace_student"
                assert name in namespace_reference, f"Variable {name} not found in the namespace_reference"

                val_student = namespace_student[name]
                val_reference = namespace_reference[name]
                type_student = type(val_student)
                type_reference = type(val_reference)
                #assert isinstance(val_student, type_reference), f"Variable {name} has incorrect type"
                assert type_student == type_reference, f"Variable {name} has incorrect type"

                if isinstance(val_student, str):
                    assert val_student == val_reference, f"Variable {name} has incorrect value"
                elif isinstance(val_student, np.ndarray):
                    np.testing.assert_allclose(val_student, val_reference, relative_tolerance, absolute_tolerance), f"Variable {name} has incorrect value"
                else:
                    assert val_student == approx(val_reference, relative_tolerance, absolute_tolerance)

            return test_variable

        test_name = f"test_{test['name']}_{var_name}"
        globals()[test_name] = create_test_fn(var_name, var_value, var_type)

