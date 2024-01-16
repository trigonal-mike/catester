import glob
import os
import re
import sys
import time
import pytest
import numpy as np
from pandas import DataFrame, Series
from matplotlib import pyplot as plt
import random
from enum import Enum

from model import CodeAbilitySpecification, CodeAbilityTestSuite, CodeAbilityTestCollection, CodeAbilityTest
from .conftest import testsuite_key
from .conftest import specification_key
from .conftest import report_key
from .conftest import TestResult

class Solution(str, Enum):
    student = "student"
    reference = "reference"

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
        if hasattr(ancestor, property):
            x = getattr(ancestor, property)
            if x is not None:
                return x
    return default

def get_property_as_list(property_name):
    if property_name is None:
        return []
    if isinstance(property_name, str):
        return [property_name]
    return property_name

def check_success_dependency(report, success_dependencies):
    success_dependencies = get_property_as_list(success_dependencies)
    for dependency in success_dependencies:
        #todo: search for id first, then check as idx => check also if idx not out of bounds
        main_idx = int(dependency)
        total = report["tests"][main_idx]["summary"]["total"]
        for sub_idx in range(total):
            result = report["tests"][main_idx]["tests"][sub_idx]["result"]
            if result != TestResult.passed:
                return False
    return True

def get_solution(mm, specification: CodeAbilitySpecification, id, main: CodeAbilityTestCollection, where: Solution, store_graphics):
    """Calculate solution if not yet exists"""
    exec_time = 0
    if not "solutions" in globals():
        globals()["solutions"] = {}
    if not id in globals()["solutions"]:
        globals()["solutions"][id] = {}
    if not where in globals()["solutions"][id]:
        test_info = specification.testInfo
        test_directory = test_info.testDirectory
        artefact_directory = test_info.artefactDirectory
        _dir = test_info.studentDirectory if where == Solution.student else test_info.referenceDirectory

        type = main.type
        entry_point = main.entryPoint
        setup_code = get_property_as_list(main.setUpCode)
        teardown_code = get_property_as_list(main.tearDownCode)
        setup_code_dependency = main.setUpCodeDependency

        """ remember old working directory """
        dir_old = os.getcwd()

        """ add test-directory to paths """
        sys.path.append(test_directory)

        """ change into solution-directory student | reference """
        os.chdir(_dir)

        """ close all open figures """
        plt.close("all")

        """ seed the random generator """
        random.seed(1)

        """ Override/Disable certain methods """ 
        #mm.setattr(random, "seed", lambda *x: None)
        #mm.setattr(os, "getcwd", lambda: "xxx")
        #mm.setattr(time, "sleep", lambda x: None)
        #mm.setattr(time, "time", lambda: 999)
        mm.setattr(plt, "show", lambda *x: None)

        """ start solution with empty namespace """
        namespace = {}

        if setup_code_dependency is not None:
            """ start solution with prior solution """
            try:
                namespace = globals()["solutions"][setup_code_dependency][where]
            except Exception as e:
                print(f"Exception: setUpCodeDependency {setup_code_dependency} not found")
                print(e)
                raise

        if entry_point is not None:
            """ try execute the solution """
            file = os.path.join(_dir, entry_point)
            if not os.path.exists(file):
                if where == Solution.student:
                    """ only raise if student entry point is not found """
                    raise FileNotFoundError(f"entryPoint {entry_point} not found")
            else:
                """ measure execution time """
                start_time = time.time()
                #otherwise time gets converted to zero, hmmm?
                time.sleep(0.00000001)
                try:
                    execute_file(file, namespace)
                except Exception as e:
                    print(f"Exception: execute_file {file} failed")
                    print(e)
                    raise
                exec_time = time.time() - start_time
                if type == "graphics":
                    if store_graphics:
                        fignums = plt.get_fignums()
                        for i in fignums:
                            file_name = f"{where}_test_{id}_figure_{i}.png"
                            abs_file_name = os.path.join(artefact_directory, file_name)
                            figure = plt.figure(i)
                            figure.savefig(abs_file_name)

                    # extract variable data from graphics object and store them in the respective namespace
                    # for later use when the subTests are run
                    # supported are qualified strings which can be evaluated
                    namespace["_graphics_object_"] = {}
                    for sub_test in main.tests:
                        name = sub_test.name
                        fun2eval = f'globals()["plt"].{name}'
                        value = eval(fun2eval)
                        namespace["_graphics_object_"][name] = value

        """ run setup-code """
        execute_code_list(setup_code, namespace)

        """ run teardown-code """
        execute_code_list(teardown_code, namespace)

        """ close all open figures """
        plt.close("all")

        """ change back to where we were before """
        os.chdir(dir_old)

        """ remove test-directory from paths """
        sys.path.remove(test_directory)

        globals()["solutions"][id][where] = namespace
    return globals()["solutions"][id][where], exec_time

