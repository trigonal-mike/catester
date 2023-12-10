from matplotlib import pyplot as plt
import numpy as np

data = np.loadtxt('data.dat', dtype=np.float64, comments='%')

U = data[:, 0]
I = data[:, 1] * 1000

#matplot-figure:
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.figure()
plt.plot(x, y, linestyle='--')
plt.text(5, 0, 'Sample Text', fontsize=12, color='red')
plt.xlabel('xAy', {"fontsize": 14})
plt.ylabel('y', {"fontsize": 14})
plt.show()

x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.figure()
plt.plot(x, y, linestyle='--')
plt.text(5, 0, 'xxx', fontsize=12, color='red')
plt.xlabel('xAy', {"fontsize": 14})
plt.ylabel('y', {"fontsize": 14})
plt.show()

