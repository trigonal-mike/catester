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
    pytestflags = "-rA,--tb=no,--no-header,--no-summary,-q"
    pytestflags = "-ra,--tb=no,--no-header,-q"

    #scandir = "../ex_master/_ex_/1"
    #scandir = "../ex_master/_ex_/2"
    #scandir = "../ex_master/_ex_/3"

    scandir = "../ex_master/examples/stdout"
    #scandir = "../ex_master/examples/empty"
    #scandir = "../ex_master/examples/new"
    #scandir = "../ex_master/examples/vector_random"
    #scandir = "../ex_master/examples/graphics"
    #scandir = "../ex_master/examples/minimal"
    #scandir = "../ex_master/examples/full"
    #scandir = "../../progphys-py.2023.basis1"

    metayaml = "../ex_master/example-init-meta.yaml"

    #formatter = False
    formatter = True

    testdirs = "all"
    #testdirs = "none"
    #testdirs = "correct"
    #testdirs = "empty"

    dir = os.path.dirname(__file__)
    scandir = os.path.abspath(os.path.join(dir, scandir))
    metayaml = os.path.abspath(os.path.join(dir, metayaml))
    convert_master(scandir, action, verbosity, pytestflags, metayaml, formatter, testdirs)
    #convert_master(scandir, action, verbosity, None)
