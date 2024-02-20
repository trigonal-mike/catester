#$VARIABLETEST test1
#$TESTVAR x
#$PROPERTY value 2
#$TESTVAR y

#$VARIABLETEST test2
#$PROPERTY successDependency 1
#$TESTVAR h

import numpy as np
h=np.array([[[1,2,3],[3,4,5]],[[5,6,7],[7,8,9]],[[9,10,11],[12,13,14]]])
x=1
y=1

#$META additionalFiles ./add
#$META studentTemplates ./templates
