from matplotlib.container import ErrorbarContainer
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
x = np.arange(10)
y = 2.5 * np.sin(x / 20 * np.pi)
yerr = np.linspace(0.05, 0.2, 10)

plt.errorbar(x, y + 3, yerr=yerr, label='both limits (default)', fmt="-.", capsize=25, elinewidth=7)
plt.errorbar(x, y + 2, yerr=yerr, uplims=True, label='uplims=True')
plt.errorbar(x, y + 1, yerr=yerr, uplims=True, lolims=True, label='uplims=True, lolims=True')
upperlimits = [True, False] * 5
lowerlimits = [False, True] * 5
plt.errorbar(x, y, yerr=yerr, uplims=upperlimits, lolims=lowerlimits, label='subsets of uplims and lolims')
plt.legend(loc='lower right')
#plt.show()

figure = plt.figure(1)
con = figure.axes[0].containers
print(con)
errb:ErrorbarContainer = con[0]
(data_line, caplines, barlinecols) = errb

print(caplines)

x=errb.lines
print(x)
x=errb.lines[0].get_children()
print(x)
x=errb.lines[2][0].get_linewidth()[0]
print(x)
x=errb.lines[0].get_linestyle()
print(x)
x=errb.get_label()
print(x)
x=errb.lines[0].get_label()
print(x)
# [<BarContainer object of 3 artists>]
