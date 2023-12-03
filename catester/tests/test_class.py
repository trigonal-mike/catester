import numpy as np
from pandas import DataFrame, Series
from pytest import approx

class Test:
    def setup_method(self, test_method):
        print("setup_method")
        print(test_method)

    def teardown_method(self, test_method):
        print("teardown_method")
        print(test_method)

    def get_inherited_property(self, property, ancestors, default):
        for ancestor in ancestors:
            if property in ancestor and ancestor[property] is not None:
                return ancestor[property]
        return default

    def test_entrypoint(self, testsuite, testcase, namespace_student, namespace_reference):
        main, sub = testcase
        ancestors = [sub, main, testsuite["properties"]]
        relative_tolerance = self.get_inherited_property("relativeTolerance", ancestors, None)
        absolute_tolerance = self.get_inherited_property("absoluteTolerance", ancestors, None)
        qualification = self.get_inherited_property("qualification", ancestors, None)
        testtype = main["type"]
        if testtype == "variable":
            name = sub["name"]
            assert name in namespace_student, f"Variable {name} not found in the namespace_student"
            assert name in namespace_reference, f"Variable {name} not found in the namespace_reference"
            val_student = namespace_student[name]
            val_reference = namespace_reference[name]
            type_student = type(val_student)
            type_reference = type(val_reference)
            #strict type check vs isinstance
            #assert isinstance(val_student, type_reference), f"Variable {name} has incorrect type"
            assert type_student == type_reference, f"Variable {name} has incorrect type"

            #check for equality for different types
            failure_msg = f"Variable {name} has incorrect value"
            if isinstance(val_student, (str, set, frozenset)):
                assert val_student == val_reference, failure_msg
            elif isinstance(val_student, (DataFrame, Series)):
                assert val_student.equals(val_reference), failure_msg
            elif isinstance(val_student, np.ndarray):
                try:
                    np.testing.assert_allclose(val_student, val_reference, rtol=relative_tolerance, atol=absolute_tolerance)
                except AssertionError as e:
                    raise AssertionError(failure_msg)
            else:
                assert val_student == approx(val_reference, rel=relative_tolerance, abs=absolute_tolerance), failure_msg
        elif testtype == "graphics":
            pass
        elif testtype == "structural":
            pass
        elif testtype == "linting":
            pass
        elif testtype == "exist":
            pass
        elif testtype == "error":
            pass
        elif testtype == "warning":
            pass
        elif testtype == "help":
            pass
        else:
            raise KeyError
        
