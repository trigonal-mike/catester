''' Python Skript: "04_plot_docstr"
    Einfaches Plotprogramm
    Name: "xxx" "yyy"
    Datum: "10.03.2024"'''


import numpy as np
import matplotlib.pyplot as plt


pi = np.pi


x = np.linspace(-pi, pi, num=200)

y_1 = x
y_2 = x
y_3 = x


plt.plot(x, y_1, 'r')
plt.plot(x, y_2, '--b')
plt.plot(x, y_3, ':k')


plt.xlim(min(x), max(x))
plt.ylim(min(y_3), max(y_3))

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Test')


plt.show()

#$VARIABLETEST variables docstring
#$TESTVAR __doc__
#$PROPERTY qualification contains
#$PROPERTY pattern Name
