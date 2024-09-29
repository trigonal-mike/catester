import os
from convert import convert_master
from run_tests import DEFAULT_PYTESTFLAGS

""" please see doc/CONVERTER.md for detailed instructions """

# TESTRUNNER_DIR: name of directory where the tests should run
# best being placed next to repository "catester"
# this directory MUST be relative to this file (devconvert.py)
TESTRUNNER_DIR = "../../testrunner"

# INITIAL_META: yaml-file containing initial values for the generated meta.yaml file
# or None if initial values are not provided
INITIAL_META = "../../assignments/initial-meta.yaml"
#INITIAL_META = "../../catester-examples/initial-meta.yaml"
#INITIAL_META = None

# USE_FORMATTER: if files should be formatted or not
USE_FORMATTER = True
#USE_FORMATTER = False

# SUPPRESS_OUTPUT: suppress converter output or not
#SUPPRESS_OUTPUT = True
SUPPRESS_OUTPUT = False

# CONVERTER_ACTION: action for the converter
# None      ... run all (DEFAULT)
# "convert" ... just convert
# "test"    ... just run the tests
# "cleanup" ... just run cleanup
CONVERTER_ACTION = None
#CONVERTER_ACTION = "convert"
#CONVERTER_ACTION = "test"
#CONVERTER_ACTION = "cleanup"

# CATESTER_VERBOSITY: verbosity level for catester
# 0 ... no additional output
# 1 ... show exit-code (and additional output, ONLY if PYTEST_FLAGS are without "--no-summary" flag)
CATESTER_VERBOSITY = 0

# PYTEST_FLAGS: test flags for pytest
# https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags
PYTEST_FLAGS = DEFAULT_PYTESTFLAGS
#PYTEST_FLAGS = "-rA"
#PYTEST_FLAGS = "-ra,--tb=no,--no-header,--no-summary,-q"

# ASSIGNMENTS_DIR: name of directory containing the assignments or examples
ASSIGNMENTS_DIR = "../../assignments"
#ASSIGNMENTS_DIR = "../../catester-examples/dev_examples"
#ASSIGNMENTS_DIR = "../../catester-examples/examples"

# SCAN_DIR: actual assignment to test
# MUST be relative to ASSIGNMENTS_DIR

# these following are from python assignments - repository
SCAN_DIR = "Week01/01_math_constants"
#SCAN_DIR = "Week01/02_basis1"
#SCAN_DIR = "Week01/03_basis2"
#SCAN_DIR = "Week01/04_plot_docstr"
#SCAN_DIR = "Week01/05_simple_taylor"
#SCAN_DIR = "Week01/06_chars"
#SCAN_DIR = "Week01/07_osterformeln"
#SCAN_DIR = "Week02/01_vector_compute"
#SCAN_DIR = "Week02/02_vector_create"
#SCAN_DIR = "Week02/03_vector_random"
#SCAN_DIR = "Week02/04_basis3"
#SCAN_DIR = "Week02/05_sindex"
#SCAN_DIR = "Week02/06_Laboruebung1"
#SCAN_DIR = "Week02/07_Laboruebung2"
#SCAN_DIR = "Week03/01_Laboruebung3"
#SCAN_DIR = "Week03/02_Kerrzelle"
#SCAN_DIR = "Week03/03_EigeneFunktionen"
#SCAN_DIR = "Week03/04_cosinus_funktion"
#SCAN_DIR = "Week03/05_schwebung"
#SCAN_DIR = "Week03/06_3week_summary"
#SCAN_DIR = "Week04/01_datentypen"
#SCAN_DIR = "Week04/02_machine-precision"
#SCAN_DIR = "Week04/03_basis-char"
#SCAN_DIR = "Week04/04_steuer-if"
#SCAN_DIR = "Week04/05_if_vocal"
#SCAN_DIR = "Week04/06_regpol"
#SCAN_DIR = "Week04/07_brutto_netto"
#SCAN_DIR = "Week05/01_steuer_for"
#SCAN_DIR = "Week05/02_steuer_while"
#SCAN_DIR = "Week05/03_forsum"
#SCAN_DIR = "Week05/04_forsum_sin"
#SCAN_DIR = "Week05/05_gauss1d"
#SCAN_DIR = "Week05/06_quadgl"
#SCAN_DIR = "Week05/07_password_validator"
#SCAN_DIR = "Week06/01_slogic"
#SCAN_DIR = "Week06/02_slogcomp"
#SCAN_DIR = "Week06/03_pivot_index"
#SCAN_DIR = "Week06/04_quadgl"
#SCAN_DIR = "Week06/05_quadgleval"
#SCAN_DIR = "Week06/06_quadgltest"
#SCAN_DIR = "Week07/01_reihenentwicklung"
#SCAN_DIR = "Week07/02_darstellung_torus"
#SCAN_DIR = "Week07/03_einfache_animation"
#SCAN_DIR = "Week07/04_histogram"
#SCAN_DIR = "Week07/05_roman_numbers"
#SCAN_DIR = "Week07/06_dict_und_json"
#SCAN_DIR = "Week08/01_lambda"
#SCAN_DIR = "Week08/02_damped_oscillation"
#SCAN_DIR = "Week08/03_radioactive_decay"
#SCAN_DIR = "Week08/04_interpolate"
#SCAN_DIR = "Week08/05_hanoi"
#SCAN_DIR = "Week09/01_lingl_netzwerk"
#SCAN_DIR = "Week09/02_lingl_diagmatrix"
#SCAN_DIR = "Week09/03_lingl_kegelschnitte"
#SCAN_DIR = "Week09/04_vector_field"
#SCAN_DIR = "Week09/05_caesar"
#SCAN_DIR = "Week10/01_differentiate"
#SCAN_DIR = "Week10/02_integrate"
#SCAN_DIR = "Week10/03_pi_int"
#SCAN_DIR = "Week10/04_pendulum"
#SCAN_DIR = "Week10/05_pendulum_animation"
#SCAN_DIR = "Week11/01_uncertainties"
#SCAN_DIR = "Week11/02_pi_random"
#SCAN_DIR = "Week11/03_pi_series"
#SCAN_DIR = "Week11/04_pi_archimedes"
#SCAN_DIR = "Week11/05_pytest"
#SCAN_DIR = "Week12/01_planets"
#SCAN_DIR = "Week12/02_polynom"
#SCAN_DIR = "Week12/03_animals"

