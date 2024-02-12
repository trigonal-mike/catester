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

LOCAL_TEST_SPECIFICATION = CodeAbilitySpecification(
    referenceDirectory="../_reference",
    isLocalUsage=True
)

class Converter:
    def __init__(self, scandir, metatemplate = None):
        self.ready = False
        self._scan_dir = scandir
        if scandir is None:
            scandir = os.getcwd()
        if not os.path.exists(scandir):
            print(f"Directory not found: {scandir}")
            return
        scandir = os.path.abspath(scandir)
        os.chdir(scandir)
        flist = glob.glob("*_master.py")
        if len(flist) == 0:
            print(f"No file named *_master.py in directory: {scandir}")
            return
        entrypoint = flist[0].replace("_master", "")
        self.scandir = scandir
        self.entrypoint = entrypoint
        self.masterfile = os.path.join(scandir, flist[0])
        self.py_file = os.path.join(scandir, entrypoint)
        self.meta_yaml = os.path.join(scandir, "meta.yaml")
        self.test_yaml = os.path.join(scandir, "test.yaml")
        self.spec_file = os.path.join(self.scandir, "specification.yaml")
        self.localTestdir = os.path.join(self.scandir, "localTests")
        self.ready = True
        self.conv_error = False

        if metatemplate is not None and not os.path.isabs(metatemplate):
            metatemplate = os.path.join(scandir, metatemplate)
            metatemplate = os.path.abspath(metatemplate)
        self.metaconfig = parse_meta_file(metatemplate)
        self.metaconfig.properties.studentSubmissionFiles.append(self.py_file.replace(self.scandir, "."))

    def _remove_file(self, path):
        if os.path.exists(path):
            os.remove(path)
            print(f"{Fore.MAGENTA}Removed file: {path}{Style.RESET_ALL}")

    def cleanup(self):
        print(f"Cleanup started: {self.scandir}")
        self._remove_file(self.py_file)
        self._remove_file(self.meta_yaml)
        self._remove_file(self.test_yaml)
        self._remove_file(self.spec_file)
        for directory in LOCAL_TEST_DIRECTORIES._member_names_:
            dir = os.path.join(self.localTestdir, directory)
            if os.path.exists(dir):
                shutil.rmtree(dir)
                print(f"{Fore.MAGENTA}Removed directory: {dir}{Style.RESET_ALL}")
        if os.path.exists(self.localTestdir) and not os.listdir(self.localTestdir):
            shutil.rmtree(self.localTestdir)
            print(f"{Fore.MAGENTA}Removed empty directory: {self.localTestdir}{Style.RESET_ALL}")
        print(f"Cleanup ended")

    def convert(self):
        self.conv_error = True
        if not self.ready:
            print(f"{Fore.RED}ERROR Conversion, directory invalid: {self._scan_dir}{Style.RESET_ALL}")
        start = time.time()
        self.errors = 0

        try:
            self._analyze_tokens()
            self._convert_tokens()
            self._write_yaml("TestSuite", self.test_yaml, self.testsuite, parse_test_file)
            self._write_yaml("Specification", self.spec_file, LOCAL_TEST_SPECIFICATION, parse_spec_file)
            self._write_yaml("Meta", self.meta_yaml, self.metaconfig, parse_meta_file)
        except:
            return

        print(f"Creating Reference-File: {self.py_file}")
        with open(self.py_file, "w") as file:
            file.write("".join(self.lines))
        print(f"{Fore.GREEN}Reference-File created{Style.RESET_ALL}")
        #todo: validate reference-file for obvious errors, linting, ...!!!

        print(f"Preparing Local Test Directory: {self.localTestdir}")
        self._prepare_local_test_directories()

        end = round(time.time() - start, 3)
        print(f"{Fore.GREEN}Conversion successful, duration {end} seconds{Style.RESET_ALL}")
        self.conv_error = False

    def _write_yaml(self, title, filename, obj, parsing_fct):
        print(f"Creating {title}: {filename}")
        with open(filename, "w") as file:
            yaml.dump(obj.model_dump(exclude_none=True), file, sort_keys=False, indent=2)
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
            os.path.basename(self.spec_file),
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
        self.errors = self.errors + 1
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
            elif argument in ("successDependency", "setUpCode", "tearDownCode", "keywords"):
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
                curr_test = curr_test + 1
                testsuite.properties.tests.append(
                    CodeAbilityTestCollection(
                        type = TEST_MAPPING[tokenname],
                        name = argument,
                        entryPoint = self.entrypoint,
                        tests = [],
                    )
                )
            elif tokenname == TokenEnum.TESTVAR:
                curr_subtest = curr_subtest + 1
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
                                    #todo:
                                    #maybe better following?
                                    #.\file.py => file.py
                                    #.\data\dat.txt => data\dat.txt
                                    #v.append(os.path.relpath(f))
                            else:
                                self._error(f"{Fore.RED}ERROR: Additional file/folder does not exist: {f}{Style.RESET_ALL}")
                    else:
                        self._try_set_value(token, self.metaconfig)
        if len(testsuite.properties.tests) == 0:
            self._error(f"{Fore.RED}ERROR no testcollection specified{Style.RESET_ALL}")
        for idx, test in enumerate(testsuite.properties.tests):
            if len(test.tests) == 0:
                self._error(f"{Fore.RED}ERROR at testcollection #{idx+1} '{test.name}' no tests specified{Style.RESET_ALL}")
        if self.errors > 0:
            print(f"{Fore.RED}{self.errors} error{'s' if self.errors>1 else ''} occurred, Converting Tokens failed{Style.RESET_ALL}")
            raise
        print(f"{Fore.GREEN}All Tokens converted{Style.RESET_ALL}")
        self.testsuite = testsuite

    def _prepare_local_test_directories(self):
        if not os.path.exists(self.localTestdir):
            os.makedirs(self.localTestdir)
            print(f"Creating directory: {self.localTestdir}")
        else:
            print(f"{Fore.CYAN}Directory already exists:{Style.RESET_ALL} {self.localTestdir}")
        if not os.path.exists(self.test_yaml):
            print(f"test.yaml does not exist in directory: {self.scandir}")
            return
        for directory in LOCAL_TEST_DIRECTORIES._member_names_:
            self._init_local_test_dir(directory)

    def _init_local_test_dir(self, directory: str):
        isref = directory == LOCAL_TEST_DIRECTORIES._reference
        isempty = directory == LOCAL_TEST_DIRECTORIES._emptySolution
        directory = os.path.join(self.localTestdir, directory)
        student_directory = os.path.join(directory, "student")
        if os.path.exists(directory):
            print(f"{Fore.MAGENTA}Removing directory: {directory}{Style.RESET_ALL}")
            shutil.rmtree(directory)
        print(f"Creating directory: {directory}")
        os.makedirs(directory)
        if isref:
            shutil.copy(self.py_file, directory)
            self._copy_addfiles(directory)
        else:
            shutil.copy(self.test_yaml, directory)
            shutil.copy(self.meta_yaml, directory)
            os.makedirs(student_directory)
            if not isempty:
                shutil.copy(self.py_file, student_directory)
                self._copy_addfiles(student_directory)

    def _copy_addfiles(self, directory: str):
        for file in self.metaconfig.properties.additionalFiles:
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

    def run_local_tests(self, verbosity):
        if self.conv_error:
            print(f"{Back.YELLOW}Testing skipped{Style.RESET_ALL}")
            return
        directories = [ f.path for f in os.scandir(self.localTestdir) if f.is_dir() and not f.path.endswith("_reference") ]
        print(f"Running {len(directories)} local tests: {self.localTestdir}")
        for idx, directory in enumerate(directories):
            print()
            print(f"{Back.MAGENTA}Running local test #{idx+1}{Style.RESET_ALL}")
            print(f"{Back.MAGENTA}Directory: {directory}{Style.RESET_ALL}")
            self._run_local_test(directory, verbosity)

    def _run_local_test(self, directory, verbosity):
        os.chdir(directory)
        dir = os.path.dirname(__file__)
        run_tests_py = os.path.join(dir, "../run_tests.py")
        run_tests_py = os.path.abspath(run_tests_py)
        retcode = subprocess.run(f"python {run_tests_py} --specification={self.spec_file} --verbosity={verbosity}", shell=True)
        print(retcode)
