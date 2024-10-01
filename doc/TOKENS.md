# TOKENS
- to specify meta information, meta tokens can be set in the masterfile **_master.py**
- to specify test information, test tokens can be set in the masterfile **_master.py**
- a valid master file contains at least one test (e.g. VARIABLETEST)
- a valid test contains at least one TESTVAR
- see catester/model/model.py for default values:
[default values](../catester/model/model.py#L64)
- see also: [TOKENS-META.md](TOKENS-META.md)
- see also: [TOKENS-TEST.md](TOKENS-TEST.md)

## searching in vscode for #$tokenname
to find examples using certain tokens, use the search in vscode, e.g. search for:
- #$META studentTemplates
- #$META additionalFiles
- #$TESTSUITE
- #$VARIABLETEST
- #$TESTVAR
- #$PROPERTY successDependency
- #$PROPERTY qualification
- #$PROPERTY setUpCode
- ...

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
`#$[tokenname] [property] [value]`

[valid tokennames](../catester/converter/settings.py#L4)
- META
- TESTSUITE
- PROPERTY
- VARIABLETEST
- GRAPHICSTEST
- EXISTANCETEST
- LINTINGTEST
- STRUCTURALTEST
- ERRORTEST
- HELPTEST
- WARNINGTEST
- STDOUTTEST
- TESTVAR

## tokenname: META
[valid properties](../catester/converter/settings.py#L42)
- version
- kind
- type
- title
- description
- authors
- maintainers
- links
- supportingMaterial
- language
- keywords
- license
- testDependencies
- studentSubmissionFiles
- additionalFiles
- testFiles
- studentTemplates
- executionBackendSlug
```python
#$META title "Title of the problemset"
```

## tokenname: TESTSUITE
[valid properties](../catester/converter/settings.py#L64)
- type
- name
- description
- version
```python
#$TESTSUITE name "Title of the testsuite"
```

## tokenname: TESTVAR
when specifying a test variable, only the field [value] is needed, i.e. the name of the variable
```python
#$TESTVAR var1
#$TESTVAR __doc__
#$TESTVAR some_other_variable
```

## specifying tests (i.e. testcollection)
when specifying a testcollection, only the field [value] is needed, which is the name of the test

following testcollections can be set:
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
#$TESTVAR var1

#$GRAPHICSTEST "graphics-test-1"
#$TESTVAR figure(1).axes[0].lines[0]._linestyle
```

## tokenname: PROPERTY
- properties can be set at different "levels"
  - testsuite-level, i.e. before any testcollection is specified
  - testcollection-level, i.e. after a testcollection is specified and before a variable is specified
  - variable-level, i.e. after a variable is specified

[default properties](../catester/model/model.py#L83)

all properties:
- can be used at all levels:
  - failureMessage
  - successMessage
  - qualification
  - relativeTolerance
  - absoluteTolerance
  - allowedOccuranceRange
  - occuranceType
  - typeCheck
  - shapeCheck
  - verbosity
- not used at variable-level:
  - storeGraphicsArtifacts
  - competency
  - timeout
- variable-level only:
  - name, (just used via "#$TESTVAR ...")
  - value
  - evalString
  - pattern
  - countRequirement
- testcollection-level only:
  - name, (just used via e.g. "#$VARIABLETEST ...")
  - type, (just used via e.g. "#$VARIABLETEST ...")
  - description
  - successDependency
  - setUpCodeDependency
  - entryPoint
  - inputAnswers
  - setUpCode
  - tearDownCode
  - id
  - file
  - moduleBlacklist
- [valid properties (testsuite-level)](../catester/converter/settings.py#L84)
- [valid properties (testcollection-level)](../catester/converter/settings.py#L100)
- [valid properties (variable-level)](../catester/converter/settings.py#L91)
```python
#$PROPERTY qualification verifyEqual
#$PROPERTY absoluteTolerance 0
#$PROPERTY relativeTolerance 1.0E-06
```

## inherited PROPERTIES
properties are inherited from "testsuite-level" to "testcollection-level" to "variable-level", see here [where properties are inherited](../catester/tests/conftest.py#L123)

inherited properties:
- testsuite => testcollection => variable-level
  - qualification
  - relativeTolerance
  - absoluteTolerance
  - allowedOccuranceRange
  - occuranceType
  - typeCheck
  - shapeCheck
  - verbosity
- testsuite => testcollection
  - storeGraphicsArtifacts
  - competency
  - timeout

e.g.
```python
"""
the following property will be inherited down to testcollections and testvars,
if not specified (different) later for a testcollection or testvar
"""
#$PROPERTY absoluteTolerance 0.01

#$VARIABLETEST test-1
#$TESTVAR var1
#$TESTVAR var2
#$PROPERTY absoluteTolerance 0.0001
#$TESTVAR var3

#$VARIABLETEST test-2
#$PROPERTY absoluteTolerance 0
#$TESTVAR var1
#$PROPERTY absoluteTolerance 1.0E-06
#$TESTVAR var2
#$TESTVAR var3

"""
with following outcome:
test-1, var1: absoluteTolerance 0.01
test-1, var2: absoluteTolerance 0.0001
test-1, var3: absoluteTolerance 0.01

test-2, var1: absoluteTolerance 1.0E-06
test-2, var2: absoluteTolerance 0
test-2, var3: absoluteTolerance 0
"""
```

## PROPERTY entryPoint
if the masterfile is named e.g. **ex1_master.py**, then the entryPoint will be set to **ex1.py**
if not specified different in the masterfile.

```python
#$META additionalFiles some-other-file.py

#$VARIABLETEST test-some-other-files-variables
#$PROPERTY entryPoint some-other-file.py
#$TESTVAR variable_which_should_be_tested
```

## special cases for testcollections:
EXISTANCETEST, LINTINGTEST, STRUCTURALTEST:
- "#$PROPERTY file [some-filename].py" must be set

EXISTANCETEST, LINTINGTEST:
- #$TESTVAR is needed, but does not point to any "variable", can be any string

```python
#$EXISTANCETEST existance
#$PROPERTY file "file1.py"
#$TESTVAR -

#$LINTINGTEST linting
#$PROPERTY file "file2.py"
#$TESTVAR -
#$PROPERTY pattern W,E2,E3

#$STRUCTURALTEST structural
#$PROPERTY file some-other-file.py
#$TESTVAR some_variable_or_expression_or_string_to_search_for
#$PROPERTY allowedOccuranceRange [1,1]
#$TESTVAR import
#$PROPERTY allowedOccuranceRange [0,1]
#$TESTVAR None
#$PROPERTY allowedOccuranceRange [0,0]
#$TESTVAR "hello world"
#$PROPERTY allowedOccuranceRange [1,1]
```

## incorrect usage
the converter will give hints at several incorrect usages, e.g.:
- misspelled tokennames
- unknown property for a given tokenname 
- no testcollection specified
- testcollection without testvar
- #$PROPERTY at wrong place
- etc...
