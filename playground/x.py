import os
from matplotlib import pyplot as plt
import numpy as np

def execute_file(filename, namespace):
    with open(filename, "r") as file:
        exec(compile(file.read(), filename, "exec"), namespace)

dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(dir)

#plt.ion()
from _pytest.monkeypatch import MonkeyPatch
mpatch = MonkeyPatch()
mpatch.setattr(plt, "show", lambda: None)

file1 = "./plot1.py"
namespace1 = {}
if os.path.exists(file1):
    execute_file(file1, namespace1)

file2 = "./plot2.py"
namespace2 = {}
if os.path.exists(file2):
    execute_file(file2, namespace2)

var1 = "add(1, 2)"

#x = eval('add(1, 3)', namespace)
#print(x)
name = "figure(1).axes[0].lines[0]._linestyle"
fun2eval = f'globals()["plt"].{name}'
x = eval(fun2eval, namespace1)
print(x)
name = "figure(2).axes[0].lines[0]._linestyle"
fun2eval = f'globals()["plt"].{name}'
x = eval(fun2eval, namespace1)
print(x)
name = "figure(3).axes[0].lines[0]._linestyle"
fun2eval = f'globals()["plt"].{name}'
x = eval(fun2eval, namespace2)
print(x)
name = "figure(4).axes[0].lines[0]._linestyle"
fun2eval = f'globals()["plt"].{name}'
x = eval(fun2eval, namespace2)
print(x)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

x = eval('globals()["plt"].get_fignums()', namespace1)
print(x)
x = eval('globals()["plt"].figure(1)', namespace1)
print(x)
x = eval('globals()["plt"].figure(1).axes[0].lines[0].get_linestyle()', namespace1)
print(x)
x = eval('globals()["plt"].figure(1).axes[0].lines[0]._linestyle', namespace1)
print(x)
#x = eval('globals()["plt"].figure(2).axes[0].lines[0].get_linestyle()', namespace)
#print(x)
mpatch.undo()
plt.show()

"""
#figure(1).axes(1).line(1).linestyle
x = eval('globals()["plt"].gca().get_lines()[-1].get_linestyle()', namespace)
print(x)

x = eval('globals()["plt"].gca().get_lines()[0].get_linestyle()', namespace)
print(x)

x = eval('globals()["plt"].gca().lines[0]._linestyle', namespace)
print(x)
"""


#print(globals())

#print(namespace)
#dict = {}
#axes:plt.Axes = plt.gca()
#if (len(axes.get_lines()) < 1):
#    return dict
#print(axes.get_lines()[-1].get_linestyle())
#print(axes.get_lines()[-1].get_color())
#print(axes.get_lines()[0].get_color())
#dict["linestyle"] = axes.get_lines()[-1].get_linestyle()

def bar():
    return 33
foo = {
    'bar': bar
}
x = eval('bar()', globals(), foo)
print(x)
