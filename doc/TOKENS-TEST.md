# TOKENS-TEST
- to specify test information, test tokens can be set in the masterfile **[some-name]_master.py**

- a valid master file contains at least one test!

- see catester/model/model.py for default values:
[default values](../catester/model/model.py#64)

test.yaml (defaults)
```yaml
type: python
name: Python Test Suite
description: Checks subtests and graphics
version: '1.0'
properties:
  failureMessage: Some or all tests failed
  successMessage: Congratulations! All tests passed
  qualification: verifyEqual
  relativeTolerance: 1.0e-12
  absoluteTolerance: 0.0001
  allowedOccuranceRange:
  - 0
  - 0
  occuranceType: NAME
  typeCheck: true
  shapeCheck: true
  timeout: 180.0
```

several examples are listed here

and can also be found in the repository "catester-examples" and "assignments"

## Variable Test (reference - solution)
```python
var1 = 123.456
#$VARIABLETEST simple-test
#$TESTVAR var1
```

## Variable Test (value)
```python
var1 = 123
#$VARIABLETEST simple-test
#$TESTVAR var1
#$PROPERTY value 123
```

## Variable Test (evalString)
```python
var1 = 123
#$VARIABLETEST simple-test
#$TESTVAR var1
#$PROPERTY evalString "120 + 3"
```





wenn input imfile => inputAnswers erforderlich!!!


