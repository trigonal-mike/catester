import os
from convert import convert_master
from run_tests import DEFAULT_PYTESTFLAGS

if __name__ == "__main__":
    action = None
    #action = "convert"
    #action = "test"
    #action = "cleanup"

    #catester-verbosity
    verbosity = 0

    #test flags:
    #https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags
    pytestflags = DEFAULT_PYTESTFLAGS
    #pytestflags = "-rA"
    #pytestflags = "-ra,--tb=no,--no-header,-q"

    #scandir = "../ex_master/_ex_/1"
    #scandir = "../ex_master/_ex_/2"
    #scandir = "../ex_master/_ex_/3"
    #scandir = "../ex_master/_ex_/4"
    #scandir = "../ex_master/_ex_/5"
    #scandir = "../ex_master/_ex_/15"
    #scandir = "../ex_master/_ex_/14"
    #scandir = "../ex_master/_ex_/17"
    #scandir = "../ex_master/_ex_/ue33"
    scandir = "../ex_master/_ex_/Week03/Unit01"
    scandir = "../ex_master/_ex_/Week03/Unit02"

    #scandir = "../ex_master/examples/docstring"
    #scandir = "../ex_master/examples/errorbar"
    #scandir = "../ex_master/examples/stdin"
    #scandir = "../ex_master/examples/stdout"
    #scandir = "../ex_master/examples/empty"
    #scandir = "../ex_master/examples/new"
    #scandir = "../ex_master/examples/vector_random"
    #scandir = "../ex_master/examples/graphics"
    #scandir = "../ex_master/examples/minimal"
    #scandir = "../ex_master/examples/full"
    #scandir = "../ex_master/examples/open"
    #scandir = "../ex_master/examples/malicious"
    #scandir = "../ex_master/examples/blacklist"
    #scandir = "../../progphys-py.2023.basis1"

    metayaml = "../ex_master/example-init-meta.yaml"

    #formatter = False
    formatter = True

    dir = os.path.dirname(__file__)
    scandir = os.path.abspath(os.path.join(dir, scandir))
    metayaml = os.path.abspath(os.path.join(dir, metayaml))

    testrunnerdir = "../testrunner"
    testrunnerdir = os.path.abspath(os.path.join(dir, testrunnerdir))
    assignmentsdir = "../ex_master/_ex_"
    assignmentsdir = os.path.abspath(os.path.join(dir, assignmentsdir))

    convert_master(scandir, testrunnerdir, assignmentsdir, action, verbosity, pytestflags, metayaml, formatter)
    #convert_master(scandir, action, verbosity, None)