class CodeabilityPythonTest:
    """ this class gets tested """
    # hooks for setup/teardown
    # currently not used
    # teardown also possible with fixtures and code after yield statement (see conftest.py)
    @classmethod
    def setup_class(cls):
        pass
        #print("setup_class")

    @classmethod
    def teardown_class(cls):
        pass
        #print("teardown_class")

    # these are called for each invocation of test_entrypoint
    def setup_method(self, test_method):
        pass
        #print("setup_method")

    def teardown_method(self, test_method):
        pass
        #print("teardown_method")

    # testcases get parametrized in conftest.py (pytest_generate_tests)
    def test_entrypoint(self, request, record_property, monkeymodule, testcases):
        idx_main, idx_sub = testcases

        report: any = request.config.stash[report_key]
        testsuite: CodeAbilityTestSuite = request.config.stash[testsuite_key]
        specification: CodeAbilitySpecification = request.config.stash[specification_key]

        main: CodeAbilityTestCollection = testsuite.properties.tests[idx_main]
        sub: CodeAbilityTest = main.tests[idx_sub]

        if not check_success_dependency(report, main.successDependency):
            #raise TimeoutError(f"Dependency {main.successDependency} not satisfied")
            #raise LookupError(f"Dependency {main.successDependency} not satisfied")
            #raise RuntimeWarning(f"Dependency {main.successDependency} not satisfied")
            pytest.skip(f"Dependency {main.successDependency} not satisfied")

        dir_reference = specification.testInfo.referenceDirectory
        dir_student = specification.testInfo.studentDirectory

        testtype = main.type
        file = main.file
        id = main.id if main.id is not None else str(idx_main + 1)

        name = sub.name
        value = sub.value
        evalString = sub.evalString
        pattern = sub.pattern
        countRequirement = sub.countRequirement
        #options = sub.options
        #verificationFunction = sub.verificationFunction

        ancestors_sub = [sub, main, testsuite.properties]
        ancestors_main = [main, testsuite.properties]

        qualification = get_inherited_property("qualification", ancestors_sub, None)
        relative_tolerance = get_inherited_property("relativeTolerance", ancestors_sub, 0)
        absolute_tolerance = get_inherited_property("absoluteTolerance", ancestors_sub, 0)
        allowed_occuranceRange = get_inherited_property("allowedOccuranceRange", ancestors_sub, None)
        store_graphics_artefacts = get_inherited_property("storeGraphicsArtefacts", ancestors_main, False)

        #not needed here:
        #failure_message = get_inherited_property("failureMessage", ancestors_sub, None)
        #success_message = get_inherited_property("successMessage", ancestors_sub, None)
        #verbosity = get_inherited_property("verbosity", ancestors_sub, None)
        #competency = get_inherited_property("competency", ancestors_main, None)

        # Get student solution, measure execution time
        solution_reference, exec_time_reference = get_solution(monkeymodule, specification, id, main, Solution.reference, store_graphics_artefacts)
        record_property("exec_time_reference", exec_time_reference)
        solution_student, exec_time_student = get_solution(monkeymodule, specification, id, main, Solution.student, store_graphics_artefacts)
        record_property("exec_time_student", exec_time_student)

        # if test is graphics => get saved graphics object as solution
        if testtype == "graphics":
            solution_student = solution_student["_graphics_object_"]
            solution_reference = solution_reference["_graphics_object_"]

        if testtype in ["variable", "graphics", "error", "warning", "help"]:
            # student value
            if name in solution_student:
                val_student = solution_student[name]
            else:
                # value not found, try eval
                try:
                    val_student = eval(name, solution_student)
                except Exception as e:
                    raise AssertionError(f"Variable {name} not found in student namespace")

            if qualification == "verifyEqual":
                # reference value
                if value is not None:
                    val_reference = value
                elif evalString is not None:
                    try:
                        val_reference = eval(evalString)
                    except Exception as e:
                        pytest.skip(reason="Evaluation of 'evalString' not possible")
                else:
                    if name in solution_reference:
                        val_reference = solution_reference[name]
                    else:
                        try:
                            val_reference = eval(name, solution_reference)
                        except Exception as e:
                            raise AssertionError(f"Variable {name} not found in reference namespace")
                
                type_student = type(val_student)
                type_reference = type(val_reference)
                assert type_student == type_reference, f"Variable {name} has incorrect type, expected: {type_reference}, obtained {type_student}"

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
                    """attention: pytest.approx() does not support nested data structures, like: 'var7 = [[1, 22, 44]]' """
                    assert val_student == pytest.approx(val_reference, rel=relative_tolerance, abs=absolute_tolerance), failure_msg
            elif qualification == "matches":
                assert str(val_student) == pattern, f"Variable {name} does not match the specified pattern {pattern}"
            elif qualification == "contains":
                assert str(val_student).find(pattern) > -1, f"Variable {name} does not contain the specified pattern {pattern}"
            elif qualification == "startsWith":
                assert str(val_student).startswith(pattern), f"Variable {name} does not start with the specified pattern {pattern}"
            elif qualification == "endsWith":
                assert str(val_student).endswith(pattern), f"Variable {name} does not end with the specified pattern {pattern}"
            elif qualification == "count":
                assert str(val_student).count(pattern) == countRequirement, f"Variable {name} does not contain the specified pattern {pattern} {countRequirement}-times"
            elif qualification == "regexp":
                result = re.match(re.compile(fr"{pattern}"), str(val_student))
                assert result is not None, f"Variable {name} does not match the compiled regular expression from the specified pattern {pattern}"
            elif qualification == "verification":
                # not implemented yet
                pass
        elif testtype == "structural":
            # not implemented yet
            pass
        elif testtype == "linting":
            # not implemented yet
            pass
        elif testtype == "exist":
            assert len(glob.glob(file, root_dir=dir_reference)) > 0, f"File with pattern {file} not found in reference namespace"
            assert len(glob.glob(file, root_dir=dir_student)) > 0, f"File with pattern {file} not found in student namespace"
        else:
            # this should not happen anyway
            raise KeyError

