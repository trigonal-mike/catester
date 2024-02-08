import glob
import os
import time
import shutil
import subprocess
from colorama import Fore, Back, Style
from enum import Enum
from pydantic import ValidationError
from model.model import TypeEnum, QualificationEnum
from model.model import parse_test_file
from model.model import DEFAULTS
from .enums import VALID_PROPS_TESTSUITE, VALID_PROPS_TESTCOLLECTION_COMMON, VALID_PROPS_TESTCOLLECTION, VALID_PROPS_TEST, TokenEnum

DEFAULT_SPECIFICATION = """referenceDirectory: "../_reference"\nisLocalUsage: true\n"""

TEST_MAPPING = {
    TokenEnum.VARIABLETEST: TypeEnum.variable,
    TokenEnum.GRAPHICSTEST: TypeEnum.graphics,
    TokenEnum.EXISTANCETEST: TypeEnum.exist,
    TokenEnum.LINTINGTEST: TypeEnum.linting,
    TokenEnum.STRUCTURALTEST: TypeEnum.structural,
    TokenEnum.ERRORTEST: TypeEnum.error,
    TokenEnum.HELPTEST: TypeEnum.help,
    TokenEnum.WARNINGTEST: TypeEnum.warning,
}

ARGUMENT_VALUE_TOKENS = (
    TokenEnum.TESTSUITE,
    TokenEnum.PROPERTY,
)

class LOCAL_TEST_DIRECTORIES(str, Enum):
    _reference = "_reference"
    _correctSolution = "_correctSolution"
    _emptySolution = "_emptySolution"

