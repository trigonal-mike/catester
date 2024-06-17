import os
from run_tests import run_tests, DEFAULT_PYTESTFLAGS
from devflags import get_pytest_flags

# this file is for development purposes only
# facilitates starting local test-examples

def start_tests():
    indent = 2
    catester_verbosity = 0
    # show exit-code if catester_verbosity > 0
    # enable catester-summary if catester_verbosity > 2

    #specification = "../examples/specification.yaml"
    #specification = None
    #test = "../examples/ex2/test2.yaml"
    #test = "../examples/ex2/test_timeout.yaml"
    #test = "../examples/ex2/test_linting.yaml"
    #test = "../examples/ex2/test_structural.yaml"

    #specification = "../ex_master/examples/graphics/localTests/specification.yaml"
    #test = "../ex_master/examples/graphics/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/full/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/full/localTests/_emptySolution/test.yaml"
    #test = "../ex_master/examples/new/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/empty/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/stdout/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/stdin/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/errorbar/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/open/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/malicious/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/blacklist/localTests/_correctSolution/test.yaml"
    specification = "../testrunner/test1-_correctSolution/specification.yaml"
    test = "../testrunner/test1-_correctSolution/test.yaml"

    # construct pytest flags:
    pytestflags = get_pytest_flags(
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
    pytestflags = DEFAULT_PYTESTFLAGS

    dir = os.path.abspath(os.path.dirname(__file__))
    if specification is not None:
        specification = os.path.join(dir, specification)
    test = os.path.join(dir, test)

    run_tests(specification, test, indent, catester_verbosity, pytestflags)

if __name__ == "__main__":
    start_tests()
