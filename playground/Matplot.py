import matplotlib.pyplot as plt

def add(a, b):
  return a + b

# First plot with a solid line
plt.figure()  # Create the first figure
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], linestyle='-', label='Solid Line')  # Plot with solid line style (abbreviated as '-')
plt.legend()  # Show legend for the first figure
fig1 = plt.gcf()  # Get reference to the first figure

# Second plot with a dashed line
plt.figure()  # Create the second figure
plt.plot([1, 2, 3, 4], [1, 3, 6, 10], linestyle='--', label='Dashed Line')  # Plot with dashed line style (abbreviated as '--')
plt.legend()  # Show legend for the second figure
fig2 = plt.gcf()  # Get reference to the second figure

# Show the plots
#plt.show()

# Now 'fig1' and 'fig2' hold references to their respective figures
# Each plot has its own line style defined using abbreviated aliases