class Converter:
    def __init__(self, scandir):
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

    def cleanup(self):
        print(f"Cleanup started: {self.scandir}")
        if os.path.exists(self.py_file):
            os.remove(self.py_file)
            print(f"{Fore.MAGENTA}Removed file: {self.py_file}{Style.RESET_ALL}")
        if os.path.exists(self.meta_yaml):
            os.remove(self.meta_yaml)
            print(f"{Fore.MAGENTA}Removed file: {self.meta_yaml}{Style.RESET_ALL}")
        if os.path.exists(self.test_yaml):
            os.remove(self.test_yaml)
            print(f"{Fore.MAGENTA}Removed file: {self.test_yaml}{Style.RESET_ALL}")
        if os.path.exists(self.spec_file):
            os.remove(self.spec_file)
            print(f"{Fore.MAGENTA}Removed file: {self.spec_file}{Style.RESET_ALL}")
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

        print(f"Analyzing Tokens {self.masterfile}")
        errors = self._analyze_tokens()
        if errors > 0:
            print(f"{Fore.RED}{errors} error{'s' if errors>1 else ''} occurred, Analyzing Tokens failed{Style.RESET_ALL}")
            return
        print(f"{Fore.GREEN}All Tokens valid{Style.RESET_ALL}")

        print(f"Converting Tokens {self.masterfile}")
        errors = self._convert_tokens()
        if errors > 0:
            print(f"{Fore.RED}{errors} error{'s' if errors>1 else ''} occurred, Converting Tokens failed{Style.RESET_ALL}")
            return
        print(f"{Fore.GREEN}All Tokens converted{Style.RESET_ALL}")

        print(f"Creating Test-Yaml-File: {self.test_yaml}")
        #todo: check encoding
        #if encoding="utf-8" => 'ä' turns into 'Ã¤'
        #with open(self.test_yaml, "w", encoding="utf-8") as file:
        with open(self.test_yaml, "w") as file:
            file.write("\n".join(self.contents))
        print(f"{Fore.GREEN}Test-Yaml-File created{Style.RESET_ALL}")

        print(f"Validating TestSuite")
        try:
            _test = parse_test_file(self.test_yaml)
            #print(_test)
        except ValidationError as e:
            print(f"{Fore.RED}TestSuite could not be validated{Style.RESET_ALL}")
            print(e)
            return
        print(f"{Fore.GREEN}TestSuite validated{Style.RESET_ALL}")

        print(f"Creating Reference-File: {self.py_file}")
        with open(self.py_file, "w") as file:
            file.write("".join(self.lines))
        print(f"{Fore.GREEN}Reference-File created{Style.RESET_ALL}")
        #todo: validate reference-file for obvious errors, linting, ...!!!

        print(f"Creating Specification-File: {self.spec_file}")
        with open(self.spec_file, "w") as file:
            file.write(DEFAULT_SPECIFICATION)
        print(f"{Fore.GREEN}Specification-File created{Style.RESET_ALL}")

        print(f"Creating Meta-Yaml-File: {self.meta_yaml}")
        with open(self.meta_yaml, "w") as file:
            file.write("\n".join(self.meta))
        print(f"{Fore.GREEN}Meta-Yaml-File created{Style.RESET_ALL}")

        print(f"Preparing Local Test Directory: {self.localTestdir}")
        self._prepare_local_test_directories()

        time.sleep(0.0001)
        end = round(time.time() - start, 3)
        print(f"{Fore.GREEN}Conversion successful, duration {end} seconds{Style.RESET_ALL}")
        self.conv_error = False

    def _analyze_tokens(self):
        with open(self.masterfile, "r") as file:
            masterlines = file.readlines()
        #lines = [l for l in lines if l.startswith("#$")]
        self.lines = []
        self.tokens = []
        errors = 0
        for idx, line in enumerate(masterlines):
            if line.startswith("#$"):
                line = line.rstrip()[2:]
                try:
                    token, argument, value = self._extract_from_line(line)
                    self.tokens.append((token, argument, value, idx, line))
                except Exception as e:
                    errors = errors + 1
                    print(f"{Fore.RED}ERROR in Line {idx+1}{Style.RESET_ALL}: {line}")
                    print(e)
            elif not line.startswith("##"):
                self.lines.append(line)
        return errors

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
        if argument == "qualification":
            if value not in QualificationEnum._member_names_:
                raise Exception(f"value invalid: {Fore.MAGENTA}{value}{Style.RESET_ALL}\nchoose from: {QualificationEnum._member_names_}")
        if token != TokenEnum.TESTSUITE and argument == "type":
            if value not in TypeEnum._member_names_:
                raise Exception(f"value invalid: {Fore.MAGENTA}{value}{Style.RESET_ALL}\nchoose from: {TypeEnum._member_names_}")
        return token, argument, value
    
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

    def _convert_tokens(self):
        self.addfiles = []
        testsuite = DEFAULTS["testsuite"]
        properties = DEFAULTS["properties"]
        tests = []
        curr_test = -1
        curr_subtest = -1
        errors = 0
        for idx, token in enumerate(self.tokens):
            token, argument, value, idx, line = token
            if token == TokenEnum.TESTSUITE:
                if argument not in VALID_PROPS_TESTSUITE:
                    errors = errors + 1
                    print(f"{Fore.RED}ERROR in Line {idx+1}{Style.RESET_ALL}: {line}\nargument invalid: {Fore.MAGENTA}{argument}{Style.RESET_ALL}\nchoose from: {VALID_PROPS_TESTSUITE}")
                else:
                    testsuite[argument] = value
            elif token == TokenEnum.PROPERTY:
                if curr_test == -1:
                    if argument not in VALID_PROPS_TESTCOLLECTION_COMMON:
                        errors = errors + 1
                        print(f"{Fore.RED}ERROR in Line {idx+1}{Style.RESET_ALL}: {line}\nargument invalid: {Fore.MAGENTA}{argument}{Style.RESET_ALL}\nchoose from: {VALID_PROPS_TESTCOLLECTION_COMMON}")
                    else:
                        properties[argument] = value
                elif curr_subtest == -1:
                    if argument not in VALID_PROPS_TESTCOLLECTION:
                        errors = errors + 1
                        print(f"{Fore.RED}ERROR in Line {idx+1}{Style.RESET_ALL}: {line}\nargument invalid: {Fore.MAGENTA}{argument}{Style.RESET_ALL}\nchoose from: {VALID_PROPS_TESTCOLLECTION}")
                    else:
                        tests[curr_test][argument] = value
                else:
                    if argument not in VALID_PROPS_TEST:
                        errors = errors + 1
                        print(f"{Fore.RED}ERROR in Line {idx+1}{Style.RESET_ALL}: {line}\nargument invalid: {Fore.MAGENTA}{argument}{Style.RESET_ALL}\nchoose from: {VALID_PROPS_TEST}")
                    else:
                        tests[curr_test]["tests"][curr_subtest][argument] = value
            elif token in (TEST_MAPPING):
                curr_subtest = -1
                curr_test = curr_test + 1
                tests.append({
                    "type": TEST_MAPPING[token],
                    "name": f"{argument}",
                    "entryPoint": f"{self.entrypoint}",
                    "tests": [],
                })
            elif token == TokenEnum.TESTVAR:
                curr_subtest = curr_subtest + 1
                tests[curr_test]["tests"].append({
                    "name": argument,
                })
            elif token == TokenEnum.ADDITIONALFILES:
                files = str(argument).split(":")
                for file in files:
                    f = file.strip()
                    ff = os.path.join(self.scandir, f)
                    ff = os.path.abspath(ff)
                    if os.path.exists(ff):
                        f = ff.replace(self.scandir, ".")
                        if f == ".":
                            errors = errors + 1
                            print(f"{Fore.RED}ERROR: choose files/folders from inside scandir: {self.list_scandir()}{Style.RESET_ALL}")
                        else:
                            self.addfiles.append(f)
                    else:
                        errors = errors + 1
                        print(f"{Fore.RED}ERROR: Additional file/folder does not exist: {f}{Style.RESET_ALL}")

        self.meta = [
            "properties:",
            f"  additionalFiles: [{','.join(self.addfiles)}]",
        ]
        self.contents = []
        for key in testsuite:
            if isinstance(testsuite[key], str):
                self.contents.append(f'{key}: "{testsuite[key]}"')
            else:
                self.contents.append(f"{key}: {testsuite[key]}")
        self.contents.append("properties:")
        for key in properties:
            self.contents.append(f"  {key}: {properties[key]}")
        self.contents.append("  tests:")
        if len(tests) == 0:
            errors = errors + 1
            print(f"{Fore.RED}ERROR no testcollection specified{Style.RESET_ALL}")
        else:
            for idx, test in enumerate(tests):
                found_test = False
                for argument in test:
                    if argument != "tests":
                        prefix = "      " if found_test else "    - "
                        found_test = True
                        self.contents.append(f"{prefix}{argument}: {test[argument]}")
                self.contents.append("      tests:")
                if len(test["tests"]) == 0:
                    errors = errors + 1
                    print(f"{Fore.RED}ERROR at test #{idx+1} '{test['name']}' no subtests specified{Style.RESET_ALL}")
                else:
                    for subtest in test["tests"]:
                        found_subtest = False
                        for argument in subtest:
                            prefix = "          " if found_subtest else "        - "
                            found_subtest = True
                            self.contents.append(f"{prefix}{argument}: {subtest[argument]}")
        return errors

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
        for file in self.addfiles:
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
