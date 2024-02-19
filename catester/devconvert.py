import os
from convert import convert_master

if __name__ == "__main__":
    action = None
    #action = "convert"
    #action = "test"
    #action = "cleanup"

    verbosity = 3 # with full traceback
    verbosity = 0

    #scandir = "../ex_master/_ex_/1"
    #scandir = "../ex_master/_ex_/2"
    #scandir = "../ex_master/_ex_/3"

    scandir = "../ex_master/examples/minimal"
    scandir = "../ex_master/examples/full"
    #scandir = "../../progphys-py.2023.basis1"

    metayaml = "../ex_master/example-init-meta.yaml"

    #formatter = False
    formatter = True

    dir = os.path.dirname(__file__)
    scandir = os.path.abspath(os.path.join(dir, scandir))
    metayaml = os.path.abspath(os.path.join(dir, metayaml))
    convert_master(scandir, action, verbosity, metayaml, formatter)
    #convert_master(scandir, action, verbosity, None)
