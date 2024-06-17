import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Unit01.unit1 import add

x = add(1, 2)

#$VARIABLETEST test-unit2
#$TESTVAR x
#$PROPERTY typeCheck 0
#$PROPERTY shapeCheck 0

##$META testDependencies ../Unit01
#$META testDependencies ../Unit01/unit1.py
