import os
from convert import convert_master

if __name__ == "__main__":
    action = None
    #action = "convert"
    #action = "test"

    verbosity = 3 # with full traceback
    verbosity = 0

    scandir = "../ex_master/ex1"
    scandir = "../ex_master/ex2"
    #scandir = "../ex_master/_ex_"

    dir = os.path.dirname(__file__)
    dir = os.path.join(dir, scandir)
    dir = os.path.abspath(dir)
    convert_master(dir, action, verbosity)
