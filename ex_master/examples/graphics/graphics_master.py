import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 20, 1000)
y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, "-b", label="sine")
plt.plot(x, y2, "-r", label="cosine")
plt.legend(loc="upper left")
#plt.legend(loc="best")
#plt.legend(loc="center")
plt.xlabel('xx', {"fontsize": 14})
plt.ylabel('yy', {"fontsize": 14})
plt.ylim(-1.5, 2.0)
plt.show()

#$GRAPHICSTEST graphics-test
#$PROPERTY entryPoint "graphics.py"
#$TESTVAR figure(1).axes[0].lines[0]._linestyle
#$TESTVAR figure(1).axes[0].lines[0].get_linestyle()
#$TESTVAR figure(1).axes[0].get_xlabel()
#$PROPERTY qualification startsWith
#$PROPERTY pattern "x"
#$TESTVAR figure(1).axes[0].get_ylabel()
#$PROPERTY value "yy"

#$STRUCTURALTEST structural-test
#$PROPERTY file "graphics.py"
#$TESTVAR "upper left"
#$PROPERTY allowedOccuranceRange [1,1]
#$PROPERTY occuranceType STRING
#$TESTVAR legend
#$PROPERTY allowedOccuranceRange [1,1]
#$TESTVAR (
#$PROPERTY occuranceType OP
#$PROPERTY allowedOccuranceRange [10,10]
