from matplotlib import pyplot as plt
import numpy as np

var1 = 0.2 + 0.1
var2 = "1"
var3 = True
var4 = [1, 2]
var5 = [1, 2]

x = np.linspace(0, 10, 100)
y = np.sin(x) + 0.0001
plt.plot(x, y, linestyle='--')  # Set line style
plt.text(5, 0, 'Sample Text', fontsize=12, color='red')  # Add sample text
plt.show()
