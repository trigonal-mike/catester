import re
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
        allowed_occuranceRange = self.get_inherited_property("allowedOccuranceRange", ancestors, None)
        qualification = self.get_inherited_property("qualification", ancestors, None)
        testtype = self.get_inherited_property("type", ancestors, None)

        if testtype == "variable":
            name = sub["name"]
            value = sub["value"]
            evalString = sub["evalString"]
            pattern = sub["pattern"]
            countRequirement = sub["countRequirement"]
            options = sub["options"]
            verificationFunction = sub["verificationFunction"]

            assert name in namespace_student, f"Variable {name} not found in student namespace"
            val_student = namespace_student[name]

            if qualification == "verifyEqual":
                if value is not None:
                    val_reference = value
                elif evalString is not None:
                    try:
                        val_reference = eval(evalString)
                    except Exception as e:
                        raise AssertionError("Evaluation of 'evalString' not possible")
                else:
                    assert name in namespace_reference, f"Variable {name} not found in reference namespace"
                    val_reference = namespace_reference[name]
                
                type_student = type(val_student)
                type_reference = type(val_reference)
                #strict type check vs isinstance(val_student, type_reference), hmmm?
                assert type_student == type_reference, f"Variable {name} has incorrect type"
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
            elif qualification == "matches":
                #is that ok?
                assert str(val_student) == pattern, f"Variable {name} does not match specified pattern"
            elif qualification == "contains":
                assert str(val_student).find(pattern) > -1, f"Variable {name} does not contain specified pattern"
            elif qualification == "startsWith":
                assert str(val_student).startswith(pattern), f"Variable {name} does not start with specified pattern"
            elif qualification == "endsWith":
                assert str(val_student).endswith(pattern), f"Variable {name} does not end with specified pattern"
            elif qualification == "count":
                assert str(val_student).count(pattern) == countRequirement, f"Variable {name} does not contain specified pattern {countRequirement} times"
            elif qualification == "regexp":
                re_pattern = re.compile(fr'{pattern}')
                result = re.match(re_pattern, str(val_student))
                assert result is not None, f"Variable {name} does not match specified regular expression"
            elif qualification == "verification":
                pass
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
        
