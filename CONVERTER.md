# converter
Python Testing Converter

## master file naming
the master filename has to end with **_master.py**

## converting and testing
For the first start, **ex1_master.py** is the only file needed, all other files and folders are automatically created

- **meta.yaml** is the created meta file
- **test.yaml** is the created test file
- **specification.yaml** is needed for the reference-solution path
- **localTests** contains directories which are getting tested,
directories starting with "_" are automatically created every time a test is run,
and should not be altered.
- **ex1.py** is the created reference solution (= ex1_master.py without double-comments '##' and without tokens '#$TOKENNAME')

## tokens
token format: `#$TOKENNAME ARGUMENT VALUE`
valid token names see [here](catester/converter/settings.py#L4)

## providing more solutions
the best way is to copy the contents of **_correctSolution** directory into an new directory under **localTests** and modify some variables in the copied **ex1.py** file

## example folder structure
```
└── ex_master
    ├── ex1
        ├── ex1_master.py
        ├── ex1.py
        ├── meta.yaml
        ├── test.yaml
        ├── specification.yaml
        ├── localTests
            ├── _reference
                └── ex1.py
            ├── _correctSolution
                ├── meta.yaml
                ├── test.yaml
                ├── student
                    └── ex1.py
                ├── output
                    └── report.json
                ├── ...
            ├── _emptySolution
                ├── meta.yaml
                ├── test.yaml
                ├── student
                ├── output
                    └── report.json
                ├── ...
            ├── userSolution1
                ├── meta.yaml
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
| --action | all | 'all', 'cleanup', 'test' or 'convert' |
| --verbosity | 0 | 0, 1, 2 or 3 |
| --pytestflags | -ra,--tb=no | comma-separated flags, for configuring pytest |
| --metayaml | none | abs/rel path to initial meta.yaml |
| --formatter | true | use black as formatter |
| --testdirs | all | 'all', 'none', 'correct' or 'empty', local test directories to include for action |

if `--metayaml` is set, that file will be the initial configuration for the created meta.yaml file

if `--metayaml` is not set, the default configuration will be used, see [here](catester/metayaml/_meta-default.yaml)

## starting pytest with convert.py
python /abs/path/to/convert.py

python ../../rel/path/to/convert.py

## flake8 linter options
https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-ignore

## code formatter
https://pypi.org/project/black/

