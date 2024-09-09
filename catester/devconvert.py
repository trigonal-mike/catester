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

    #ex_master/_ex_:
    #scandir = "../../catester-examples/ex_master/_ex_/1"
    #scandir = "../../catester-examples/ex_master/_ex_/2"
    #scandir = "../../catester-examples/ex_master/_ex_/3"
    #scandir = "../../catester-examples/ex_master/_ex_/4"
    #scandir = "../../catester-examples/ex_master/_ex_/5"
    #scandir = "../../catester-examples/ex_master/_ex_/6"
    #scandir = "../../catester-examples/ex_master/_ex_/7"
    #scandir = "../../catester-examples/ex_master/_ex_/8"
    #scandir = "../../catester-examples/ex_master/_ex_/9"
    #scandir = "../../catester-examples/ex_master/_ex_/10"
    #scandir = "../../catester-examples/ex_master/_ex_/11"
    #scandir = "../../catester-examples/ex_master/_ex_/12"
    #scandir = "../../catester-examples/ex_master/_ex_/13"
    #scandir = "../../catester-examples/ex_master/_ex_/14"
    #scandir = "../../catester-examples/ex_master/_ex_/15"
    #scandir = "../../catester-examples/ex_master/_ex_/16"
    #scandir = "../../catester-examples/ex_master/_ex_/17"

    #ex_master/examples:
    #scandir = "../../catester-examples/ex_master/examples/aaa/bbb/ccc"
    #scandir = "../../catester-examples/ex_master/examples/basic"
    #scandir = "../../catester-examples/ex_master/examples/blacklist"
    #scandir = "../../catester-examples/ex_master/examples/datetime"
    #scandir = "../../catester-examples/ex_master/examples/docstring"
    #scandir = "../../catester-examples/ex_master/examples/empty"
    #scandir = "../../catester-examples/ex_master/examples/errorbar"
    #scandir = "../../catester-examples/ex_master/examples/existance"
    #scandir = "../../catester-examples/ex_master/examples/full"
    #scandir = "../../catester-examples/ex_master/examples/graphics"
    #scandir = "../../catester-examples/ex_master/examples/linting"
    #scandir = "../../catester-examples/ex_master/examples/matplot"
    #scandir = "../../catester-examples/ex_master/examples/malicious"
    #scandir = "../../catester-examples/ex_master/examples/minimal"
    #scandir = "../../catester-examples/ex_master/examples/new"
    #scandir = "../../catester-examples/ex_master/examples/open"
    #scandir = "../../catester-examples/ex_master/examples/pandas"
    #scandir = "../../catester-examples/ex_master/examples/pi_int"
    #scandir = "../../catester-examples/ex_master/examples/python_types"
    #scandir = "../../catester-examples/ex_master/examples/random"
    #scandir = "../../catester-examples/ex_master/examples/stdin"
    #scandir = "../../catester-examples/ex_master/examples/stdout"
    #scandir = "../../catester-examples/ex_master/examples/strings"
    #scandir = "../../catester-examples/ex_master/examples/structural"
    #scandir = "../../catester-examples/ex_master/examples/timeout"
    #scandir = "../../catester-examples/ex_master/examples/typecheck"
    #scandir = "../../catester-examples/ex_master/examples/vector_random"
    #scandir = "../../catester-examples/ex_master/examples/Week03/Unit01"
    scandir = "../../catester-examples/ex_master/examples/Week03/Unit02"

    metayaml = "../../catester-examples/ex_master/example-init-meta.yaml"

    dir = os.path.dirname(__file__)
    scandir = os.path.abspath(os.path.join(dir, scandir))
    metayaml = os.path.abspath(os.path.join(dir, metayaml))

    testrunnerdir = "../testrunner"
    testrunnerdir = os.path.abspath(os.path.join(dir, testrunnerdir))
    #assignmentsdir = "../../catester-examples/ex_master/_ex_"
    assignmentsdir = "../../catester-examples/ex_master/examples"
    assignmentsdir = os.path.abspath(os.path.join(dir, assignmentsdir))

    formatter = True #or false (if formatting of files is not required)

    convert_master(scandir, testrunnerdir, assignmentsdir, action, verbosity, pytestflags, metayaml, formatter)
