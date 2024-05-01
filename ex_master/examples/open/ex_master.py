import os
import numpy as np

class file_reader:
    def readfile_open(self, filename):
        with open(filename, "r") as file:
            return file.read()

    def readfile_numpy_loadtxt(self, filename):
        return np.loadtxt(filename)

    def readfile_numpy_genfromtxt(self, filename):
        return np.genfromtxt(filename)

filename_allowed = "./dat.txt"
filename_not_allowed = "i:/PYTHON/catester/ex_master/examples/open/dat.txt"
_file_reader = file_reader()
var1 = _file_reader.readfile_open(filename_allowed)
var2 = _file_reader.readfile_numpy_loadtxt(filename_allowed)
var3 = _file_reader.readfile_numpy_genfromtxt(filename_allowed)
#var1 = _file_reader.readfile_open(filename_not_allowed)
#var2 = _file_reader.readfile_numpy_loadtxt(filename_not_allowed)
#var3 = _file_reader.readfile_numpy_genfromtxt(filename_not_allowed)

print(var1)
print(var2)
print(var3)

#$META additionalFiles ./dat.txt

#$VARIABLETEST variables test-1
#$TESTVAR var1
#$TESTVAR var2
#$TESTVAR var3
