import glob
import io
import os
import re
import sys
import time
import pytest
import random
import numpy as np
import traceback
import subprocess
import token
import tokenize
import types
from pandas import DataFrame, Series
from matplotlib import pyplot as plt
from model.model import CodeAbilitySpecification, CodeAbilityTestSuite
from model.model import CodeAbilityTestCollection, CodeAbilityTest
from model.model import TypeEnum, QualificationEnum
from model.model import StatusEnum, ResultEnum
from model.model import CodeAbilityReport
from .conftest import report_key, Solution
from .execution import execute_code_list, execute_file
from .modules import get_imported_modules
from .helper import get_property_as_list, get_abbr
from contextlib import redirect_stdout, redirect_stderr

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
    report: CodeAbilityReport = _report["report"]
    testsuite: CodeAbilityTestSuite = _report["testsuite"]
    specification: CodeAbilitySpecification = _report["specification"]
    main: CodeAbilityTestCollection = testsuite.properties.tests[idx_main]
    id = str(idx_main)

    if id not in solutions:
        solutions[id] = {}
    if where not in solutions[id]:
        solutions[id][where] = {
            "namespace": {},
            "timestamp": time.time(),
            "status": StatusEnum.scheduled,
            "errormsg": "",
            "exectime": 0,
            "traceback": {},
            "errors": [],
            "warnings": [],
            "modules": [],
        }
        _solution = solutions[id][where]
        _dir = specification.studentDirectory if where == Solution.student else specification.referenceDirectory
        entry_point = main.entryPoint
        timeout = main.timeout
        input_answers = get_property_as_list(main.inputAnswers)
        setup_code = get_property_as_list(main.setUpCode)
        teardown_code = get_property_as_list(main.tearDownCode)
        success_dependencies = get_property_as_list(main.successDependency)
        module_blacklist = get_property_as_list(main.moduleBlacklist)
        setup_code_dependency = main.setUpCodeDependency
        store_graphics_artifacts = main.storeGraphicsArtifacts
        if specification.storeGraphicsArtifacts is not None:
            store_graphics_artifacts = specification.storeGraphicsArtifacts

        """ start solution with empty namespace """
        namespace = {}
        if entry_point is not None:
            #todo: check if this correct:
            namespace["__file__"] = os.path.join(_dir, entry_point)

        error = False
        errormsg = ""
        status = StatusEnum.scheduled
        tb = {}
        exectime = 0
        std = {
            "stdout": None,
            "stderr": None,
        }

        """ check success dependencies, mark as skipped if not satisfied """
        for dependency in success_dependencies:
            _idx = main_idx_by_dependency(testsuite, dependency)
            if _idx is None:
                error = True
                errormsg = f"Success-Dependency `{success_dependencies}` not valid"
                status = StatusEnum.failed
            else:
                total = report.tests[_idx].summary.total
                for sub_idx in range(total):
                    result = report.tests[_idx].tests[sub_idx].result
                    if result != ResultEnum.passed:
                        error = True
                        errormsg = f"Success-Dependency `{success_dependencies}` not satisfied"
                        status = StatusEnum.skipped
                        break
            if error:
                break

        if setup_code_dependency is not None and not error:
            _idx = main_idx_by_dependency(testsuite, setup_code_dependency)
            if _idx is None:
                error = True
                errormsg = f"Setup-Code-Dependency `{setup_code_dependency}` not valid"
                status = StatusEnum.failed
            else:
                try:
                    namespace = solutions[str(_idx)][where]["namespace"]
                except Exception as e:
                    error = True
                    errormsg = f"ERROR: Setup-Code-Dependency `{setup_code_dependency}` not found"
                    status = StatusEnum.failed

        """ remember old working directory """
        dir_old = os.getcwd()

        """ add test-directory to paths """
        #todo: test if this works
        sys.path.append(specification.testDirectory)
        sys.path.append(_dir)

        """ change into solution-directory student | reference """
        os.chdir(_dir)

        """ close all open figures """
        plt.close("all")

        """ seed the random generator """
        random.seed(1)
        np.random.seed(1)

        """ Override/Disable certain methods """ 
        mm.setattr(plt, "show", lambda *x: None)
        if len(input_answers) > 0:
            mm.setattr('sys.stdin', io.StringIO("\n".join(input_answers)))
        
        def calculate_solution():
            nonlocal error, errormsg, status, exectime, tb, status, namespace

            if entry_point is not None and not error:
                filename = os.path.join(_dir, entry_point)
                if not os.path.exists(filename):
                    if where == Solution.student:
                        error = True
                        errormsg = f"entryPoint {entry_point} not found"
                        status = StatusEnum.failed
                else:
                    modules = get_imported_modules(filename)
                    blacklisted = list(set(modules).intersection(module_blacklist))
                    if len(blacklisted):
                        error = True
                        errormsg = f"Import not allowed for: {blacklisted}"
                        status = StatusEnum.failed
                    else:
                        try:
                            start_time = time.time()
                            result = execute_file(_dir, entry_point, namespace, timeout)
                            time.sleep(0.0001)
                            exectime = time.time() - start_time
                            if result is None:
                                error = True
                                errormsg = f"Maximum execution time of {timeout} seconds exceeded"
                                status = StatusEnum.timedout
                        except Exception as e:
                            error = True
                            errormsg = f"Execution of {filename} failed, ERROR: {e}"
                            status = StatusEnum.crashed
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
                    status = StatusEnum.failed

            # todo: tearDownCode is not really useful here :-)
            if not error:
                try:
                    """ run teardown-code """
                    execute_code_list(teardown_code, namespace)
                except:
                    error = True
                    errormsg = f"teardownCode {teardown_code} could not be executed"
                    status = StatusEnum.failed

        if main.type == TypeEnum.stdout:
            out = io.StringIO()
            with redirect_stdout(out):
                calculate_solution()
            std["stdout"] = out.getvalue()
        else:
            calculate_solution()

        """ undo monkeypatches """
        mm.undo()

        """ close all open figures """
        plt.close("all")

        """ change back to where we were before """
        os.chdir(dir_old)

        """ remove test-directory from paths """
        sys.path.remove(specification.testDirectory)
        sys.path.remove(_dir)

        if not error:
            status = StatusEnum.completed

        _solution["exectime"] = exectime
        _solution["traceback"] = tb
        _solution["namespace"] = namespace
        _solution["status"] = status
        _solution["errormsg"] = errormsg
        _solution["std"] = std
    return solutions[id][where]

