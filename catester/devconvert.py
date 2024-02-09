import os
from convert import convert_master

if __name__ == "__main__":
    action = None
    #action = "convert"
    #action = "test"
    #action = "cleanup"

    verbosity = 3 # with full traceback
    verbosity = 0

    scandir = "../ex_master/ex1"
    scandir = "../ex_master/ex2"
    #scandir = "../ex_master/_ex_"

    metayaml = "./metayaml/meta-template.yaml"

    dir = os.path.dirname(__file__)
    scandir = os.path.abspath(os.path.join(dir, scandir))
    metayaml = os.path.abspath(os.path.join(dir, metayaml))
    convert_master(scandir, action, verbosity, metayaml)
