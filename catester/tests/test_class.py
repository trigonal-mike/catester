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
    with open(filename, "r") as file:
        execute_code(file.read(), filename, namespace)

def get_inherited_property(property, ancestors, default):
    for ancestor in ancestors:
        if property in ancestor and ancestor[property] is not None:
            return ancestor[property]
    return default

def get_property_as_list(main, property_name):
    property = main[property_name]
    if property is None:
        return []
    if isinstance(property, str):
        property = [property]
    return property

def get_solution(mm, conf, id, main, where):
    # calculate solution, only if not already exists
    if not "solutions" in globals():
        globals()["solutions"] = {}
    if not id in globals()["solutions"]:
        globals()["solutions"][id] = {}
    if not where in globals()["solutions"][id]:
        dirabs = conf["abs_path_to_yaml"]
        test_suite = conf["testsuite"]
        store_graphics_artefacts = test_suite["storeGraphicsArtefacts"]
        dir = test_suite["testInfo"][f"{where}Directory"]
        artefact_directory = test_suite["testInfo"]["artefactDirectory"]
        # create all non-existing directories like in CodeAbilityTestSuite.m L221

        type = main["type"]
        entry_point = main["entryPoint"]
        setup_code = get_property_as_list(main, "setUpCode")
        teardown_code = get_property_as_list(main, "tearDownCode")
        setup_code_dependency = main["setUpCodeDependency"]

        abs_dir = os.path.join(dirabs, dir)

        # remember old working directory
        dir_old = os.getcwd()
        #sys.path.append(abs_dir)
        os.chdir(abs_dir)
        plt.close("all")

        # start solution with empty namespace
        namespace = {}

        if setup_code_dependency is not None:
            # start solution with prior solution
            try:
                namespace = globals()["solutions"][setup_code_dependency][where]
            except Exception as e:
                print(f"Exception: setUpCodeDependency {setup_code_dependency} not found")
                print(e)
                raise

        # run setup code anyway,
        # or like Winfried did in CodeAbilityTest.m L123 if setup_code_dependency is None
        execute_code_list(setup_code, namespace)

        if entry_point is not None:
            file = os.path.join(dirabs, dir, entry_point)
            if not os.path.exists(file):
                raise FileNotFoundError(f"entryPoint {entry_point} not found")

            # disable plt.show() command, otherwise figure gets destroyed afterwards
            mm.setattr(plt, "show", lambda: None)
            execute_file(file, namespace)
            if type == "graphics":
                if store_graphics_artefacts:
                    fignums = plt.get_fignums()
                    for i in fignums:
                        file_name = f"{where}_test_{id}_figure_{i}.png"
                        abs_file_name = os.path.join(dirabs, artefact_directory, file_name)
                        figure = plt.figure(i)
                        figure.savefig(abs_file_name)

                # extract variable data from graphics object
                # these variables are being stored in the respective namespace
                # for later use when the subTests are run
                # splitObject() like in CodeAbilityTestTemplate.m L57 is not implemented (yet)
                # supported are qualified strings which can be evaluated
                namespace["_graphics_object_"] = {}
                for sub_test in main["tests"]:
                    name = sub_test["name"]
                    fun2eval = f'globals()["plt"].{name}'
                    value = eval(fun2eval)
                    namespace["_graphics_object_"][name] = value

        # run teardown code
        execute_code_list(teardown_code, namespace)

        # change back to where we were before
        #sys.path.remove(abs_dir)
        os.chdir(dir_old)
        plt.close("all")

        globals()["solutions"][id][where] = namespace
    return globals()["solutions"][id][where]

class CodeabilityTestSuite:
    # hooks for setup/teardown
    # currently not used
    # teardown also possible with fixtures and code after yield statement (see conftest.py)
    @classmethod
    def setup_class(cls):
        print("setup_class")

    @classmethod
    def teardown_class(cls):
        print("teardown_class")

    # these are called for each invocation of test_entrypoint
    def setup_method(self, test_method):
        print("setup_method")

    def teardown_method(self, test_method):
        print("teardown_method")

    # testcases get parametrized in conftest.py (pytest_generate_tests)
    def test_entrypoint(self, monkeymodule, config, testcases):
        idx_main, idx_sub = testcases
        main = config["testsuite"]["properties"]["tests"][idx_main]
        sub = main["tests"][idx_sub]
        id = main["id"] if main["id"] is not None else str(idx_main + 1)

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

        if testtype == "graphics":
            solution_student = solution_student["_graphics_object_"]
            solution_reference = solution_reference["_graphics_object_"]

        if testtype in ["variable", "graphics", "error", "warning", "help"]:
            assert name in solution_student, f"Variable {name} not found in student namespace"
            val_student = solution_student[name]

            # get reference value
            if qualification == "verifyEqual":
                if value is not None:
                    val_reference = value
                elif evalString is not None:
                    try:
                        val_reference = eval(evalString)
                    except Exception as e:
                        pytest.skip()
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
                # is that ok?
                # what are the differences between "matches", string compare ("verifyEqual") and "regexp"?
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
        elif testtype == "structural":
            # not implemented yet
            pass
        elif testtype == "linting":
            # not implemented yet
            pass
        elif testtype == "exist":
            test_info = config["testsuite"]["testInfo"]
            dirabs = config["abs_path_to_yaml"]
            dir_reference = os.path.join(dirabs, test_info["referenceDirectory"])
            dir_student = os.path.join(dirabs, test_info["studentDirectory"])
            assert len(glob.glob(file, root_dir=dir_reference)) > 0, f"File with pattern {file} not found in reference namespace"
            assert len(glob.glob(file, root_dir=dir_student)) > 0, f"File with pattern {file} not found in student namespace"
        else:
            raise KeyError

