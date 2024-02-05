import glob
import os
import time
import shutil
import subprocess
from colorama import Fore, Back, Style
from enum import Enum
from pydantic import ValidationError
from model import TypeEnum, QualificationEnum
from model import parse_test_file
from .enums import PropertyEnum, SubTestEnum, TestEnum, TestSuiteEnum, TokenEnum

DEFAULT_SPECIFICATION = """testInfo:\n  referenceDirectory: "../_reference"\n"""

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
        self.test_yaml = os.path.join(scandir, "test.yaml")
        self.spec_file = os.path.join(self.scandir, "specification.yaml")
        self.localTestdir = os.path.join(self.scandir, "localTests")
        self.ready = True

    def convert(self):
        if not self.ready:
            print(f"{Fore.RED}ERROR Conversion, directory invalid: {self._scan_dir}{Style.RESET_ALL}")
        print(f"### Conversion started")
        start = time.time()

        print(f"### Analyzing {self.masterfile}")
        self._analyze_master()
        print(f"### Creating TestSuite: {self.test_yaml}")
        self._write_testsuite()
        print(f"### Validating TestSuite")
        self._validate_yaml()
        print(f"### Creating Reference: {self.py_file}")
        self._write_reference()
        print(f"### Creating Specification: {self.spec_file}")
        self._write_specification()
        print(f"### Preparing Local Test Directory: {self.localTestdir}")
        self._prepare_local_test_directories()

        time.sleep(0.00000000000001)
        end = round(time.time() - start, 3)
        print(f"### Conversion finished, duration {end} seconds")

    def _analyze_master(self):
        with open(self.masterfile, "r") as file:
            masterlines = file.readlines()
        #lines = [l for l in lines if l.startswith("#$")]
        lines = []
        tokens = []
        error = False
        for idx, line in enumerate(masterlines):
            if line.startswith("#$"):
                line = line.rstrip()[2:]
                try:
                    token, argument, value = self._extract_from_line(line)
                    tokens.append((token, argument, value))
                except Exception as e:
                    error = True
                    print(f"{Fore.RED}ERROR in Line {idx+1}{Style.RESET_ALL}: {line}")
                    print(e)
                    print()
            else:
                lines.append(line)
        if error:
            print(f"{Fore.RED}some errors occurred, writing of yaml file failed{Style.RESET_ALL}")
        else:
            self.tokens = tokens
            self.lines = lines

    def _extract_from_line(self, line: str):
        if len(line) == 0:
            raise Exception("Line too short")
        arr = line.split(" ", 1)
        token = arr[0]
        if token not in TokenEnum._member_names_:
            raise Exception(f"token invalid")
        if len(arr) == 1:
            raise Exception("no argument specified")
        if token == TokenEnum.VARIABLE or token == TokenEnum.GRAPHICS:
            return token, arr[1], None
        
        arr = arr[1].split(":", 1)
        if len(arr) == 1:
            raise Exception("no value specified")
        argument = arr[0]
        value = arr[1].strip()
        if token == TokenEnum.TESTSUITE:
            if argument not in TestSuiteEnum._member_names_:
                raise Exception(f"TESTSUITE argument invalid: {Fore.RED}{argument}{Style.RESET_ALL}\nchoose from: {TestSuiteEnum._member_names_}")
        elif token == TokenEnum.PROPERTY:
            if argument not in PropertyEnum._member_names_:
                raise Exception(f"PROPERTY argument invalid: {Fore.RED}{argument}{Style.RESET_ALL}\nchoose from: {PropertyEnum._member_names_}")
        elif token == TokenEnum.TEST:
            if argument not in TestEnum._member_names_:
                raise Exception(f"TEST argument invalid: {Fore.RED}{argument}{Style.RESET_ALL}\nchoose from: {TestEnum._member_names_}")
        elif token == TokenEnum.SUBTEST:
            if argument not in SubTestEnum._member_names_:
                raise Exception(f"SUBTEST argument invalid: {Fore.RED}{argument}{Style.RESET_ALL}\nchoose from: {SubTestEnum._member_names_}")
        if token == TokenEnum.PROPERTY or token == TokenEnum.TEST or token == TokenEnum.SUBTEST:
            if argument == TestEnum.type:
                if value not in TypeEnum._member_names_:
                    raise Exception(f"TYPE value invalid: {Fore.RED}{value}{Style.RESET_ALL}\nchoose from: {TypeEnum._member_names_}")
            elif argument == TestEnum.qualification:
                if value not in QualificationEnum._member_names_:
                    raise Exception(f"QUALIFICATION value invalid: {Fore.RED}{value}{Style.RESET_ALL}\nchoose from: {QualificationEnum._member_names_}")
        return token, argument, value

    def _write_testsuite(self):
        if not hasattr(self, "tokens"):
            return        
        contents = []
        testsuite = {}
        properties = {}
        tests = []
        xxx = ""
        curr_test = -1
        curr_subtest = -1
        for idx, token in enumerate(self.tokens):
            token, argument, value = token
            if token == TokenEnum.TESTSUITE:
                testsuite[argument] = value
            elif token == TokenEnum.PROPERTY:
                properties[argument] = value
            elif token in (TokenEnum.VARIABLE, TokenEnum.GRAPHICS):
                if xxx != token:
                    xxx = token
                    curr_subtest = 0
                    curr_test = curr_test + 1
                    tests.append({
                        "name": f"Test {curr_test+1}",
                        "entryPoint": f"{self.entrypoint}",
                        "type": TypeEnum.variable if token == TokenEnum.VARIABLE else TypeEnum.graphics,
                        "tests": [
                            {
                                "name": argument,
                            }
                        ],
                    })
                else:
                    curr_subtest = curr_subtest + 1
                    tests[curr_test]["tests"].append({
                        "name": argument,
                    })
            elif token == TokenEnum.TEST:
                if curr_test >= 0:
                    tests[curr_test][argument] = value
            elif token == TokenEnum.SUBTEST:
                if curr_test >= 0 and curr_subtest >= 0:
                    tests[curr_test]["tests"][curr_subtest][argument] = value

        for key in testsuite:
            contents.append(f"{key}: {testsuite[key]}")

        contents.append("properties:")
        for key in properties:
            contents.append(f"  {key}: {properties[key]}")
        contents.append("  tests:")

        for test in tests:
            found_test = False
            for argument in test:
                if argument != "tests":
                    prefix = "      " if found_test else "    - "
                    found_test = True
                    contents.append(f"{prefix}{argument}: {test[argument]}")
            contents.append("      tests:")
            for subtest in test["tests"]:
                found_subtest = False
                for argument in subtest:
                    prefix = "          " if found_subtest else "        - "
                    found_subtest = True
                    contents.append(f"{prefix}{argument}: {subtest[argument]}")

        content = "\n".join(contents)
        with open(self.test_yaml, "w", encoding="utf-8") as file:
            file.write(content)

    def _write_reference(self):
        if not hasattr(self, "lines"):
            return
        with open(self.py_file, "w", encoding="utf-8") as file:
            file.write("".join(self.lines))

    def _write_specification(self):
        with open(self.spec_file, "w", encoding="utf-8") as file:
            file.write(DEFAULT_SPECIFICATION)

    def _validate_yaml(self):
        try:
            _test = parse_test_file(self.test_yaml)
            #print(_test)
        except ValidationError as e:
            print("YAML File could not be validated")
            print(e)

    def _prepare_local_test_directories(self):
        if not os.path.exists(self.localTestdir):
            os.makedirs(self.localTestdir)
            print(f"### Creating directory: {self.localTestdir}")
        else:
            print(f"{Fore.CYAN}### Directory already exists:{Style.RESET_ALL} {self.localTestdir}")
        if not os.path.exists(self.test_yaml):
            print(f"### test.yaml does not exist in directory: {self.scandir}")
            return
        for directory in LOCAL_TEST_DIRECTORIES._member_names_:
            self._init_local_test_dir(directory)

    def _init_local_test_dir(self, directory: str):
        isref = directory == LOCAL_TEST_DIRECTORIES._reference
        isempty = directory == LOCAL_TEST_DIRECTORIES._emptySolution
        directory = os.path.join(self.localTestdir, directory)
        student_directory = os.path.join(directory, "student")

        if os.path.exists(directory):
            print(f"{Fore.RED}### Removing directory: {directory}{Style.RESET_ALL}")
            shutil.rmtree(directory)
        print(f"### Creating directory: {directory}")
        os.makedirs(directory)

        if isref:
            shutil.copy(self.py_file, directory)
        else:
            shutil.copy(self.test_yaml, directory)
            os.makedirs(student_directory)
            if not isempty:
                shutil.copy(self.py_file, student_directory)

    def run_local_tests(self):
        print(f"### Running local tests: {self.localTestdir}")
        directories = [ f.path for f in os.scandir(self.localTestdir) if f.is_dir() and not f.path.endswith("_reference") ]
        for idx, directory in enumerate(directories):
            print()
            print(f"{Back.MAGENTA}### Running local test #{idx+1}{Style.RESET_ALL}")
            print(f"{Back.MAGENTA}### Directory: {directory}{Style.RESET_ALL}")
            self._run_local_test(directory)

    def _run_local_test(self, directory):
        os.chdir(directory)
        dir = os.path.dirname(__file__)
        run_tests_py = os.path.join(dir, "../run_tests.py")
        run_tests_py = os.path.abspath(run_tests_py)
        retcode = subprocess.run(f"python {run_tests_py} --specification={self.spec_file}", shell=True)
