import glob
import os
import shutil
import subprocess
from colorama import Fore, Back, Style

DEFAULT_SPECIFICATION = """testInfo:
  studentDirectory: "student"
  referenceDirectory: "../_reference"
  outputDirectory: "output"
"""

LOCAL_TEST_DIRECTORIES = [
    "_reference",
    "correctSolution",
    "emptySolution",
    "wrongSolution",
]

class LocalTester:
    def __init__(self, scandir: str):
        self.scandir = scandir

    def prepare(self):
        print(f"### Preparing {self.scandir}")
        localTestdir = "localTests"
        localTestdir = os.path.join(self.scandir, localTestdir)
        if not os.path.exists(localTestdir):
            os.makedirs(localTestdir)
            print(f"### Creating directory: {localTestdir}")
        else:
            print(f"### Directory already exists: {localTestdir}")

        flist = glob.glob("*_master.py")
        if len(flist) == 0:
            print(f"No file named *_master.py in directory: {self.scandir}")
            return
        entrypoint = os.path.basename(flist[0]).replace("_master", "")
        py_file = os.path.join(self.scandir, entrypoint)
        test_file = os.path.join(self.scandir, "test.yaml")
        spec_file = os.path.join(self.scandir, "specification.yaml")
        with open(spec_file, "w", encoding="utf-8") as file:
            file.write(DEFAULT_SPECIFICATION)
        if not os.path.exists(test_file):
            print(f"### test.yaml does not exist in directory: {self.scandir}")
            return

        self.py_file = py_file
        self.test_file = test_file
        self.spec_file = spec_file
        self.localTestdir = localTestdir
        for directory in LOCAL_TEST_DIRECTORIES:
            self.init_local_test_dir(directory)

    def init_local_test_dir(self, directory: str):
        isref = directory.startswith("_")
        directory = os.path.join(self.localTestdir, directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"### Creating directory: {directory}")
        else:
            print(f"### Directory already exists: {directory}")
            print(f"### Skipping: {directory}")
            return
        if isref:
            shutil.copy(self.py_file, directory)
        else:
            shutil.copy(self.test_file, directory)
            #shutil.copy(self.spec_file, directory)
            student_directory = os.path.join(directory, "student")
            os.makedirs(student_directory, exist_ok=True)
            shutil.copy(self.py_file, student_directory)

    def run_local_tests(self):
        print(f"### Running local tests: {self.localTestdir}")
        directories = [ f.path for f in os.scandir(self.localTestdir) if f.is_dir() and not f.path.endswith("_reference") ]
        for idx, directory in enumerate(directories):
            print()
            print(f"{Back.MAGENTA}### Running local test #{idx+1}{Style.RESET_ALL}")
            print(f"{Back.MAGENTA}### Directory: {directory}{Style.RESET_ALL}")
            self.run_local_test(directory)

    def run_local_test(self, directory):
        os.chdir(directory)
        dir = os.path.dirname(__file__)
        entry_file = os.path.join(dir, "../run_tests.py")
        entry_file = os.path.abspath(entry_file)
        retcode = subprocess.run(f"python {entry_file} --specification={self.spec_file}", shell=True)
