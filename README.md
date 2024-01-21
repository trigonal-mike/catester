# catester
Python Testing Library

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
            ├── artefacts       ... generated images/data/etc
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
| --output | report.json | abs/rel file name of generated json-report |
| --indent | 2 | indentation for the generated report |
| --verbosity | 0 | verbosity level [0,1,2,3] |

if --output is relative path, then it is relative to **specification.testInfo.outputDirectory**

## starting pytest with run_tests.py
python ./run_tests.py

python /abs/path/to/run_tests.py

python ../../rel/path/to/run_tests.py --specification=../specification.yaml

# TODOS

## Timeout (stopit vs func_timeout):

stopit:
https://pypi.org/project/stopit/

- License MIT

func_timeout:
https://pypi.org/project/func-timeout/

- License LGPLv2

https://pypi.org/project/stopit/#signaling-based-resources

https://pypi.org/project/stopit/#comparing-thread-based-and-signal-based-timeout-control

Can’t interrupt a long Python atomic instruction. e.g. if time.sleep(20.0) is actually executing, the timeout will take effect at the end of the execution of this line.

**func_timeout** seems to has solved it for windows as well, but its license is LGPLv2, do we want/need that?

## Pytest-JSON-Report
https://pypi.org/project/pytest-json-report/
- incompatible with metadata (environment is not set)
- do we need it actually?

## Pytest-Metadata
https://pypi.org/project/pytest-metadata/
- this plugin provides environment data (platform, python version, plugins)

