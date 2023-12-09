import glob
import os
import re
#import sys
import pytest
import numpy as np
from pandas import DataFrame, Series
from matplotlib import pyplot as plt

def execute_code(code, filename, namespace):
    exec(compile(code, filename, "exec"), namespace)

def execute_code_list(code_list, namespace):
    for code in code_list:
        execute_code(code, "", namespace)

def execute_file(filename, namespace):
    dir_old = os.getcwd()
    dir = os.path.abspath(os.path.dirname(filename))
    #sys.path.append(dir)
    os.chdir(dir)
    with open(filename, "r") as file:
        execute_code(file.read(), filename, namespace)
    os.chdir(dir_old)
    #sys.path.remove(dir)

def get_inherited_property(property, ancestors, default):
    for ancestor in ancestors:
        if property in ancestor and ancestor[property] is not None:
            return ancestor[property]
    return default

def get_solution(mm, conf, id, main, where):
    if not "solutions" in globals():
        globals()["solutions"] = {}
    if not id in globals()["solutions"]:
        globals()["solutions"][id] = {}
    if not where in globals()["solutions"][id]:
        entry_point = main["entryPoint"]
        setup_code = main["setUpCode"]
        teardown_code = main["tearDownCode"]
        setup_code_dependency = main["setUpCodeDependency"]
        namespace = {}
        if setup_code_dependency is not None:
            try:
                namespace = globals()["solutions"][setup_code_dependency][where]
            except Exception as e:
                print(f"Exception: setUpCodeDependency {setup_code_dependency} not found")
                print(e)
                raise
        if setup_code is not None:
            if isinstance(setup_code, str):
                setup_code = [setup_code]            
            execute_code_list(setup_code, namespace)
        if entry_point is not None:
            dirabs = conf["abs_path_to_yaml"]
            test_info = conf["testsuite"]["testInfo"]
            dir = test_info[f"{where}Directory"]
            file = os.path.join(dirabs, dir, entry_point)
            if os.path.exists(file):
                #mm.setattr(plt, "show", lambda: None)
                execute_file(file, namespace)
        globals()["solutions"][id][where] = namespace
    return globals()["solutions"][id][where]

class CodeabilityTestSuite:
    @classmethod
    def setup_class(cls):
        print("setup_class")

    @classmethod
    def teardown_class(cls):
        print("teardown_class")

    def setup_method(self, test_method):
        print("setup_method")

    def teardown_method(self, test_method):
        print("teardown_method")

    def test_entrypoint(self, monkeymodule, config, testcases):
        idx_main, idx_sub = testcases
        main = config["testsuite"]["properties"]["tests"][idx_main]
        sub = main["tests"][idx_sub]
        id = main["id"] if main["id"] is not None else str(idx_main)

        solution_student = get_solution(monkeymodule, config, id, main, "student")
        solution_reference = get_solution(monkeymodule, config, id, main, "reference")
        
        ancestors = [sub, main, config["testsuite"]["properties"]]

        relative_tolerance = get_inherited_property("relativeTolerance", ancestors, 0)
        absolute_tolerance = get_inherited_property("absoluteTolerance", ancestors, 0)
        allowed_occuranceRange = get_inherited_property("allowedOccuranceRange", ancestors, None)
        qualification = get_inherited_property("qualification", ancestors, None)
        testtype = get_inherited_property("type", ancestors, None)

        file = main["file"]

        name = sub["name"]
        value = sub["value"]
        evalString = sub["evalString"]
        pattern = sub["pattern"]
        countRequirement = sub["countRequirement"]
        options = sub["options"]
        verificationFunction = sub["verificationFunction"]

        if testtype == "variable":
            assert name in solution_student, f"Variable {name} not found in student namespace"
            val_student = solution_student[name]

            if qualification == "verifyEqual":
                if value is not None:
                    val_reference = value
                elif evalString is not None:
                    try:
                        val_reference = eval(evalString)
                    except Exception as e:
                        raise AssertionError("Evaluation of 'evalString' not possible")
                else:
                    assert name in solution_reference, f"Variable {name} not found in reference namespace"
                    val_reference = solution_reference[name]
                
                type_student = type(val_student)
                type_reference = type(val_reference)
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
                    assert val_student == pytest.approx(val_reference, rel=relative_tolerance, abs=absolute_tolerance), failure_msg
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
                result = re.match(re.compile(fr"{pattern}"), str(val_student))
                assert result is not None, f"Variable {name} does not match specified regular expression"
            elif qualification == "verification":
                pass
        elif testtype == "graphics":

            figure_student = solution_student["plt"].gcf()
            figure_reference = solution_reference["plt"].gcf()

            #name = sub["name"]
            #val_reference = eval(name, solution_reference)

            print(figure_student)
            print(figure_reference)
            assert figure_student == figure_reference, "ERROR ::: "
        elif testtype == "structural":
            pass
        elif testtype == "linting":
            pass
        elif testtype == "exist":
            test_info = config["testsuite"]["testInfo"]
            dirabs = config["abs_path_to_yaml"]
            dir_reference = os.path.join(dirabs, test_info["referenceDirectory"])
            dir_student = os.path.join(dirabs, test_info["studentDirectory"])
            assert len(glob.glob(file, root_dir=dir_reference)) > 0, f"File with pattern {file} not found in reference namespace"
            assert len(glob.glob(file, root_dir=dir_student)) > 0, f"File with pattern {file} not found in student namespace"
        elif testtype == "error":
            pass
        elif testtype == "warning":
            pass
        elif testtype == "help":
            pass
        else:
            raise KeyError
        
