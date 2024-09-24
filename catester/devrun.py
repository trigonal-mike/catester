import os
from run_tests import run_tests, DEFAULT_PYTESTFLAGS
from devflags import get_pytest_flags

""" this file is for development purposes only,
facilitates starting local test-examples,
can be used for debugging the testing, because breakpoints can be set,
with devconvert.py breakpoints cannot be set """

# CATESTER_VERBOSITY: verbosity level for catester
# 0 ... no additional output
# 1 ... show exit-code (and additional output, ONLY if PYTEST_FLAGS are without "--no-summary" flag)
CATESTER_VERBOSITY = 0

# REPORT_INDENT: indentation of the generated json report file
REPORT_INDENT = 2

# SPECIFICATION: yaml file containing test specification
# MUST be relative to this file (devrun.py)
SPECIFICATION_YAML = "../../testrunner/test1-_correctSolution/specification.yaml"

# TEST_YAML: yaml file containing test instructions
# MUST be relative to this file (devrun.py)
TEST_YAML = "../../testrunner/test1-_correctSolution/test.yaml"

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
    dir = os.path.abspath(os.path.dirname(__file__))

    # construct absulute paths for the tester
    specification = os.path.join(dir, SPECIFICATION_YAML)
    test = os.path.join(dir, TEST_YAML)

    # run the tester
    run_tests(specification, test, REPORT_INDENT, CATESTER_VERBOSITY, PYTEST_FLAGS)
