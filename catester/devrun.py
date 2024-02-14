import os
from run_tests import run_tests

# this file is for development purposes only
# facilitates starting local test-examples

def start_tests():
    #specification = "../examples/specification.yaml"
    specification = None
    #test = "../examples/ex1/test1.yaml"
    test = "../examples/ex2/test_timeout.yaml"
    test = "../examples/ex2/test_linting.yaml"
    #test = "../examples/ex2/test_structural.yaml"

    specification = "../ex_master/examples/full/specification.yaml"
    test = "../ex_master/examples/full/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/full/localTests/_emptySolution/test.yaml"
    indent = 2
    verbosity = 0

    dir = os.path.abspath(os.path.dirname(__file__))
    if specification is not None:
        specification = os.path.join(dir, specification)
    test = os.path.join(dir, test)

    run_tests(specification, test, indent, verbosity)

if __name__ == "__main__":
    start_tests()
