import os
from convert import convert_master

if __name__ == "__main__":
    scandir = "../ex_master/ex1"
    #scandir = "../ex_master/ex2"
    dir = os.path.dirname(__file__)
    dir = os.path.join(dir, scandir)
    dir = os.path.abspath(dir)
    convert_master(dir)
