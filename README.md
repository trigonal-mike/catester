# catester
Python Testing Engine

## project folder structure
```
└── catester
    ├── catester
        ├── model
            ├── output          ... generated json schemas by model.py
            └── model.py        ... model definitions
        ├── tests
            ├── conftest.py     ... test setup, report generation, ...
            ├── execution.py    ... timeoutable execution helper
            ├── test_class.py   ... this class gets tested by pytest
        ├── devrun.py           ... for development purposes
        ├── pytest.ini          ... pytest settings
        └── run_tests.py        ... ---MAIN ENTRY---
    ├── examples                ... test examples
        ├── ex1
            ├── student         ... student files
            ├── reference       ... reference files
            ├── output          ... JSON-Report output
            ├── artifacts       ... generated images/data/etc
            ├── testprograms    ... additional test programs
            └── test.yaml       ... file containing testsuite
        ├── ex2
        ├── ...
        └── specification.yaml  ... file containing specification
```

## command line arguments for run_tests.py
run_tests.py uses following command line arguments:

| Argument | Default | Description |
| --- | --- | --- |
| --specification | specification.yaml | abs/rel path to specification file |
| --test | test.yaml | abs/rel path to testsuite file |
| --indent | 2 | indentation for the generated report |
| --verbosity | 0 | catester-verbosity level [0,1,2,3] |
| --pytestflags | -ra,--tb=no | comma-separated flags, for configuring pytest |

## pytestflags
pytest command-line-flags

https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags

e.g. set verbosity of pytest with --pytestflags

DEFAULT-Setting: report all but PASSED, no traceback


## starting pytest with run_tests.py
python ./run_tests.py

python /abs/path/to/run_tests.py

python ../../rel/path/to/run_tests.py --specification=../specification.yaml

# Plugins used

## Pytest-Metadata
https://pypi.org/project/pytest-metadata/
- this plugin provides environment data (platform, python version, plugins)

