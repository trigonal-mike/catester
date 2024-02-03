#$TESTSUITE type: Pythgfghon  
#$TESTSUITE name: xxxxxxx
#$TESTSUITE name: Python Test suite
#$TESTSUITE description: Checks variables
#$TESTSUITE version: "1.0"
#$PROPERTY qualification: contains
#$PROPERTY successMessage: Tests succeeded
#$PROPERTY storeGraphicsArtifacts: true

var1 = 1.0
var2 = [1, 2]
var3 = "[1, 2]"
#$VARIABLE var1
#$TEST successMessage: "Test succeeded"
#$TEST failureMessage: "Test failed"
#$SUBTEST value: df
#$VARIABLE var2
#$SUBTEST failureMessage: "Test failed"
#$VARIABLE var3
#$SUBTEST successMessage: "Test succeeded"
#$SUBTEST countRequirement: "123"
#$TEST qualification: verifyEqual
#$TEST name: ccccccc

#$GRAPHICS figure(1).axes[0].lines[0].get_linestyle()
#$GRAPHICS figure(1).axes[0].get_xlabel()