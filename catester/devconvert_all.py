import glob
import os
from convert import convert_master
from run_tests import DEFAULT_PYTESTFLAGS

""" settings are explained here: doc/DEVCONVERT.md """

TESTRUNNER_DIR = "../../testrunner"
INITIAL_META = "../../assignments/initial-meta.yaml"
USE_FORMATTER = True
SUPPRESS_OUTPUT = True
CONVERTER_ACTION = None
#CONVERTER_ACTION = 'cleanup'
#CONVERTER_ACTION = 'convert'
#CONVERTER_ACTION = 'test'
CATESTER_VERBOSITY = 0
PYTEST_FLAGS = DEFAULT_PYTESTFLAGS
PYTEST_FLAGS = "-ra,--tb=no,--no-header,--no-summary,-q"

#SEARCH_DIR = "../../assignments"
SEARCH_DIR = "../../assignments/Week01"
#SEARCH_DIR = "../../catester-examples/ex_master/_ex_"
#SEARCH_DIR = "../../catester-examples/ex_master/examples"
#SEARCH_DIR = "../../catester-examples/tokens-test"

if __name__ == "__main__":
    thisdir = os.path.dirname(__file__)
    testrunnerdir = os.path.abspath(os.path.join(thisdir, TESTRUNNER_DIR))
    searchdir = os.path.abspath(os.path.join(thisdir, SEARCH_DIR))
    metayaml = None if INITIAL_META is None else os.path.abspath(os.path.join(thisdir, INITIAL_META))

    masterlist = glob.glob("**/*_master.py", root_dir=searchdir, recursive=True)
    count = len(masterlist)

    def convert_file(file: str):
        return os.path.dirname(os.path.abspath(os.path.join(searchdir, file)))

    masterlist = [convert_file(e) for e in masterlist]

    print(f"{count} Master Files found")
    print(f"starting conversion")

    assignmentsdir = searchdir

    for index, scandir in enumerate(masterlist):
        print(f"#{index+1}: converting {scandir}")
        convert_master(scandir, testrunnerdir, assignmentsdir, CONVERTER_ACTION, CATESTER_VERBOSITY, PYTEST_FLAGS, metayaml, USE_FORMATTER, SUPPRESS_OUTPUT)

    print(f"conversion finished")
