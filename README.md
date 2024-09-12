# catester
Python Testing Engine

NOTE: all the examples are put in an extra repository named "catester-examples",
and for development purposes best being placed next to this repository "catester"

## project folder structure
```
├── catester                    ... this repository
    ├── catester
        ├── converter
            ├── __init__.py     ... for exporting the Converter
            ├── conv.py         ... the actual Converter class
            └── settings.py     ... all possible settings for the Converter
        ├── metayaml            ... directory with default/template meta yaml
        ├── model
            ├── output          ... generated json schemas by model.py
            ├── __init__.py     ... empty file
            └── model.py        ... model definitions
        ├── tests
            ├── __init__.py     ... empty file
            ├── conftest.py     ... pytest setup, report generation, ...
            ├── execution.py    ... timeoutable execution helper
            ├── helper.py       ... helper functions
            ├── modules.py      ... for imported modules inspection
            └── test_class.py   ... contains the test entrypoint for pytest
        ├── convert.py          ... ---ENTRY FOR STARTING THE CONVERTER---
        ├── devconvert.py       ... for development purposes (convert/run tests)
        ├── devflags.py         ... helper for pytestflags used by devrun.py
        ├── devrun.py           ... for development purposes (run tests)
        ├── pytest.ini          ... pytest settings
        └── run_tests.py        ... ---MAIN ENTRY FOR STARTING PYTEST---
└── catester-examples           ... extra repository
    └── ex_master
        ├── _ex_                ... various development examples
        ├── examples            ... named test examples
        └── initial-meta.yaml   ... file containing initial meta specification
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