class CodeabilityPythonTest:
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
        allowed_occurance_range = sub.allowedOccuranceRange
        occurance_type = sub.occuranceType
        typeCheck = sub.typeCheck
        shapeCheck = sub.shapeCheck

        try:
            _solution_student = get_solution(monkeymodule, pytestconfig, idx_main, Solution.student)
            _solution_reference = get_solution(monkeymodule, pytestconfig, idx_main, Solution.reference)
        except Exception as e:
            pytest.fail(f"getting solution failed, error: {e}")

        if _solution_student["status"] == StatusEnum.skipped:
            pytest.skip(_solution_student["errormsg"])
        elif _solution_student["status"] != StatusEnum.completed:
            pytest.fail(_solution_student["errormsg"])
        #if _solution_reference["status"] != SolutionStatus.completed:
        #    #pytest.skip(_solution_reference["errormsg"])
        #    pass

        if testtype in [
            TypeEnum.variable,
            TypeEnum.graphics,
            TypeEnum.error,
            TypeEnum.warning,
            TypeEnum.help,
            TypeEnum.stdout,
        ]:
            solution_student = _solution_student["namespace"]
            solution_reference = _solution_reference["namespace"]

            """ if test is graphics => get saved graphics object as solution """
            if testtype == TypeEnum.graphics:
                solution_student = solution_student["_graphics_object_"]
                solution_reference = solution_reference["_graphics_object_"]

            """ get the student value """
            if testtype == TypeEnum.stdout:
                val_student = _solution_student["std"]["stdout"]
            elif name in solution_student:
                val_student = solution_student[name]
            else:
                """ value not found, try eval """
                try:
                    val_student = eval(name, solution_student)
                except Exception as e:
                    raise KeyError(f"Variable `{name}` not found in student namespace") from None

            if qualification == QualificationEnum.verifyEqual:
                """ get the reference value """
                if value is not None:
                    val_reference = value
                elif evalString is not None:
                    try:
                        val_reference = eval(evalString, solution_reference)
                    except Exception as e:
                        pytest.skip(f"Evaluation of `{evalString}` not possible")
                else:
                    if testtype == TypeEnum.stdout:
                        val_reference = _solution_reference["std"]["stdout"]
                    elif name in solution_reference:
                        val_reference = solution_reference[name]
                    else:
                        try:
                            val_reference = eval(name, solution_reference)
                        except Exception as e:
                            pytest.skip(f"Variable `{name}` not found in reference namespace")
                
                if typeCheck:
                    """ assert variable-type """
                    type_student = type(val_student)
                    type_reference = type(val_reference)
                    assert type_student == type_reference, f"Variable `{name}` has incorrect type, expected: {type_reference}, obtained {type_student}"

                if shapeCheck:
                    """ assert variable-shape, of supported types, dont look for int,float,complex,bool,NoneType """
                    if isinstance(val_student, (str, list, tuple, range, dict, set, frozenset, bytes, bytearray, memoryview)):
                        len_student = len(val_student)
                        len_reference = len(val_reference)
                        assert len_student == len_reference, f"Variable `{name}` has incorrect len, expected: {len_reference}, obtained {len_student}"
                    elif isinstance(val_student, np.ndarray):
                        shape_student = val_student.shape
                        shape_reference = val_reference.shape
                        assert shape_student == shape_reference, f"Variable `{name}` has incorrect shape, expected: {shape_reference}, obtained {shape_student}"
                    else:
                        #todo: which types support something like len, shape, dimensions, etc...?
                        pass

                """ assert variable-value """
                #todo: support for more types
                failure_msg = f"Variable `{name}` has incorrect value (`{get_abbr(val_student)}` instead of `{get_abbr(val_reference)}`)"
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
                pytest.skip(reason="qualification not set")
        elif testtype == TypeEnum.structural:
            if allowed_occurance_range is None:
                pytest.skip(reason="allowedOccuranceRange not set")
            if not hasattr(token, occurance_type):
                pytest.skip(reason=f"occuranceType not found: {occurance_type}")
            c_type = getattr(token, occurance_type)
            if not isinstance(c_type, int):
                pytest.skip(reason=f"occuranceType not int: {type(c_type)}")
            c_min = allowed_occurance_range[0]
            c_max = allowed_occurance_range[1]
            c = 0
            ff = os.path.join(dir_student, file)
            with open(ff, 'rb') as f:
                tokens = tokenize.tokenize(f.readline)
                for _token in tokens:
                    #print(f"{_token.exact_type} -- {_token}" )
                    if _token.type == c_type and _token.string == name:
                        c += 1
            if c < c_min:
                raise AssertionError(f"`{name}` found {c}-times, minimum required: {c_min}")
            if c > c_max:
                raise AssertionError(f"`{name}` found {c}-times, maximum required: {c_max}")
        elif testtype == TypeEnum.linting:
            filename = f"{main.name}-{name}-linting.txt"
            filename = filename.replace(" ", "-")
            outputfile = os.path.join(specification.outputDirectory, filename)
            if os.path.exists(outputfile):
                os.remove(outputfile)
            ff = os.path.join(dir_student, file)
            #todo: find something better than "pattern" as ignorelist
            #ignore_list = ["W"]
            #ignore = ",".join(ignore_list)
            result = subprocess.run(f'python -m flake8 {ff} --tee --output-file="{outputfile}" --ignore={pattern}', shell=True, capture_output=True)
            _stdout = result.stdout.decode()
            _stderr = result.stderr
            lines = _stdout.splitlines()
            errcount = len(lines)
            rlines = []
            for line in lines:
                arr = line.split(": ")
                arr1 = arr[0].rsplit(":", 2)
                fn = os.path.relpath(arr1[0], dir_student)
                rlines.append(f"{fn}:{arr1[1]}:{arr1[2]} {arr[1]}")
            _solution_student["errors"] = rlines
            if len(_stderr) > 0:
                pytest.skip(reason=f"Linting Error occurred: {_stderr}")
            if errcount > 0:
                raise SyntaxError(f"{errcount} Syntax Error{'s' if errcount != 1 else ''} in file `{file}` (see: {outputfile})")
        elif testtype == TypeEnum.exist:
            len_s = len(glob.glob(file, root_dir=dir_student))
            len_r = len(glob.glob(file, root_dir=dir_reference))
            if len_s == 0:
                raise FileNotFoundError(f"File with pattern `{file}` not found in student namespace")
            if len_r == 0:
                raise FileNotFoundError(f"File with pattern `{file}` not found in reference namespace")
        else:
            pytest.skip(reason="type not set")
