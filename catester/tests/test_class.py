import glob
import os
import re
import sys
import time
import pytest
import random
import numpy as np
from pandas import DataFrame, Series
from matplotlib import pyplot as plt
from enum import Enum

from model import CodeAbilitySpecification, CodeAbilityTestSuite
from model import CodeAbilityTestCollection, CodeAbilityTest
from model import TypeEnum, QualificationEnum
from .conftest import report_key, TestResult
from .execution import execute_code_list, execute_file

class Solution(str, Enum):
    student = "student"
    reference = "reference"

def get_property_as_list(property_name):
    if property_name is None:
        return []
    if not isinstance(property_name, list):
        return [property_name]
    return property_name

def main_idx_by_dependency(testsuite: CodeAbilityTestSuite, dependency):
    for idx_main, main in enumerate(testsuite.properties.tests):
        if main.id is not None and dependency == main.id:
            return idx_main
    try:
        idx = int(dependency)
        if idx <= 0 or idx >= len(testsuite.properties.tests):
            raise
        return idx - 1
    except Exception as e:
        pytest.fail(f"Dependency {dependency} not found!!!")

def get_solution(mm, request, idx_main, where: Solution):
    """Calculate solution if not yet exists"""
    _report = request.config.stash[report_key]
    testsuite: CodeAbilityTestSuite = _report["testsuite"]
    specification: CodeAbilitySpecification = _report["specification"]
    main: CodeAbilityTestCollection = testsuite.properties.tests[idx_main]
    id = str(idx_main)

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
        store_graphics_artefacts = main.storeGraphicsArtefacts
        timeout = main.timeout

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
            scd_idx = main_idx_by_dependency(testsuite, setup_code_dependency)
            ss = str(scd_idx)
            """ start solution with prior solution """
            try:
                namespace = globals()["solutions"][ss][where]
            except Exception as e:
                print(f"Exception: setUpCodeDependency {ss} not found")
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
                try:
                    result = execute_file(file, namespace, timeout=timeout)
                    if result is None:
                        print(f"TimeoutError: execute_file {file} failed")
                        raise TimeoutError()
                except Exception as e:
                    print(f"Exception: execute_file {file} failed")
                    #print(e)
                    raise

                #without follwing line, exec_time gets converted to zero, hmmm?
                time.sleep(0.00000001)

                exec_time = time.time() - start_time
                if type == "graphics":
                    if store_graphics_artefacts:
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

def check_success_dependency(request, idx_main):
    _report = request.config.stash[report_key]
    report: any = _report["report"]
    testsuite: CodeAbilityTestSuite = _report["testsuite"]
    main: CodeAbilityTestCollection = testsuite.properties.tests[idx_main]
    success_dependencies = get_property_as_list(main.successDependency)
    for dependency in success_dependencies:
        main_idx = main_idx_by_dependency(testsuite, dependency)
        total = report["tests"][main_idx]["summary"]["total"]
        for sub_idx in range(total):
            result = report["tests"][main_idx]["tests"][sub_idx]["result"]
            if result != TestResult.passed:
                pytest.skip(f"Dependency {success_dependencies} not satisfied")

class CodeabilityPythonTest:
    # testcases get parametrized in conftest.py (pytest_generate_tests)
    def test_entrypoint(self, request, record_property, monkeymodule, testcases):
        idx_main, idx_sub = testcases

        check_success_dependency(request, idx_main)

        _report = request.config.stash[report_key]
        testsuite: CodeAbilityTestSuite = _report["testsuite"]
        specification: CodeAbilitySpecification = _report["specification"]
        main: CodeAbilityTestCollection = testsuite.properties.tests[idx_main]
        sub: CodeAbilityTest = main.tests[idx_sub]

        dir_reference = specification.testInfo.referenceDirectory
        dir_student = specification.testInfo.studentDirectory

        testtype = main.type
        file = main.file

        name = sub.name
        value = sub.value
        evalString = sub.evalString
        pattern = sub.pattern
        countRequirement = sub.countRequirement
        qualification = sub.qualification
        relative_tolerance = sub.relativeTolerance
        absolute_tolerance = sub.absoluteTolerance
        allowed_occuranceRange = sub.allowedOccuranceRange

        """ Get solutions, measure execution time """
        try:
            solution_student, exec_time_student = get_solution(monkeymodule, request, idx_main, Solution.student)
            record_property("exec_time_student", exec_time_student)
            solution_reference, exec_time_reference = get_solution(monkeymodule, request, idx_main, Solution.reference)
            record_property("exec_time_reference", exec_time_reference)
        except TimeoutError as e:
            record_property("timeout", True)
            raise

        """ if test is graphics => get saved graphics object as solution """
        if testtype == TypeEnum.graphics:
            solution_student = solution_student["_graphics_object_"]
            solution_reference = solution_reference["_graphics_object_"]

        if testtype in [
            TypeEnum.variable,
            TypeEnum.graphics,
            TypeEnum.error,
            TypeEnum.warning,
            TypeEnum.help,
        ]:
            """ get the student value """
            if name in solution_student:
                val_student = solution_student[name]
            else:
                """ value not found, try eval """
                try:
                    val_student = eval(name, solution_student)
                except Exception as e:
                    raise AssertionError(f"Variable {name} not found in student namespace")

            if qualification == QualificationEnum.verifyEqual:
                """ get the reference value """
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
                
                """ assert variable-type """
                type_student = type(val_student)
                type_reference = type(val_reference)
                assert type_student == type_reference, f"Variable {name} has incorrect type, expected: {type_reference}, obtained {type_student}"

                """ assert variable-value """
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
            elif qualification == QualificationEnum.matches:
                assert str(val_student) == pattern, f"Variable {name} does not match the specified pattern {pattern}"
            elif qualification == QualificationEnum.c:
                assert str(val_student).find(pattern) > -1, f"Variable {name} does not contain the specified pattern {pattern}"
            elif qualification == QualificationEnum.startsWith:
                assert str(val_student).startswith(pattern), f"Variable {name} does not start with the specified pattern {pattern}"
            elif qualification == QualificationEnum.endsWith:
                assert str(val_student).endswith(pattern), f"Variable {name} does not end with the specified pattern {pattern}"
            elif qualification == QualificationEnum.count:
                assert str(val_student).count(pattern) == countRequirement, f"Variable {name} does not contain the specified pattern {pattern} {countRequirement}-times"
            elif qualification == QualificationEnum.regexp:
                result = re.match(re.compile(fr"{pattern}"), str(val_student))
                assert result is not None, f"Variable {name} does not match the compiled regular expression from the specified pattern {pattern}"
            elif qualification == QualificationEnum.verification:
                # not implemented yet
                pass
        elif testtype == TypeEnum.structural:
            # not implemented yet
            pass
        elif testtype == TypeEnum.linting:
            # not implemented yet
            pass
        elif testtype == TypeEnum.exist:
            assert len(glob.glob(file, root_dir=dir_reference)) > 0, f"File with pattern {file} not found in reference namespace"
            assert len(glob.glob(file, root_dir=dir_student)) > 0, f"File with pattern {file} not found in student namespace"
        else:
            # this should not happen anyway
            raise KeyError

