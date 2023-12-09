from matplotlib import pyplot as plt
import numpy as np

data = np.loadtxt('data.dat', dtype=np.float64, comments='%')

U = data[:, 0]
I = data[:, 1] * 1000

#matplot-figure:
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y, linestyle='--')
plt.text(5, 0, 'Sample Text', fontsize=12, color='red')
plt.show()

