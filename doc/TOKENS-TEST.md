# TOKENS-TEST
- various basic examples of how to implement tokens can be found here
- these examples also exist in the repo [catester-examples/tokens-test](../../catester-examples/tokens-test)
- for these examples the master-file is always named **ex_master.py**
- default values are found here: [catester/model/model.py](../catester/model/model.py#L83)

## Variable Tests
- a variable test checks if a variable is correct
- by default, it performs a type check
- by default, it performs a shape check
- type check => shape check => value check
- for numerical types it uses absolute and relative tolerances

### Variable Test 1 (reference solution)
- [catester-examples/tokens-test/variable-1/ex_master.py](../../catester-examples/tokens-test/variable-1/ex_master.py)
- this test uses the reference solution
```python
var1 = 123.456
#$VARIABLETEST variable-1
#$TESTVAR var1
```

### Variable Test 2 (value)
- [catester-examples/tokens-test/variable-2/ex_master.py](../../catester-examples/tokens-test/variable-2/ex_master.py)
- this test does not use the reference solution
- it performs the check against the value provided via PROPERTY value
```python
var1 = 123
#$VARIABLETEST variable-2
#$TESTVAR var1
#$PROPERTY value 123
```

### Variable Test 3 (evalString)
- [catester-examples/tokens-test/variable-3/ex_master.py](../../catester-examples/tokens-test/variable-3/ex_master.py)
- this test does not use the reference solution
- it performs the check against the value evaluated via PROPERTY evalString
```python
var1 = 123
#$VARIABLETEST variable-3
#$TESTVAR var1
#$PROPERTY evalString "120 + 3"
```

### Variable Test 4 (typeCheck)
- [catester-examples/tokens-test/variable-4/ex_master.py](../../catester-examples/tokens-test/variable-4/ex_master.py)
- this test does not use the reference solution
- it performs the check against the value provided via PROPERTY value
- typeCheck is set to false (same as "0", or "False")
- here, the second test will fail, because typeCheck is true (default)
```python
var1 = 1.0
#$VARIABLETEST variable-4
#$TESTVAR var1
#$PROPERTY value 1
#$PROPERTY typeCheck false

#$TESTVAR var1
#$PROPERTY value 1
```

### Variable Test 5 (shapeCheck)
- [catester-examples/tokens-test/variable-5/ex_master.py](../../catester-examples/tokens-test/variable-5/ex_master.py)
- this test does not use the reference solution
- it performs the check against the value provided via PROPERTY value
- shapeCheck is set to false (same as "0", or "False")
- shapeCheck only works for supported types
- shapeCheck is not performed with these types: (int,float,complex,bool,NoneType)
- without shapeCheck is useful, for having the wrong value in the test-summary
- with shapeCheck is useful, for not performing the value check for huge string/array values
- here, the second test will not perform the value check, it failed already the shape check
- here, both tests will fail
```python
var1 = "abcde"
#$VARIABLETEST variable-5
#$TESTVAR var1
#$PROPERTY value "abcdef"
#$PROPERTY shapeCheck false

#$TESTVAR var1
#$PROPERTY value "abcdef"
```

### Variable Test 6 (relativeTolerance, absoluteTolerance)
- [catester-examples/tokens-test/variable-6/ex_master.py](../../catester-examples/tokens-test/variable-6/ex_master.py)
- default values are:
    - relativeTolerance: 1.0e-12
    - absoluteTolerance: 0.0001
- see also [pytest approx](https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest-approx) on how pytest handles absolute and relative tolerances
- a test is passed if either tolerance is met
- here, tests 1 and 2 will pass, test 3 fill fail beacause both tolerances are not met
```python
var1 = 1 + 1e-13
#$VARIABLETEST variable-6
#$TESTVAR var1
#$PROPERTY relativeTolerance 1e-99
#$PROPERTY value 1.0

#$TESTVAR var1
#$PROPERTY absoluteTolerance 0
#$PROPERTY value 1.0

#$TESTVAR var1
#$PROPERTY relativeTolerance 1e-14
#$PROPERTY absoluteTolerance 0
#$PROPERTY value 1.0
```

### Variable Test 7 (\_\_doc\_\_)
- [catester-examples/tokens-test/variable-7/ex_master.py](../../catester-examples/tokens-test/variable-7/ex_master.py)
- this test checks the doc-string from a python file against a given pattern
```python
"""this is the doc-string, which gets stored into __doc__"""
#$VARIABLETEST variable-7
#$TESTVAR __doc__
#$PROPERTY qualification startsWith
#$PROPERTY pattern "this is the"
```

### String Test 1 (matches, contains, startsWith, endsWith, count, regexp)
- [catester-examples/tokens-test/string-1/ex_master.py](../../catester-examples/tokens-test/string-1/ex_master.py)
- for string comparisons PROPERTY "pattern" is mandatory
- PROPERTY "qualification" must be set to:
    - matches
    - contains
    - startsWith
    - endsWith
    - count
    - regexp
- if qualification = count, then PROPERTY "countRequirement" is also needed
- nice regex reference, see here: [regexr.com](https://regexr.com/)
- these tests does not use the reference solution, is checks the variable against the specified pattern
```python
var1 = "_abcdefgh_"
#$VARIABLETEST string-1
#$TESTVAR var1
#$PROPERTY qualification matches
#$PROPERTY pattern "_abcdefgh_"

#$TESTVAR var1
#$PROPERTY qualification contains
#$PROPERTY pattern "cde"

#$TESTVAR var1
#$PROPERTY qualification startsWith
#$PROPERTY pattern "_a"

#$TESTVAR var1
#$PROPERTY qualification endsWith
#$PROPERTY pattern "gh_"

#$TESTVAR var1
#$PROPERTY qualification count
#$PROPERTY countRequirement 2
#$PROPERTY pattern "_"

#$TESTVAR var1
#$PROPERTY qualification regexp
#$PROPERTY pattern "^_[a-h]+_$"

#$TESTVAR var1
#$PROPERTY qualification regexp
#$PROPERTY pattern "^\\w+$"
```

### Testcollection Test 1 (timeout)
- [catester-examples/tokens-test/testcollection-1/ex_master.py](../../catester-examples/tokens-test/testcollection-1/ex_master.py)
- the first test passes
- the second test fails, because of timeout
```python
import time
time.sleep(0.25)
var1 = 1
#$VARIABLETEST timeout-pass
#$PROPERTY timeout 0.5
#$TESTVAR var1

#$VARIABLETEST timeout-fail
#$PROPERTY timeout 0.1
#$TESTVAR var1
```

### Testcollection Test 2 (successDependency)
- [catester-examples/tokens-test/testcollection-1/ex_master.py](../../catester-examples/tokens-test/testcollection-1/ex_master.py)
- successDependency can be a string or integer, or a list of strings/integers
- if a testcollection has the PROPERTY id (a string), then this id can be used as the successDependency
- if successDependency is an integer, then it means the 1-based index of testcollections (e.g. 1 = the first testcollection, and so on...)
- test-1 passes
- test-2 fails
- test-3 passes
- test-4 passes, successDependency met
- test-5 skips, successDependency not met
- test-6 passes, all successDependencies met
- test-7 skips, one of the successDependencies not met
- test-8 passes, successDependency (1) met
- test-9 skips, successDependency (2) not met
```python
var1 = 1
var2 = 2
var3 = 3
#$VARIABLETEST test-1
#$PROPERTY id test1
#$TESTVAR var1
#$PROPERTY value 1

#$VARIABLETEST test-2
#$PROPERTY id test2
#$TESTVAR var2
#$PROPERTY value 99

#$VARIABLETEST test-3
#$PROPERTY id test3
#$TESTVAR var3
#$PROPERTY value 3

#$VARIABLETEST test-4
#$PROPERTY successDependency "test1"
#$TESTVAR var1
#$PROPERTY value 1

#$VARIABLETEST test-5
#$PROPERTY successDependency "test2"
#$TESTVAR var1
#$PROPERTY value 1

#$VARIABLETEST test-6
#$PROPERTY successDependency ["test1", "test2"]
#$TESTVAR var1
#$PROPERTY value 1

#$VARIABLETEST test-7
#$PROPERTY successDependency ["test1", "test3"]
#$TESTVAR var1
#$PROPERTY value 1

#$VARIABLETEST test-8
#$PROPERTY successDependency 1
#$TESTVAR var1
#$PROPERTY value 1

#$VARIABLETEST test-9
#$PROPERTY successDependency 2
#$TESTVAR var1
#$PROPERTY value 1
```

### Testcollection Test 3 (entryPoint)
- [catester-examples/tokens-test/testcollection-3/ex_master.py](../../catester-examples/tokens-test/testcollection-3/ex_master.py)
- the entryPoint defaults to the reference file, here (ex.py)
- test-2 uses the PROPERTY "entryPoint", set to additional-file.py
```python
#$META studentSubmissionFiles additional-file.py

var1 = 1
#$VARIABLETEST test-1
#$TESTVAR var1

#$VARIABLETEST test-2
#$PROPERTY entryPoint additional-file.py
#$TESTVAR var2
```

### Testcollection Test 4 (setUpCode)
- [catester-examples/tokens-test/testcollection-4/ex_master.py](../../catester-examples/tokens-test/testcollection-4/ex_master.py)
- setUpCode can be a string or a list of string which will be executed
- setUpCode is executed after the entryPoint is executed into the namespace
- test-1, test-2 and test-3 are all the same
```python
var1 = 1
#$VARIABLETEST test-1
#$PROPERTY setUpCode "var2 = var1\ndel var1"
#$TESTVAR var1
#$TESTVAR var2

#$VARIABLETEST test-2
#$PROPERTY setUpCode ["var2 = var1", "del var1"]
#$TESTVAR var1
#$TESTVAR var2

#$VARIABLETEST test-3
#$PROPERTY setUpCode "var2 = var1"
#$PROPERTY setUpCode "del var1"
#$TESTVAR var1
#$TESTVAR var2
```

### Testcollection Test 5 (setUpCodeDependency)
- [catester-examples/tokens-test/testcollection-5/ex_master.py](../../catester-examples/tokens-test/testcollection-5/ex_master.py)
- if setUpCodeDependency is set it uses the namespace of the corresponding testcollection as its initial values
- setUpCodeDependency can be a string or integer
- if a testcollection has the PROPERTY id (a string), then this id can be used as the setUpCodeDependency
- if setUpCodeDependency is an integer, then it means the 1-based index of testcollections (e.g. 1 = the first testcollection, and so on...)
- test-1 passes, because var1 is defined in additional-file.py
- test-2 passes, because it uses the namespace of test-1 (as initial)
- test-3 passes, because it uses the namespace of test-2 (as initial)
- test-4 fails, because var1 is not found
```python
#$META studentSubmissionFiles additional-file.py

#$VARIABLETEST test-1
#$PROPERTY id "test1"
#$PROPERTY entryPoint additional-file.py
#$TESTVAR var1

#$VARIABLETEST test-2
#$PROPERTY setUpCodeDependency "test1"
#$TESTVAR var1

#$VARIABLETEST test-3
#$PROPERTY setUpCodeDependency 2
#$TESTVAR var1

#$VARIABLETEST test-4
#$TESTVAR var1
```

### Testcollection Test 6 (inputAnswers)
- [catester-examples/tokens-test/testcollection-6/ex_master.py](../../catester-examples/tokens-test/testcollection-6/ex_master.py)
- the PROPERTY "inputAnswers" is MANDATORY, if there is an input prompt in the code
- inputAnswers is either a string or a list of strings
- the count of inputAnswers MUST match the count of input-prompts
- here, two answers are needed (for each test)
- test-2 uses a mixture of inputAnswers and STDOUTTEST
```python
var1 = input("Please input a number from 1 to 100: ")
var2 = input("Please input a number from 1 to 100: ")
var3 = int(var1) + int(var2)
print(f"the sum of {var1} and {var2} is {var3}")

#$VARIABLETEST test-1
#$PROPERTY inputAnswers 7
#$PROPERTY inputAnswers 8
#$TESTVAR var3
#$PROPERTY value 15

#$STDOUTTEST test-2
#$PROPERTY inputAnswers ["1", "2"]
#$TESTVAR -
#$PROPERTY qualification endsWith
#$PROPERTY pattern "the sum of 1 and 2 is 3\n"
```

### Testcollection Test 7 (moduleBlacklist)
- [catester-examples/tokens-test/testcollection-7/ex_master.py](../../catester-examples/tokens-test/testcollection-7/ex_master.py)
- moduleBlacklist is either a string or a list of strings
- currently, moduleBlacklist only works for direct imports
- moduleBlacklist does not work for indirect imports, see test-2
- test-1 fails, because it imports "additional"
- test-2 passes, because additional.py imports "numpy", <span style="background-color: red; color: black">TODO, this test should fail</span>
- test-3 fails, because it imports "additional" and "math"
```python
#$META studentSubmissionFiles ./additional.py

from additional import get_pi_from_numpy
import math

var1 = get_pi_from_numpy()
var2 = var1 * math.pi

#$VARIABLETEST variables test-1
#$PROPERTY moduleBlacklist ["additional"]
#$TESTVAR var2

#$VARIABLETEST variables test-2
#$PROPERTY moduleBlacklist ["numpy"]
#$TESTVAR var2

#$VARIABLETEST variables test-3
#$PROPERTY moduleBlacklist ["additional", "numpy", "math"]
#$TESTVAR var2
```

## Existance Tests
- an existance test checks if a file or folder exists
- the token TESTVAR is needed, but does not point to any "variable", can be any string

### Existance Test 1
- [catester-examples/tokens-test/existance-1/ex_master.py](../../catester-examples/tokens-test/existance-1/ex_master.py)
```python
#$EXISTANCETEST existance-1
#$PROPERTY file ex.py
#$TESTVAR -
```

### Existance Test 2 (file)
- [catester-examples/tokens-test/existance-2/ex_master.py](../../catester-examples/tokens-test/existance-2/ex_master.py)
- this test checks for existance of an additional file
```python
#$META additionalFiles additional-file.py

#$EXISTANCETEST existance-2
#$PROPERTY file additonal-file.py
#$TESTVAR -
```

### Existance Test 3 (folder)
- [catester-examples/tokens-test/existance-3/ex_master.py](../../catester-examples/tokens-test/existance-3/ex_master.py)
- this test checks for existance of an additional folder
```python
#$META additionalFiles ./additional-folder

#$EXISTANCETEST existance-3
#$PROPERTY file additonal-folder
#$TESTVAR -
```

### Stdout Test 1
- [catester-examples/tokens-test/stdout-1/ex_master.py](../../catester-examples/tokens-test/stdout-1/ex_master.py)
- the token TESTVAR is needed, but does not point to any "variable", can be any string
- test-1 compares against the reference solution
- test-2 and test-3 compare against a given pattern
- test-3 obviously fails
```python
print("abc")
#$STDOUTTEST test-1
#$TESTVAR -

#$STDOUTTEST test-2
#$TESTVAR -
#$PROPERTY qualification startsWith
#$PROPERTY pattern "ab"

#$STDOUTTEST test-3
#$TESTVAR -
#$PROPERTY qualification matches
#$PROPERTY pattern "abcde"
```

### Graphics Test 1
- [catester-examples/tokens-test/graphics-1/ex_master.py](../../catester-examples/tokens-test/graphics-1/ex_master.py)
- basic graphics test
```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 20, 1000)
y = np.sin(x)
plt.plot(x, y, "-b", label="sine")
plt.show()

#$GRAPHICSTEST graphics-1
#$TESTVAR figure(1).axes[0].lines[0].get_linestyle()
```

### Graphics Test 2 (storeGraphicsArtifacts)
- [catester-examples/tokens-test/graphics-2/ex_master.py](../../catester-examples/tokens-test/graphics-2/ex_master.py)
- basic graphics test
- storeGraphicsArtifacts defaults to False
- here, storeGraphicsArtifacts is set to True, graphics get stored into "artifacts"-directory, see testrunner-directory
```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 20, 1000)
y = np.sin(x)
plt.plot(x, y, "-b", label="sine")
plt.show()

#$GRAPHICSTEST graphics-1
#$TESTVAR figure(1).axes[0].lines[0].get_linestyle()
```

### Structural Test 1
- [catester-examples/tokens-test/structural-1/ex_master.py](../../catester-examples/tokens-test/structural-1/ex_master.py)
- STRUCTURALTEST uses the [tokenizer](https://github.com/python/cpython/blob/3.12/Lib/token.py) from python
- occuranceType defaults to "NAME"
- occuranceType "STRING" is supported as well
- allowedOccuranceRange defaults to [0, 0], (i.e. [min, max]-required)
```python
import numpy
var1 = numpy.pi
var2 = "None"
var3 = None
var4 = None
var5 = "def"
def add(a, b):
    return a + b
#$STRUCTURALTEST structural-1
#$PROPERTY file "ex.py"
#$TESTVAR import
#$PROPERTY allowedOccuranceRange [1, 1]
#$TESTVAR def
#$PROPERTY allowedOccuranceRange [0, 2]
#$TESTVAR None
#$PROPERTY allowedOccuranceRange [2, 2]
#$TESTVAR "None"
#$PROPERTY occuranceType STRING
#$PROPERTY allowedOccuranceRange [1, 1]
#$TESTVAR numpy
#$PROPERTY allowedOccuranceRange [2, 2]
#$TESTVAR scipy
#$PROPERTY allowedOccuranceRange [0, 0]
```

### Linting Test 1
- [catester-examples/tokens-test/linting-1/ex_master.py](../../catester-examples/tokens-test/linting-1/ex_master.py)
- flake8 is used as linter: [see here](https://flake8.pycqa.org/)
- ignore-flag: https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-ignore
- for the LINTINGTEST, the property "pattern" is used as the ignore-flag for the linter
- pattern is a comma-separated list of error-codes which should be ignored
- flake8 error codes: https://flake8.pycqa.org/en/latest/user/error-codes.html
- pycodestyle error codes: https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes
- here, a folder userSolution1 exists under localTests, containing some linting-errors, check the testrunner/output...
- test-1 ignores every error-code starting with "E2" (i.e. whitespace - errors)
- test-1 ignores every error-code starting with "E3" (i.e. blank line - errors)
- test-1 ignores every error-code starting with "W" (i.e. warnings)
- test-2 reports everything
```python
var1 = 1
#$LINTINGTEST test-1
#$PROPERTY file "ex.py"
#$TESTVAR -
#$PROPERTY pattern W,E2,E3

#$LINTINGTEST test-2
#$PROPERTY file "ex.py"
#$TESTVAR -
```

### TestDependency Test 1
- [catester-examples/tokens-test/testDependency1/ex_master.py](../../catester-examples/tokens-test/testDependency1/ex_master.py)
- here, the function "add" is defined
```python
def add(a, b):
    return a + b
x = add(1, 2)
#$VARIABLETEST test-1
#$TESTVAR x
```

### TestDependency Test 2 (META testDependencies)
- [catester-examples/tokens-test/testDependency2/ex_master.py](../../catester-examples/tokens-test/testDependency2/ex_master.py)
- here, the function "add" is imported
- the specified testDependencies get copied to the respective directories in testrunner
```python
#$META testDependencies ../testDependency1/ex.py
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from testDependency1.ex import add
x = add(1, 2)
#$VARIABLETEST test-unit2
#$TESTVAR x
```
