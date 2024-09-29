# devconvert.py

run devconvert.py for automatically creating associated files/folders and running local tests of an example

you have to provide a folder with a containing **[some-file-name]_master.py** file

# associated files/folders
associated files are created following the instructions (pragmas, tokens) set in a **_master.py** file

assume a folder containing **ex1_master.py**

the created files/folders are:
- **meta.yaml** - file containing test meta-information
- **test.yaml** - file containing actual tests, which sould be performed, when the tests are run
- **ex1.py** - file with reference solution
- **localTests** - folder containing local tests
- **localTests/_reference** - folder containing the reference Solution
- **localTests/_correctSolution** - folder containing the correct Solution (i.e. the reference Solution)
- **localTests/_emptySolution** - folder containing the empty Solution (no files)

# settings for devconvert.py
all important settings for devconvert.py are explained here

## TESTRUNNER_DIR

this sould point to the directory where the tests should run, best being placed next to repository "catester", this directory MUST be relative to devconvert.py

e.g.: TESTRUNNER_DIR = "../../testrunner"

this directory will be created by devconvert, if it does not exist

## INITIAL_META
points to the file containing initial values for the generated meta.yaml file

e.g.: INITIAL_META = "../../assignments/initial-meta.yaml"

can be **NONE** if initial values are not provided

## USE_FORMATTER
**True** if files should be formatted or **False** if not

e.g.: USE_FORMATTER = True

## SUPPRESS_OUTPUT
if converter output should be suppressed or not

e.g.: SUPPRESS_OUTPUT = False

## CONVERTER_ACTION
action for the converter
- **None** - run all (cleanup => convert => test)
- **"convert"** - just convert, i.e. create associated files and test folders
- **"test"** - just run the tests
- **"cleanup"** - just run the cleanup, i.e. delete associated files and test folders

e.g.: CONVERTER_ACTION = None

## CATESTER_VERBOSITY
verbosity level for catester
- 0, without additional output
- 1, show exit-code (and additional output, ONLY if PYTEST_FLAGS are without "--no-summary" flag)
CATESTER_VERBOSITY = 0

## PYTEST_FLAGS
test flags for pytest, further information can be found here:

https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags

examples:
- PYTEST_FLAGS = DEFAULT_PYTESTFLAGS
- PYTEST_FLAGS = "-rA"
- PYTEST_FLAGS = "-ra,--tb=no,--no-header,--no-summary,-q"

these flags can also be created with a helper function from devflags.py:
```
PYTEST_FLAGS = get_pytest_flags(
    reportPassed = False,
    withHeader = False,
    withSummary = False,
    withTraceback = True,
    fullTraceback = False,
    collectOnly = False,
    showFixtures = False,
    showLocals = False,
    exitOnFirstError = False,
    verbosity = -1
)
```

## ASSIGNMENTS_DIR
name of directory containing the assignments or examples

examples:
- ASSIGNMENTS_DIR = "../../assignments"
- ASSIGNMENTS_DIR = "../../catester-examples/dev_examples"
- ASSIGNMENTS_DIR = "../../catester-examples/examples"

## SCAN_DIR
actual assignment to test, MUST be relative to ASSIGNMENTS_DIR

examples for (assignments):
- SCAN_DIR = "Week01/01_math_constants"
- SCAN_DIR = "Week01/02_basis1"
- SCAN_DIR = "Week01/03_basis2"

examples for (catester-examples/dev_examples):
- SCAN_DIR = "1_pskript"
- SCAN_DIR = "2_basis3"
- SCAN_DIR = "3_additional"

examples for (catester-examples/examples):
- SCAN_DIR = "basic"
- SCAN_DIR = "blacklist"
- SCAN_DIR = "datetime"
