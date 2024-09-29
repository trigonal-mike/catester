# TOKENS
- to specify test information, test tokens can be set in the masterfile **[some-name]_master.py**
- a valid master file contains at least one test (e.g. VARIABLETEST)
- a valid test contains at least one TESTVAR
- see catester/model/model.py for default values:
[default values](../catester/model/model.py#L64)

test.yaml (defaults):
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

## token syntax rules
#$[tokenname] [property] [value]

[valid tokennames](../catester/converter/settings.py#L4)

## tokenname: META
[valid properties](../catester/converter/settings.py#L42)
```python
#$META title "Title of the problemset"
```

## tokenname: TESTSUITE
[valid properties](../catester/converter/settings.py#L64)
```python
#$TESTSUITE name "Title of the testsuite"
```

## tokenname: PROPERTY
- properties are inherited from the parent, if defined there, if not default values are used.
- properties can be set at different "levels"
  - testsuite-level, i.e. before any testcollection is specified
  - testcollection-level, i.e. after a testcollection is specified and before a variable is specified
  - variable-level, i.e. after a variable is specified

[default properties](../catester/model/model.py#L83)

- [valid properties (testsuite-level)](../catester/converter/settings.py#L84)
- [valid properties (testcollection-level)](../catester/converter/settings.py#L100)
- [valid properties (variable-level)](../catester/converter/settings.py#L91)
```python
#$PROPERTY qualification verifyEqual
#$PROPERTY absoluteTolerance 0
#$PROPERTY relativeTolerance 1.0E-06
```

## tokenname: TESTVAR
when specifying a test variable, only the field [value] is needed, i.e. the name of the variable

```python
#$TESTVAR var1
#$TESTVAR __doc__
#$TESTVAR some_other_variable
```

## specifying tests
when specifying a test, only the field [value] is needed, which is the name of the test

following tests can be set:
- VARIABLETEST
- GRAPHICSTEST
- EXISTANCETEST
- LINTINGTEST
- STRUCTURALTEST
- ERRORTEST, not implemented
- HELPTEST, not implemented (use TESTVAR \_\_doc\_\_ instead)
- WARNINGTEST, not implemented
- STDOUTTEST
```python
#$VARIABLETEST variable-test-1
#$GRAPHICSTEST "graphics-test-1"
```
