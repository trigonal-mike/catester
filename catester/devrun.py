import os
from run_tests import run_tests, DEFAULT_PYTESTFLAGS

# this file is for development purposes only
# facilitates starting local test-examples

def start_tests():
    #specification = "../examples/specification.yaml"
    specification = None
    test = "../examples/ex2/test2.yaml"
    #test = "../examples/ex2/test_timeout.yaml"
    #test = "../examples/ex2/test_linting.yaml"
    #test = "../examples/ex2/test_structural.yaml"

    specification = "../ex_master/examples/graphics/localTests/specification.yaml"
    test = "../ex_master/examples/graphics/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/full/localTests/_correctSolution/test.yaml"
    #test = "../ex_master/examples/full/localTests/_emptySolution/test.yaml"
    #test = "../ex_master/examples/new/localTests/_emptySolution/test.yaml"
    indent = 2

    #catester-verbosity
    verbosity = 0
    # show exit-code, set verbosity > 0
    #verbosity = 1
    # enable catester summary, set verbosity > 2
    #verbosity = 3

    #https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags
    flags = [
        # report all but PASSED:
        "-ra",
        # report all incl PASSED:
        #"-rA",

        #"--fixtures",
        #"--collect-only",
        #"--showlocals", #never show locals :-)
        #"--tb=line",
        #"--tb=no",
        #"--tb=auto",
        #"--full-trace",
        #"--verbose",
        #"--verbosity=4",
        #"-vv",
        #"-q",
        #"-x",
        #"--no-header",
        #"--no-summary",
    ]
    pytestflags = ",".join(flags)

    #minimal:
    pytestflags = "-ra,--tb=no,--no-header,--no-summary,-q"

    #very quiet:
    pytestflags = "--no-header,--no-summary,-q"

    #most quiet:
    pytestflags = "--no-header,--no-summary,-qq"

    #no header:
    pytestflags = "-ra,--tb=no,--no-header,-q"

    # report all, verbose, with traceback:
    #pytestflags = "-rA,--tb=line,-vvv"

    # default:
    #pytestflags = DEFAULT_PYTESTFLAGS

    dir = os.path.abspath(os.path.dirname(__file__))
    if specification is not None:
        specification = os.path.join(dir, specification)
    test = os.path.join(dir, test)

    run_tests(specification, test, indent, verbosity, pytestflags)

if __name__ == "__main__":
    start_tests()
