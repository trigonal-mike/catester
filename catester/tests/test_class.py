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
import traceback
from model import CodeAbilitySpecification, CodeAbilityTestSuite
from model import CodeAbilityTestCollection, CodeAbilityTest
from model import TypeEnum, QualificationEnum
from .conftest import report_key, TestResult, TestStatus, Solution
from .execution import execute_code_list, execute_file

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
        if idx > 0 and idx <= len(testsuite.properties.tests):
            return idx - 1
    except Exception:
        pass

def get_solution(mm, pytestconfig, idx_main, where: Solution):
    """ Calculate solution if not yet exists """
    _report = pytestconfig.stash[report_key]
    solutions: any = _report["solutions"]
    report: any = _report["report"]
    testsuite: CodeAbilityTestSuite = _report["testsuite"]
    specification: CodeAbilitySpecification = _report["specification"]
    main: CodeAbilityTestCollection = testsuite.properties.tests[idx_main]
    id = str(idx_main)

    if not id in solutions:
        solutions[id] = {}
    if not where in solutions[id]:
        solutions[id][where] = {
            "namespace": {},
            "timestamp": time.time(),
            "status": TestStatus.scheduled,
            "errormsg": "",
            "exectime": 0,
            "traceback": {},
        }
        _solution = solutions[id][where]
        _dir = specification.studentDirectory if where == Solution.student else specification.referenceDirectory
        entry_point = main.entryPoint
        timeout = main.timeout
        setup_code = get_property_as_list(main.setUpCode)
        teardown_code = get_property_as_list(main.tearDownCode)
        success_dependencies = get_property_as_list(main.successDependency)
        setup_code_dependency = main.setUpCodeDependency
        store_graphics_artifacts = main.storeGraphicsArtifacts
        if specification.storeGraphicsArtifacts is not None:
            store_graphics_artifacts = specification.storeGraphicsArtifacts

        """ start solution with empty namespace """
        namespace = {}
        error = False
        errormsg = ""
        status = TestStatus.scheduled
        tb = {}
        exectime = 0

        """ check success dependencies, mark as skipped if not satisfied """
        for dependency in success_dependencies:
            _idx = main_idx_by_dependency(testsuite, dependency)
            if _idx is None:
                error = True
                errormsg = f"Success-Dependency `{success_dependencies}` not valid"
                status = TestStatus.failed
            else:
                total = report["tests"][_idx]["summary"]["total"]
                for sub_idx in range(total):
                    result = report["tests"][_idx]["tests"][sub_idx]["result"]
                    if result != TestResult.passed:
                        error = True
                        errormsg = f"Success-Dependency `{success_dependencies}` not satisfied"
                        status = TestStatus.skipped
                        break
            if error:
                break

        if setup_code_dependency is not None and not error:
            _idx = main_idx_by_dependency(testsuite, setup_code_dependency)
            if _idx is None:
                error = True
                errormsg = f"Setup-Code-Dependency `{setup_code_dependency}` not valid"
                status = TestStatus.failed
            else:
                try:
                    namespace = solutions[str(_idx)][where]["namespace"]
                except Exception as e:
                    error = True
                    errormsg = f"ERROR: Setup-Code-Dependency `{setup_code_dependency}` not found"
                    status = TestStatus.failed

        """ remember old working directory """
        dir_old = os.getcwd()

        """ add test-directory to paths """
        #todo: test if this works
        sys.path.append(specification.testDirectory)

        """ change into solution-directory student | reference """
        os.chdir(_dir)

        """ close all open figures """
        plt.close("all")

        """ seed the random generator """
        random.seed(1)

        """ Override/Disable certain methods """ 
        mm.setattr(plt, "show", lambda *x: None)

        if entry_point is not None and not error:
            file = os.path.join(_dir, entry_point)
            if not os.path.exists(file):
                if where == Solution.student:
                    error = True
                    errormsg = f"entryPoint {entry_point} not found"
                    status = TestStatus.failed
            else:
                try:
                    start_time = time.time()
                    result = execute_file(file, namespace, timeout=timeout)
                    time.sleep(0.0001)
                    exectime = time.time() - start_time
                    if result is None:
                        error = True
                        errormsg = f"Maximum execution time of {timeout} seconds exceeded"
                        status = TestStatus.timedout
                    else:
                        status = TestStatus.completed
                except Exception as e:
                    error = True
                    errormsg = f"Execution of {file} failed"
                    status = TestStatus.crashed
                    tb1 = traceback.extract_tb(e.__traceback__)
                    tb2 = tb1[len(tb1)-1]
                    tb = {
                        "name": tb2.name,
                        "filename": tb2.filename,
                        "lineno": tb2.lineno,
                        "line": tb2.line,
                        "locals": tb2.locals,
                        "errormsg": e,
                    }
                if not error and main.type == "graphics":
                    if store_graphics_artifacts:
                        fignums = plt.get_fignums()
                        for i in fignums:
                            file_name = f"{where}_test_{id}_figure_{i}.png"
                            abs_file_name = os.path.join(specification.artifactDirectory, file_name)
                            figure = plt.figure(i)
                            figure.savefig(abs_file_name)

                    # extract variable data from graphics object and store them in the respective namespace
                    # for later use when the subTests are run
                    # supported are qualified strings which can be evaluated
                    namespace["_graphics_object_"] = {}
                    for sub_test in main.tests:
                        name = sub_test.name
                        fun2eval = f"globals()['plt'].{name}"
                        try:
                            namespace["_graphics_object_"][name] = eval(fun2eval)
                        except:
                            #todo:
                            pass

        if not error:
            try:
                """ run setup-code """
                execute_code_list(setup_code, namespace)
            except:
                error = True
                errormsg = f"setupCode {setup_code} could not be executed"
                status = TestStatus.failed

        if not error:
            try:
                """ run teardown-code """
                execute_code_list(teardown_code, namespace)
            except:
                error = True
                errormsg = f"teardownCode {teardown_code} could not be executed"
                status = TestStatus.failed

        """ close all open figures """
        plt.close("all")

        """ change back to where we were before """
        os.chdir(dir_old)

        """ remove test-directory from paths """
        sys.path.remove(specification.testDirectory)

        _solution["exectime"] = exectime
        _solution["traceback"] = tb
        _solution["namespace"] = namespace
        _solution["status"] = status
        _solution["errormsg"] = errormsg
    return solutions[id][where]

