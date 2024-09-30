# examples
- examples consist of one or more folders containing master-files,
- only one master-file per folder

## example folder structure
```
└── examples
    ├── ex1
        ├── ex1_master.py
        ├── ex1.py
        ├── meta.yaml
        ├── test.yaml
        ├── localTests
            ├── _reference
                └── ex1.py
            ├── _correctSolution
                └── ex1.py
            ├── _emptySolution
            ├── userSolution1
                └── ex1.py
            └── ...
    ├── ex2
        └── somefilename_master.py
    ├── Week01
        ├── unit1
            └── unit1_master.py
        ├── unit2
            └── unit2_master.py
        └── ...
    └── ...
```

## master-file naming
- a master-file name has to end with **_master.py**, e.g. ex1_master.py
- you have to provide a folder with a containing master file

## associated files/folders
associated files are created following the instructions (pragmas, tokens) set in a **_master.py** file

assume a folder containing **ex1_master.py**

the created files/folders are:
- **meta.yaml** - file containing meta-information for the test system
- **test.yaml** - file containing the actual tests which should be performed
- **ex1.py** - is the created reference solution (i.e. ex1_master.py without double-comments '##' and without tokens '#$TOKENNAME')
- **localTests** - contains directories which are getting tested at a later stage,
directories starting with "_" are automatically created and should not be altered.
- **localTests/_reference** - folder containing the reference solution
- **localTests/_correctSolution** - folder containing the correct solution (i.e. the reference Solution)
- **localTests/_emptySolution** - folder containing the empty solution (i.e. no files)

## providing more solutions
the best way is to copy the whole content of **_correctSolution** directory into a new directory under **localTests** and modify files/variables therein

## double-comments
comments straing with ## will stay in the master-file only
```python
## this comment stays in the master-file only
# this comment will be transferred to the created reference file
```

