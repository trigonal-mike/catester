# converter
Python Testing Converter

## master file naming
the master filename has to end with **_master.py**

## converting and testing
For the first start, **ex1_master.py** is the only file needed, all other files and folders are automatically created

- **test.yaml** is the created test file
- **specification.yaml** is needed for the reference-solution path
- **localTests** contains directories which are getting tested,
directories starting with "_" are automatically created every time a test is run,
and should not be altered.
- **ex1.py** is the created reference solution (= ex1_master.py without comments)

## providing more solutions
the best way is to copy the contents of **_correctSolution** directory into an new directory under **localTests** and modify some variables in the copied **ex1.py** file

## example folder structure
```
└── ex_master
    ├── ex1
        ├── ex1_master.py
        ├── ex1.py
        ├── test.yaml
        ├── specification.yaml
        ├── localTests
            ├── _reference
                └── ex1.py
            ├── _correctSolution
                ├── test.yaml
                ├── student
                    └── ex1.py
                ├── output
                    └── report.json
                ├── ...
            ├── _emptySolution
                ├── test.yaml
                ├── student
                ├── output
                    └── report.json
                ├── ...
            ├── userSolution1
                ├── test.yaml
                ├── student
                    └── ex1.py
                ├── output
                    └── report.json
                ├── ...
            ├── userSolution2
            ├── userSolution3
            └── ...
    ├── ex2
    ├── ...
```

## command line arguments for convert.py

| Argument | Default | Description |
| --- | --- | --- |
| --scandir | none | if not set, current working directory is used |
| --action | all | 'all', 'test' or 'convert' |

## starting pytest with convert.py
python /abs/path/to/convert.py

python ../../rel/path/to/convert.py
