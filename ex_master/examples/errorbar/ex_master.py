import matplotlib.pyplot as plt
import numpy as np

x = np.arange(10)
y = 2.5 * np.sin(x / 20 * np.pi)
yerr = np.linspace(0.05, 0.2, 10)

plt.errorbar(x, y + 3, yerr=yerr, label='my errorbar', fmt="-.", capsize=25, elinewidth=7)
plt.show()

#$GRAPHICSTEST errorbar-test
#$PROPERTY entryPoint "ex.py"
#$TESTVAR figure(1).axes[0].containers[0].get_label()
#$PROPERTY qualification startsWith
#$PROPERTY pattern "my err"
#$TESTVAR figure(1).axes[0].containers[0].lines[0].get_linestyle()
#$PROPERTY value "-."
#$TESTVAR figure(1).axes[0].containers[0].lines[2][0].get_linewidth()[0]
