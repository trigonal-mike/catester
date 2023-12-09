import matplotlib.pyplot as plt

# First plot with a solid line
plt.figure()  # Create the first figure
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], linestyle=':', label='Solid Line')  # Plot with solid line style (abbreviated as '-')
plt.legend()  # Show legend for the first figure

# Second plot with a dashed line
plt.figure()  # Create the second figure
plt.plot([1, 2, 3, 4], [1, 3, 6, 10], linestyle='-.', label='Dashed Line')  # Plot with dashed line style (abbreviated as '--')
plt.legend()  # Show legend for the second figure

# Get the number of figures created by plt
number_of_figures = plt.gcf().number  # Get the number of the current figure
all_figure_numbers = plt.get_fignums()  # Get a list of all figure numbers

print("Number of figures created by plt:", number_of_figures)
print("All figure numbers:", all_figure_numbers)

# Show the plots
plt.show()

#print(plt.figure(1).axes[0].lines[0].get_linestyle())
#print(plt.figure(2).axes[0].lines[0].get_linestyle())

"""

import matplotlib.pyplot as plt

# Create a figure and a plot
plt.figure(1)
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], linestyle='--')  # Plot with dashed line style

# Get the current axes of figure 1
axes = plt.figure(1).axes[0]  # Assuming there's only one subplot

# Get the lines within the axes
lines = axes.get_lines()

# Get the linestyle of the first line in figure 1
line_style = lines[0].get_linestyle()

print("Line Style in Figure 1:", line_style)  # Print the linestyle of the line in figure 1

# Show the plot
plt.show()
"""
