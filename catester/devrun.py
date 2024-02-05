import os
from run_tests import run_tests

# this file is for development purposes only
# facilitates starting local test-examples

def start_tests():
    specification = "../examples/specification.yaml"
    #specification = None
    #test = "../examples/ex1/test5.yaml"
    test = "../examples/ex2/test2.yaml"
    #specification = "../ex_master/ex1/localTests/correctSolution/specification.yaml"
    #specification = "../ex_master/ex1/localTests/emptySolution/specification.yaml"
    #test = "../ex_master/ex1/localTests/correctSolution/test.yaml"
    #test = "../ex_master/ex1/localTests/emptySolution/test.yaml"
    indent = 2
    verbosity = 0

    dir = os.path.abspath(os.path.dirname(__file__))
    if specification is not None:
        specification = os.path.join(dir, specification)
    test = os.path.join(dir, test)

    run_tests(specification, test, indent, verbosity)

if __name__ == "__main__":
    start_tests()
