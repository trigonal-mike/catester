import glob
import json
import os
import time
import shutil
import subprocess
import yaml
from colorama import Fore, Back, Style
from pydantic import ValidationError
from model.model import TypeEnum, QualificationEnum, LanguageEnum, MetaTypeEnum
from model.model import parse_meta_file, parse_spec_file, parse_test_file
from model.model import CodeAbilityLink, CodeAbilityPerson, CodeAbilitySpecification
from model.model import CodeAbilityTestSuite, CodeAbilityTestProperty, CodeAbilityTestCollection, CodeAbilityTest 
from .settings import VALID_PROPS_META, VALID_PROPS_TESTSUITE, VALID_PROPS_TESTCOLLECTION_COMMON, VALID_PROPS_TESTCOLLECTION, VALID_PROPS_TEST
from .settings import TokenEnum, ARGUMENT_VALUE_TOKENS, TEST_MAPPING, LOCAL_TEST_DIRECTORIES

class Converter:
    def __init__(self, scandir, testrunnerdir, assignmentsdir, action, verbosity, pytestflags, metatemplate, formatter):
        self.ready = False
        self.scandir = scandir
        self.testrunnerdir = testrunnerdir
        self.assignmentsdir = assignmentsdir
        self.action = action
        self.verbosity = verbosity
        self.pytestflags = pytestflags
        self.metatemplate = metatemplate
        self.formatter = formatter
        try:
            self.init()
            self.ready = True
        except Exception as e:
            print(e)
            print(f"{Fore.RED}ERROR Initialization failed{Style.RESET_ALL}")

    def init(self):
        if self.scandir is None:
            self.scandir = os.getcwd()
        if not os.path.exists(self.scandir):
            raise Exception(f"Directory not found: {self.scandir}")
        self.scandir = os.path.abspath(self.scandir)
        os.chdir(self.scandir)
        flist = glob.glob("*_master.py")
        count = len(flist)
        if count == 0:
            raise Exception(f"No file named *_master.py in directory: {self.scandir}")
        if count >= 2:
            raise Exception(f"Only one master file alllowed. {count} files named *_master.py in directory: {self.scandir}")
        masterfile = flist[0]
        entrypoint = masterfile.replace("_master", "")
        self.entrypoint = entrypoint
        self.masterfile = os.path.join(self.scandir, masterfile)
        self.py_file = os.path.join(self.scandir, entrypoint)
        self.meta_yaml = os.path.join(self.scandir, "meta.yaml")
        self.test_yaml = os.path.join(self.scandir, "test.yaml")
        self.localTestdir = os.path.join(self.scandir, "localTests")

    def start(self):
        self.errors = 0
        self.warnings = 0
        if not self.ready:
            return
        try:
            if self.action in [None, "all", "cleanup"]:
                self.cleanup()
            if self.action in [None, "all", "convert"]:
                self.convert()
            if self.action in [None, "all", "test"]:
                self.run_local_tests()
        except Exception as e:
            print(e)
            print(f"{Fore.RED}ERROR occurred{Style.RESET_ALL}")

    def _remove_directory(self, path):
        if os.path.exists(path):
            print(f"{Fore.MAGENTA}Removed directory: {path}{Style.RESET_ALL}")
            shutil.rmtree(path)

    def _remove_file(self, path):
        if os.path.exists(path):
            os.remove(path)
            print(f"{Fore.MAGENTA}Removed file: {path}{Style.RESET_ALL}")

    def cleanup(self):
        print(f"Cleanup started: {self.scandir}")
        self._remove_file(self.py_file)
        self._remove_file(self.meta_yaml)
        self._remove_file(self.test_yaml)
        for directory in LOCAL_TEST_DIRECTORIES._member_names_:
            dir = os.path.join(self.localTestdir, directory)
            self._remove_directory(dir)
        if os.path.exists(self.localTestdir) and not os.listdir(self.localTestdir):
            self._remove_directory(self.localTestdir)
        print(f"Cleanup ended")

    def convert(self):
        start = time.time()
        try:
            self._init_meta_yaml()
            self._analyze_tokens()
            self._convert_tokens()
            self._write_yaml("TestSuite", self.test_yaml, self.testsuite, parse_test_file)
            self._write_yaml("Meta", self.meta_yaml, self.metaconfig, parse_meta_file)
            self._create_reference()
            self._format_all_files()
            self._prepare_local_test_directories()
        except Exception as e:
            print(f"{Fore.RED}ERROR Conversion failed{Style.RESET_ALL}")
            raise
        end = round(time.time() - start, 3)
        print(f"{Fore.GREEN}Conversion successful, duration {end} seconds{Style.RESET_ALL}")

    def _create_reference(self):
        print(f"Creating Reference-File: {self.py_file}")
        with open(self.py_file, "w") as file:
            file.write("".join(self.lines))
        print(f"{Fore.GREEN}Reference-File created{Style.RESET_ALL}")

    def _format_path(self, path):
        print(f"Formatting File/Folder: {path}")
        retcode = subprocess.run(f"python -m black {path}", shell=True)
        print(f"{Fore.GREEN}File/Folder formatted{Style.RESET_ALL}")

    def _format_all_files(self):
        #todo: only format .py files?
        if self.formatter is not False:
            self._format_path(self.py_file)
            for file in self.metaconfig.properties.additionalFiles:
                self._format_path(file)
            for file in self.metaconfig.properties.studentTemplates:
                self._format_path(file)

    def _init_meta_yaml(self):
        if self.metatemplate is not None and not os.path.isabs(self.metatemplate):
            self.metatemplate = os.path.join(self.scandir, self.metatemplate)
            self.metatemplate = os.path.abspath(self.metatemplate)
        self.metaconfig = parse_meta_file(self.metatemplate)
        self.metaconfig.properties.studentSubmissionFiles.append(self.py_file.replace(self.scandir, "."))

    def _write_yaml(self, title, filename, obj, parsing_fct):
        print(f"Creating {title}: {filename}")
        with open(filename, "w") as file:
            yaml.dump(obj.model_dump(exclude_none=True), file, sort_keys=False, indent=2, allow_unicode=True)
        print(f"{Fore.GREEN}{title} created{Style.RESET_ALL}")
        print(f"Validating {title}")
        try:
            _test = parsing_fct(filename)
        except ValidationError as e:
            print(e)
            print(f"{Fore.RED}{title} could not be validated{Style.RESET_ALL}")
            raise
        print(f"{Fore.GREEN}{title} validated{Style.RESET_ALL}")

    def _analyze_tokens(self):
        print(f"Analyzing Tokens: {self.masterfile}")
        with open(self.masterfile, "r") as file:
            masterlines = file.readlines()
        #lines = [l for l in lines if l.startswith("#$")]
        self.lines = []
        self.tokens = []
        for idx, line in enumerate(masterlines):
            if line.startswith("#$"):
                line = line.rstrip()[2:]
                try:
                    token, argument, value = self._extract_from_line(line)
                    self.tokens.append((token, argument, value, idx, line))
                except Exception as e:
                    self._error(f"{Fore.RED}ERROR in Line {idx+1}{Style.RESET_ALL}: {line}\n{e}")
            elif not line.startswith("##"):
                self.lines.append(line)
        if self.errors > 0:
            print(f"{Fore.RED}{self.errors} error{'s' if self.errors>1 else ''} occurred, Analyzing Tokens failed{Style.RESET_ALL}")
            raise
        print(f"{Fore.GREEN}All Tokens valid{Style.RESET_ALL}")

    def _extract_from_line(self, line: str):
        if len(line) == 0:
            raise Exception("Line too short")
        arr = line.split(" ", 1)
        token = arr[0]
        if token not in TokenEnum._member_names_:
            raise Exception(f"token invalid: {Fore.MAGENTA}{token}{Style.RESET_ALL}\nchoose from: {TokenEnum._member_names_}")
        if len(arr) == 1:
            raise Exception("no argument specified")
        if token not in ARGUMENT_VALUE_TOKENS:
            return token, arr[1].strip(), None
        arr = arr[1].split(" ", 1)
        if len(arr) == 1:
            raise Exception("no value specified")
        argument = arr[0].strip()
        value = arr[1].strip()
        if argument == "language":
            self._check_value(value, LanguageEnum._member_names_)
        if argument == "qualification":
            self._check_value(value, QualificationEnum._member_names_)
        if argument == "type":
            if token == TokenEnum.PROPERTY:
                self._check_value(value, TypeEnum._member_names_)
            elif token == TokenEnum.META:
                self._check_value(value, MetaTypeEnum._member_names_)
        return token, argument, value
    
    def _check_value(self, value, valid_values):
        if value not in valid_values:
            raise Exception(f"value invalid: {Fore.MAGENTA}{value}{Style.RESET_ALL}\nchoose from: {valid_values}")

    def list_scandir(self):
        excluded = [
            os.path.basename(self.meta_yaml),
            os.path.basename(self.test_yaml),
            os.path.basename(self.localTestdir),
            os.path.basename(self.masterfile),
            os.path.basename(self.py_file),
        ]
        dirlist = os.listdir(self.scandir)
        res = filter(lambda x: x not in excluded, dirlist)
        return list(res)
    
    def _error(self, msg):
        self.errors += 1
        print(msg)

    def _warning(self, msg):
        self.warnings += 1
        print(msg)

    def _find_argument(self, token, valid_props):
        token, argument, value, idx, line = token
        if argument not in valid_props:
            self._error(f"{Fore.RED}ERROR in Line {idx+1}{Style.RESET_ALL}: {line}\nargument invalid: {Fore.MAGENTA}{argument}{Style.RESET_ALL}\nchoose from: {valid_props}")
            return False
        return True

    def _try_set_value(self, token, obj):
        tokenname, argument, value, idx, line = token
        try:
            value = json.loads(value)
        except Exception as e:
            pass
        try:
            is_list = False
            if argument in ("links", "supportingMaterial"):
                value = CodeAbilityLink(**value)
                is_list = True
            elif argument in ("authors", "maintainers"):
                value = CodeAbilityPerson(**value)
                is_list = True
            elif argument in ("successDependency", "inputAnswers", "setUpCode", "tearDownCode", "keywords", "testDependencies"):
                is_list = True
            if is_list:
                v = getattr(obj, argument) or []
                if isinstance(value, list):
                    v.extend(value)
                else:
                    v.append(value)
                setattr(obj, argument, v)
            else:
                setattr(obj, argument, value)
        except Exception as e:
            self._error(f"{e}\n{Fore.RED}ERROR in Line {idx+1}{Style.RESET_ALL}: {line}\nvalue invalid: {Fore.MAGENTA}{value}{Style.RESET_ALL}")

    def _convert_tokens(self):
        print(f"Converting {len(self.tokens)} Tokens")
        testsuite = CodeAbilityTestSuite(
            properties = CodeAbilityTestProperty(
                tests = []
            )
        )
        curr_test = -1
        curr_subtest = -1
        for _idx, token in enumerate(self.tokens):
            tokenname, argument, value, idx, line = token
            if tokenname == TokenEnum.TESTSUITE:
                if self._find_argument(token, VALID_PROPS_TESTSUITE):
                    self._try_set_value(token, testsuite)
            elif tokenname == TokenEnum.PROPERTY:
                if curr_test == -1:
                    if self._find_argument(token, VALID_PROPS_TESTCOLLECTION_COMMON):
                        self._try_set_value(token, testsuite.properties)
                elif curr_subtest == -1:
                    if self._find_argument(token, VALID_PROPS_TESTCOLLECTION):
                        self._try_set_value(token, testsuite.properties.tests[curr_test])
                else:
                    if self._find_argument(token, VALID_PROPS_TEST):
                        self._try_set_value(token, testsuite.properties.tests[curr_test].tests[curr_subtest])
            elif tokenname in (TEST_MAPPING):
                curr_subtest = -1
                curr_test += 1
                testsuite.properties.tests.append(
                    CodeAbilityTestCollection(
                        type = TEST_MAPPING[tokenname],
                        name = argument,
                        entryPoint = self.entrypoint,
                        tests = [],
                    )
                )
            elif tokenname == TokenEnum.TESTVAR:
                curr_subtest += 1
                testsuite.properties.tests[curr_test].tests.append(
                    CodeAbilityTest(
                        name = argument,
                    )
                )
            elif tokenname == TokenEnum.META:
                if self._find_argument(token, VALID_PROPS_META):
                    if argument in ("studentSubmissionFiles", "additionalFiles", "testFiles", "studentTemplates"):
                        v = getattr(self.metaconfig.properties, argument)
                        files = value.split(":")
                        for file in files:
                            f = file.strip()
                            ff = os.path.join(self.scandir, f)
                            ff = os.path.abspath(ff)
                            if os.path.exists(ff):
                                f = ff.replace(self.scandir, ".")
                                if f == ".":
                                    self._error(f"{Fore.RED}ERROR: choose files/folders from inside scandir: {self.list_scandir()}{Style.RESET_ALL}")
                                else:
                                    v.append(f)
                            else:
                                self._error(f"{Fore.RED}ERROR: Additional file/folder does not exist: {f}{Style.RESET_ALL}")
                    else:
                        self._try_set_value(token, self.metaconfig)
        if len(testsuite.properties.tests) == 0:
            self._warning(f"{Fore.YELLOW}WARNING: no testcollection specified{Style.RESET_ALL}")
        for idx, test in enumerate(testsuite.properties.tests):
            if len(test.tests) == 0:
                self._error(f"{Fore.RED}ERROR at testcollection #{idx+1} '{test.name}' no tests specified{Style.RESET_ALL}")
        if self.warnings > 0:
            print(f"{Fore.YELLOW}{self.warnings} warning{'s' if self.warnings>1 else ''} occurred{Style.RESET_ALL}")
        if self.errors > 0:
            print(f"{Fore.RED}{self.errors} error{'s' if self.errors>1 else ''} occurred, Converting Tokens failed{Style.RESET_ALL}")
            raise
        print(f"{Fore.GREEN}All Tokens converted{Style.RESET_ALL}")
        self.testsuite = testsuite

    def _prepare_local_test_directories(self):
        print(f"Preparing Local Test Directory: {self.localTestdir}")
        if not os.path.exists(self.localTestdir):
            os.makedirs(self.localTestdir)
            print(f"Creating directory: {self.localTestdir}")
        else:
            print(f"{Fore.CYAN}Directory already exists:{Style.RESET_ALL} {self.localTestdir}")
        if not os.path.exists(self.test_yaml):
            print(f"test.yaml does not exist in directory: {self.scandir}")
            return
        for directory in LOCAL_TEST_DIRECTORIES._member_names_:
            test_directory = os.path.join(self.localTestdir, directory)
            self._remove_directory(test_directory)
            print(f"Creating directory: {test_directory}")
            os.makedirs(test_directory)
            if not directory == LOCAL_TEST_DIRECTORIES._emptySolution:
                self._copy_files(test_directory, self.metaconfig.properties.additionalFiles)
                self._copy_files(test_directory, self.metaconfig.properties.studentTemplates)
                self._copy_files(test_directory, self.metaconfig.properties.studentSubmissionFiles)

    def _copy_files(self, directory: str, files: list[str]):
        for file in files:
            dir = os.path.dirname(file)
            fn = os.path.basename(file)
            dest = os.path.join(directory, dir, fn)
            dest = os.path.abspath(dest)
            if os.path.isdir(file):
                shutil.copytree(file, dest, dirs_exist_ok=True)
            else:
                dir = os.path.dirname(dest)
                os.makedirs(dir, exist_ok=True)
                shutil.copy(file, dest)

    def run_local_tests(self):
        if not os.path.exists(self.localTestdir):
            raise Exception(f"Directory not found: {self.localTestdir}")
        directories = [ f.path for f in os.scandir(self.localTestdir) if f.is_dir() and not f.path.endswith("_reference") ]
        print(f"Running {len(directories)} local tests: {self.localTestdir}")
        self._remove_directory(self.testrunnerdir)
        os.makedirs(self.testrunnerdir)
        for idx, test_directory in enumerate(directories):
            nr = idx + 1
            print()
            print(f"{Back.MAGENTA}Running local test #{nr}{Style.RESET_ALL}")
            print(f"{Back.MAGENTA}Directory: {test_directory}{Style.RESET_ALL}")
            testdir_name = os.path.basename(os.path.normpath(test_directory))
            runner_directory = os.path.join(self.testrunnerdir, f"test{nr}-{testdir_name}")
            os.makedirs(runner_directory)
            self._run_local_test(test_directory, runner_directory)

    def _get_assignment_rel_path(self, directory: str):
        yyy = os.path.relpath(directory, self.assignmentsdir)
        zzz = yyy.split(os.sep)
        p = os.curdir
        for part in zzz:
            if part == "localTests":
                break
            p = os.path.join(p, part)
        return p

    def _run_local_test(self, test_directory: str, runner_directory: str):
        assignment_path = self._get_assignment_rel_path(test_directory)
        studentDir = os.path.join("student", assignment_path)
        referenceDir = os.path.join("reference", assignment_path)
        sdir = os.path.join(runner_directory, studentDir)
        rdir = os.path.join(runner_directory, referenceDir)
        os.makedirs(sdir)
        os.makedirs(rdir)
        refdir = os.path.join(self.localTestdir, LOCAL_TEST_DIRECTORIES._reference)
        shutil.copytree(test_directory, sdir, dirs_exist_ok=True)
        shutil.copytree(refdir, rdir, dirs_exist_ok=True)

        for x in self.metaconfig.testDependencies:
            xx = os.path.join(self.scandir, x)
            xx = os.path.abspath(xx)
            rdir1 = os.path.join(rdir, x)
            sdir1 = os.path.join(sdir, x)
            if os.path.isdir(xx):
                shutil.copytree(xx, rdir1, dirs_exist_ok=True)
                shutil.copytree(xx, sdir1, dirs_exist_ok=True)
            else:
                dir1 = os.path.dirname(rdir1)
                dir2 = os.path.dirname(sdir1)
                os.makedirs(dir1, exist_ok=True)
                os.makedirs(dir2, exist_ok=True)
                shutil.copy(xx, rdir1)
                shutil.copy(xx, sdir1)

        local_test_specification = CodeAbilitySpecification(
            referenceDirectory=referenceDir,
            studentDirectory=studentDir,
            isLocalUsage=True
        )
        self.spec_file = os.path.join(runner_directory, "specification.yaml")
        self._write_yaml("Specification", self.spec_file, local_test_specification, parse_spec_file)
        shutil.copy(self.test_yaml, runner_directory)
        shutil.copy(self.meta_yaml, runner_directory)

        #return
        os.chdir(runner_directory)
        dir = os.path.dirname(__file__)
        run_tests_py = os.path.join(dir, "../run_tests.py")
        run_tests_py = os.path.abspath(run_tests_py)
        retcode = subprocess.run(f"python {run_tests_py} --specification={self.spec_file} --verbosity={self.verbosity} --pytestflags={self.pytestflags}", shell=True)
        if int(self.verbosity) > 0:
            print(retcode)
