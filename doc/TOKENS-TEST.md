# EXAMPLES-TEST
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
- here the second test will fail, because typeCheck is true (default)
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
- here the second test will not perform the value check, it failed already the shape check
- here both tests will fail
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





wenn input imfile => inputAnswers erforderlich!!!


