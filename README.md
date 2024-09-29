# catester
Python Testing Engine

## documents
- [CONVERTER.md](doc/CONVERTER.md)
- [META-TOKENS.md](doc/META-TOKENS.md)
- [TEST-TOKENS.md](doc/TEST-TOKENS.md)

## catester examples
https://github.com/trigonal-mike/catester-examples

all examples are stored in an extra repository named "catester-examples",
and for development purposes best being placed next to this repository "catester"

## codeability assignments
https://gitlab.tugraz.at/codeability/itpcp/progphys/2024/python/assignments

for easy testing, developing of the codeability assignments, this repository should also be placed next to catester

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
├── catester-examples           ... extra repository (catester-examples)
    ├── dev_examples            ... various development examples
    ├── examples                ... named test examples
    └── initial-meta.yaml       ... file containing initial meta specification
├── assignments                 ... extra repository (codeability-assignments)
    ├── Week01
        ├── 01_math_constants   ... various development examples
            ├── assignment      ... named test examples
                ├── mediaFiles  ... optional files referenced by index.md
                └── index.md    ... markdown description of the assignment
            ├── localTests      ... solution folder (see CONVERTER.md)
            ├── mathc_master.py ... master-file with meta/test-pragmas
            ├── mathc.py        ... automatically created
            ├── meta.yaml       ... automatically created
            └── test.yaml       ... automatically created
        └── ... more assignments
    ├── ... more folders
    └── initial-meta.yaml       ... file containing initial meta specification
└── testrunner                  ... directory where actual test are copied to and run
```

## command line arguments for run_tests.py
run_tests.py uses following command line arguments:

| Argument | Default | Description |
| --- | --- | --- |
| --specification | specification.yaml | abs/rel path to specification file |
| --test | test.yaml | abs/rel path to testsuite file |
| --indent | 2 | indentation for the generated report |
| --verbosity | 0 | catester-verbosity level 0 or 1 |
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

## sandboxing:
- Wie kann das sinnvoll umgesetzt werden?
- Wie wird das in matlab gemacht?
- Wie kann/soll das in python gemacht werden?
- os.chroot würde sich anbieten, aber das geht nur mit root-Rechten, welche der test-worker (lt. Max) nicht haben darf!?
- jede einzelne Funktion "die raus kann" zu patchen, ist denke ich (viel) zu großer Aufwand

## Erweiterungen/Todos:
- Was soll geändert/hinzugefügt werden?
- verbosity ist zzt (noch) nicht ideal einstellbar

## Allowed/Disallowed Modules:
- moduleBlacklist ist umgesetzt
- eine whiteList ist nicht praktisch, weil zb. numpy insg. 176, und matplotlib insg. 338 weitere Module benötigt/importiert
