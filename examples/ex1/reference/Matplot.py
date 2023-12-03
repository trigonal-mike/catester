from matplotlib import pyplot as plt
import numpy as np

#matplot-figure:
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y, linestyle='--')  # Set line style
plt.text(5, 0, 'Sample Text', fontsize=12, color='red')  # Add sample text
plt.show()

