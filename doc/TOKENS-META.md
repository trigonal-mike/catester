# TOKENS-META
several examples using META-tokens can be found here:

## Basic Settings
```python
#$META version 1.3.4.5
#$META kind assignment
#$META type standard
#$META type extra
#$META type mandatory
#$META title "Title of the problemset"
#$META description Description of the problemset
#$META language de
#$META license MIT
```

## Author, Maintainer
```python
#$META authors {"name":"Author #1", "email":"email@tugraz.at", "affiliation":"TU Graz"}
#$META maintainers {"name":"Maintainer #1", "email":"email@tugraz.at", "affiliation":"TU Graz"}
#$META maintainers {"name":"Maintainer #2", "email":"email@tugraz.at", "affiliation":"TU Graz"}
```

## Links, Supporting Material
```python
#$META links {"description":"Description of Link-1", "url":"https://www.python.org/"}
#$META links {"description":"Description of Link-2", "url":"https://www.python.org/"}
#$META links {"description":"Description of Link-3", "url":"https://www.python.org/"}
#$META supportingMaterial {"description":"Description", "url":"supporturl"}
#$META supportingMaterial {"description":"Description", "url":"supporturl"}
```

## Keywords
```python
#$META keywords ["one keyword", "another keyword"]
#$META keywords "intermediate"
#$META keywords "testing"
```

## Test Dependencies
```python
#$META testDependencies ../04_quadgl/quadgl.py
#$META testDependencies ../Unit01/unit1.py
```

## Files, Folders
```python
#$META studentSubmissionFiles ./add1.py:add2.py
#$META studentSubmissionFiles add3.py
#$META additionalFiles ./data-dir1
#$META additionalFiles ./data-dir2/only-this.dat
#$META testFiles ./test
#$META studentTemplates ./templates
#$META studentTemplates ./studentTemplates/file1.py
#$META studentTemplates ./studentTemplates/file2.py
#$META studentTemplates studentTemplates/file1.py
```
