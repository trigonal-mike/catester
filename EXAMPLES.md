# examples
Masterfile-Examples for Python Testing Converter

A Masterfile is a file named "*_master.py", e.g.: "example_master.py"

## META-TOKENS
#### Basic Settings
```python
#$META version 1.3.4.5
#$META type ProblemSet
#$META title "Title of the problemset"
#$META description Description of the problemset
#$META language de
#$META license MIT
```
#### Author, Maintainer
```python
#$META authors {"name":"Author #1", "email":"email@tugraz.at", "affiliation":"TU Graz"}
#$META maintainers {"name":"Maintainer #1", "email":"email@tugraz.at", "affiliation":"TU Graz"}
#$META maintainers {"name":"Maintainer #2", "email":"email@tugraz.at", "affiliation":"TU Graz"}
```
#### Links, Supporting Material
```python
#$META links {"description":"Description of Link-1", "url":"https://www.python.org/"}
#$META links {"description":"Description of Link-2", "url":"https://www.python.org/"}
#$META links {"description":"Description of Link-3", "url":"https://www.python.org/"}
#$META supportingMaterial {"description":"Description", "url":"supporturl"}
#$META supportingMaterial {"description":"Description", "url":"supporturl"}
```
#### Keywords
```python
#$META keywords ["one keyword", "another keyword"]
#$META keywords "intermediate"
#$META keywords "testing"
```
#### Files, Folders
```python
#$META studentSubmissionFiles ./add1.py:add2.py
#$META studentSubmissionFiles add3.py
#$META additionalFiles ./data-dir1
#$META additionalFiles ./data-dir2/only-this.dat
#$META testFiles ./test
#$META studentTemplates ./templates
```
