"""This is the doc-string ..."""

import os


class file_reader:
    def readfile(self, filename):
        with open(filename, "r") as file:
            return file.read()


dir = os.path.dirname(__file__)
filename = os.path.abspath(os.path.join(dir, "./data/dat.txt"))
# todo: test errors/warnings
_file_reader = file_reader()
var1 = _file_reader.readfile(filename)
var2 = 2
print(var1)
pass