class CodeabilityPythonTest:
    # testcases get parametrized in conftest.py (pytest_generate_tests)
    def test_entrypoint(self, pytestconfig, monkeymodule, testcases):
        idx_main, idx_sub = testcases

        _report = pytestconfig.stash[report_key]
        testsuite: CodeAbilityTestSuite = _report["testsuite"]
        specification: CodeAbilitySpecification = _report["specification"]
        main: CodeAbilityTestCollection = testsuite.properties.tests[idx_main]
        sub: CodeAbilityTest = main.tests[idx_sub]

        dir_reference = specification.referenceDirectory
        dir_student = specification.studentDirectory

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

        _solution_student = get_solution(monkeymodule, pytestconfig, idx_main, Solution.student)
        _solution_reference = get_solution(monkeymodule, pytestconfig, idx_main, Solution.reference)
        if _solution_student["status"] == TestStatus.skipped:
            pytest.skip(_solution_student["errormsg"])
        elif _solution_student["status"] != TestStatus.completed:
            pytest.fail(_solution_student["errormsg"])
        #if _solution_reference["status"] != SolutionStatus.completed:
        #    #pytest.skip(_solution_reference["errormsg"])
        #    pass

        solution_student = _solution_student["namespace"]
        solution_reference = _solution_reference["namespace"]

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
                    pass
                finally:
                    if not "val_student" in locals():
                        raise KeyError(f"Variable `{name}` not found in student namespace")

            if qualification == QualificationEnum.verifyEqual:
                """ get the reference value """
                if value is not None:
                    val_reference = value
                elif evalString is not None:
                    try:
                        val_reference = eval(evalString)
                    except Exception as e:
                        pytest.skip(f"Evaluation of `{evalString}` not possible")
                else:
                    if name in solution_reference:
                        val_reference = solution_reference[name]
                    else:
                        try:
                            val_reference = eval(name, solution_reference)
                        except Exception as e:
                            pytest.skip(f"Variable `{name}` not found in reference namespace")
                
                """ assert variable-type """
                type_student = type(val_student)
                type_reference = type(val_reference)
                assert type_student == type_reference, f"Variable `{name}` has incorrect type, expected: {type_reference}, obtained {type_student}"

                """ assert variable-value """
                failure_msg = f"Variable `{name}` has incorrect value"
                if isinstance(val_student, (str, set, frozenset)):
                    assert val_student == val_reference, failure_msg
                elif isinstance(val_student, (DataFrame, Series)):
                    assert val_student.equals(val_reference), failure_msg
                elif isinstance(val_student, np.ndarray):
                    try:
                        if relative_tolerance is None and absolute_tolerance is None:
                            np.testing.assert_allclose(val_student, val_reference)
                        else:
                            np.testing.assert_allclose(val_student, val_reference, rtol=relative_tolerance, atol=absolute_tolerance)
                    except AssertionError as e:
                        raise AssertionError(failure_msg)
                else:
                    """ attention: pytest.approx() does not support nested data structures, like: 'var7 = [[1, 22, 44]]' """
                    assert val_student == pytest.approx(val_reference, rel=relative_tolerance, abs=absolute_tolerance), failure_msg
            elif qualification == QualificationEnum.matches:
                assert str(val_student) == pattern, f"Variable `{name}` does not match the specified pattern `{pattern}`"
            elif qualification == QualificationEnum.contains:
                assert str(val_student).find(pattern) > -1, f"Variable `{name}` does not contain the specified pattern `{pattern}`"
            elif qualification == QualificationEnum.startsWith:
                assert str(val_student).startswith(pattern), f"Variable `{name}` does not start with the specified pattern `{pattern}`"
            elif qualification == QualificationEnum.endsWith:
                assert str(val_student).endswith(pattern), f"Variable `{name}` does not end with the specified pattern `{pattern}`"
            elif qualification == QualificationEnum.count:
                assert str(val_student).count(pattern) == countRequirement, f"Variable `{name}` does not contain the specified pattern `{pattern}` {countRequirement}-times"
            elif qualification == QualificationEnum.regexp:
                result = re.match(re.compile(fr"{pattern}"), str(val_student))
                assert result is not None, f"Variable `{name}` does not match the compiled regular expression from the specified pattern `{pattern}`"
            else:
                pytest.fail(reason="qualification not set")
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
            pytest.fail(reason="type not set")
