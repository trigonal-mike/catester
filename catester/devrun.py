import os
from run_tests import run_tests, DEFAULT_PYTESTFLAGS
from devflags import get_pytest_flags

""" this file is for development purposes only, facilitates starting local test-examples,
it can be used for debugging the testing, because breakpoints can be set for example
in ./tests/conftest.py or ./tests/test_class.py """ 

# CATESTER_VERBOSITY: verbosity level for catester
# 0 ... no additional output
# 1 ... show exit-code (and additional output, ONLY if PYTEST_FLAGS are without "--no-summary" flag)
CATESTER_VERBOSITY = 0

# REPORT_INDENT: indentation of the generated json report file
REPORT_INDENT = 2

# SOLUTION_DIRECTORY: directory containing test.yaml and specification.yaml
# MUST be relative to this file (devrun.py)
SOLUTION_DIRECTORY = "../../testrunner/_Week01_01_math_constants/_correctSolution"
#SOLUTION_DIRECTORY = "../../testrunner/_Week01_01_math_constants/_emptySolution"
#SOLUTION_DIRECTORY = "../../testrunner/_Week01_01_math_constants/studentSolution"
#SOLUTION_DIRECTORY = "../../testrunner/_variable-7/_correctSolution"

# PYTEST_FLAGS: test flags for pytest
# https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags
# either construct the pytest flags with helper function:
PYTEST_FLAGS = get_pytest_flags(
    reportPassed = False,
    withHeader = False,
    withSummary = False,
    withTraceback = True,
    fullTraceback = False,
    collectOnly = False,
    showFixtures = False,
    showLocals = False,
    exitOnFirstError = False,
    verbosity = -1
)
# or use default flags:
PYTEST_FLAGS = DEFAULT_PYTESTFLAGS

if __name__ == "__main__":
    # get directory of this file 
    thisdir = os.path.dirname(__file__)

    # construct absulute paths for the tester
    solution_dir = os.path.abspath(os.path.join(thisdir, SOLUTION_DIRECTORY))
    specification = os.path.abspath(os.path.join(solution_dir, "specification.yaml"))
    test = os.path.abspath(os.path.join(solution_dir, "test.yaml"))

    # run the tester
    run_tests(specification, test, REPORT_INDENT, CATESTER_VERBOSITY, PYTEST_FLAGS)
