import os
import time
from colorama import Fore, Back, Style
from pydantic import ValidationError
from model import TypeEnum, QualificationEnum
from model import parse_test_file
from .enums import PropertyEnum, SubTestEnum, TestEnum, TestSuiteEnum, TokenEnum

class Converter:
    def __init__(self, filename: str):
        dirname = os.path.dirname(filename)
        output = os.path.join(dirname, "test.yaml")
        entrypoint = os.path.basename(filename).replace("_master", "")
        reference = os.path.join(dirname, entrypoint)

        self.filename = filename
        self.dirname = dirname
        self.output = output
        self.entrypoint = entrypoint
        self.reference = reference

    def convert(self):
        print(f"### Converting {self.filename}")
        start = time.time()
        self._analyze_master()
        self._write_yaml()
        self._validate_yaml()
        time.sleep(0.00000000000001)
        end = round(time.time() - start, 3)
        print(f"### Converting finished, duration {end} seconds")

    def _analyze_master(self):
        with open(self.filename, "r") as file:
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

    def _write_yaml(self):
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
        with open(self.output, "w", encoding="utf-8") as file:
            file.write(content)
        with open(self.reference, "w", encoding="utf-8") as file:
            file.write("".join(self.lines))

    def _validate_yaml(self):
        try:
            _test = parse_test_file(self.output)
            #print(_test)
        except ValidationError as e:
            print("YAML File could not be validated")
            print(e)
