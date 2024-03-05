#$META description "Erzeugen von Zufallszahlen"
import random
import numpy as np


rand1 = np.random.rand(10)
rand2 = np.random.randn(20)
rand_normal = np.random.randn(20) * 0.2 + 5
# rand_normal = np.random.normal(loc=5, scale=0.2, size=20)

i_min = 5
i_max = 15

# Remark: The function np.random.randint creates integer random number
# in the half-open interval [a,b)
randint1 = np.random.randint(i_min, i_max + 1, 30)
randint2 = np.floor(i_min + (i_max - i_min + 1) * np.random.rand(30))

#$VARIABLETEST random
#$PROPERTY id "random"
#$TESTVAR rand1
#$TESTVAR rand2
#$TESTVAR i_min
#$TESTVAR i_max
#$TESTVAR rand_normal
#$TESTVAR randint1
#$TESTVAR randint2
