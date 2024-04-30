import os
import numpy as np
from pathlib import PurePath
from distutils.sysconfig import get_python_lib

class Mocker:
    def __init__(self) -> None:
        self.open = open
        self.loadtxt = np.loadtxt
        self.genfromtxt = np.genfromtxt

    def has_permission(self, filename):
        path_lib = get_python_lib()
        path_cwd = os.getcwd()
        p = PurePath(filename)
        return p.is_relative_to(path_cwd) or p.is_relative_to(path_lib)

    def mock_open(self, name, mode, **kwargs):
        if not self.has_permission(name):
            raise PermissionError(f"open not allowed: location: `{name}`")
        return self.open(name, mode, **kwargs)  

    def mock_loadtxt(self, name, **kwargs):
        if not self.has_permission(name):
            raise PermissionError(f"np.loadtxt not allowed: location: `{name}`")
        return self.loadtxt(name, **kwargs)  

    def mock_genfromtxt(self, name, **kwargs):
        if not self.has_permission(name):
            raise PermissionError(f"np.genfromtxt not allowed: location: `{name}`")
        return self.genfromtxt(name, **kwargs)  