# these following are from catester-examples - repository (dev_examples)
#SCAN_DIR = "1_pskript"
#SCAN_DIR = "2_basis3"
#SCAN_DIR = "3_additional"
#SCAN_DIR = "4_pskript"
#SCAN_DIR = "5_seed"
#SCAN_DIR = "6_oster"
#SCAN_DIR = "7_setupcode"
#SCAN_DIR = "8_matplot"
#SCAN_DIR = "9_regexp"
#SCAN_DIR = "10_password"
#SCAN_DIR = "11_setupcode"
#SCAN_DIR = "12_animation"
#SCAN_DIR = "13_scipy"
#SCAN_DIR = "14_malicious"
#SCAN_DIR = "15_regexp"
#SCAN_DIR = "16_stdin"
#SCAN_DIR = "17_planets"

# these following are from catester-examples - repository (examples)
#SCAN_DIR = "aaa/bbb/ccc"
#SCAN_DIR = "basic"
#SCAN_DIR = "blacklist"
#SCAN_DIR = "datetime"
#SCAN_DIR = "docstring"
#SCAN_DIR = "empty"
#SCAN_DIR = "errorbar"
#SCAN_DIR = "existance"
#SCAN_DIR = "full"
#SCAN_DIR = "graphics"
#SCAN_DIR = "linting"
#SCAN_DIR = "matplot"
#SCAN_DIR = "malicious"
#SCAN_DIR = "minimal"
#SCAN_DIR = "new"
#SCAN_DIR = "open"
#SCAN_DIR = "pandas"
#SCAN_DIR = "pi_int"
#SCAN_DIR = "python_types"
#SCAN_DIR = "random"
#SCAN_DIR = "stdin"
#SCAN_DIR = "stdout"
#SCAN_DIR = "stdin_stdout"
#SCAN_DIR = "strings"
#SCAN_DIR = "structural"
#SCAN_DIR = "timeout"
#SCAN_DIR = "typecheck"
#SCAN_DIR = "vector_random"
#SCAN_DIR = "Week03_test_dependencies/Unit01"
#SCAN_DIR = "Week03_test_dependencies/Unit02"
#SCAN_DIR = "Week03_test_dependencies/Unit03"

if __name__ == "__main__":
    # get directory of this file 
    thisdir = os.path.dirname(__file__)

    # construct absulute paths for the converter
    testrunnerdir = os.path.abspath(os.path.join(thisdir, TESTRUNNER_DIR))
    assignmentsdir = os.path.abspath(os.path.join(thisdir, ASSIGNMENTS_DIR))
    scandir = os.path.abspath(os.path.join(assignmentsdir, SCAN_DIR))
    metayaml = None if INITIAL_META is None else os.path.abspath(os.path.join(thisdir, INITIAL_META))

    # run the converter
    convert_master(scandir, testrunnerdir, assignmentsdir, CONVERTER_ACTION, CATESTER_VERBOSITY, PYTEST_FLAGS, metayaml, USE_FORMATTER, SUPPRESS_OUTPUT)
