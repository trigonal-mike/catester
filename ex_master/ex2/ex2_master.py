#$TESTSUITE type: Pythgfghoffff
#$TESTSUITE name: xxxxxxx
#$TESTSUITE name: Python Test suite
#$TESTSUITE description: Checks variables
#$TESTSUITE version: "1.0"
#$PROPERTY qualification : verifyEqual
#$PROPERTY successMessage: Tests succeeded
#$PROPERTY storeGraphicsArtifacts: true
#$PROPERTY absoluteTolerance: 1.0

import time

var1 = 1.0
var2 = [1, 2]
var3 = "[1, 2]"
time.sleep(0.1)


#$VARIABLETEST xxxx
#$TESTVAR var1
#$TEST successMessage: "Test succeeded"
#$TEST failureMessage: "Test failed"
#$SUBTEST value: 2.1
#$TEST timeout: .9
#$TEST absoluteTolerance: 11.0
#$SUBTEST absoluteTolerance: 10.9
#$TESTVAR var2
#$SUBTEST failureMessage: "Test failed"
#$TESTVAR var3
#$SUBTEST successMessage: "Test succeeded"
#$SUBTEST countRequirement: "123"
#$TEST qualification: verifyEqual 
##$TEST nagme: ccccccc

#$GRAPHICSTEST y yy  y
#$TESTVAR figure(1).axes[0].lines[0].get_linestyle()
#$TESTVAR figure(1).axes[0].get_xlabel()
#$TEST entryPoint: xxx.py

##$PROPERTY absoluteTolerjance: 1111.0

#$VARIABLETEST xxxxdh
#gsTESTVAR[d]= var1
x = 1
y = 1
#$TESTVAR x
#$SUBTEST value: 1
#$VARIABLETEST xxhxx
#$TESTVAR y
#$SUBTEST value: 1
