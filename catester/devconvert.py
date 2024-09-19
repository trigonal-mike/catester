import os
from convert import convert_master
from run_tests import DEFAULT_PYTESTFLAGS

if __name__ == "__main__":
    action = None
    #action = "convert"
    #action = "test"
    #action = "cleanup"

    #catester-verbosity
    verbosity = 0

    #test flags:
    #https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags
    pytestflags = DEFAULT_PYTESTFLAGS
    #pytestflags = "-rA"
    pytestflags = "-ra,--tb=no,--no-header,--no-summary,-q"

    #ex_master/_ex_:
    #scandir = "../../catester-examples/ex_master/_ex_/1"
    #scandir = "../../catester-examples/ex_master/_ex_/2"
    #scandir = "../../catester-examples/ex_master/_ex_/3"
    #scandir = "../../catester-examples/ex_master/_ex_/4"
    #scandir = "../../catester-examples/ex_master/_ex_/5"
    #scandir = "../../catester-examples/ex_master/_ex_/6"
    #scandir = "../../catester-examples/ex_master/_ex_/7"
    #scandir = "../../catester-examples/ex_master/_ex_/8"
    #scandir = "../../catester-examples/ex_master/_ex_/9"
    #scandir = "../../catester-examples/ex_master/_ex_/10"
    #scandir = "../../catester-examples/ex_master/_ex_/11"
    #scandir = "../../catester-examples/ex_master/_ex_/12"
    #scandir = "../../catester-examples/ex_master/_ex_/13"
    #scandir = "../../catester-examples/ex_master/_ex_/14"
    #scandir = "../../catester-examples/ex_master/_ex_/15"
    #scandir = "../../catester-examples/ex_master/_ex_/16"
    #scandir = "../../catester-examples/ex_master/_ex_/17"

    #ex_master/examples:
    #scandir = "../../catester-examples/ex_master/examples/aaa/bbb/ccc"
    #scandir = "../../catester-examples/ex_master/examples/basic"
    #scandir = "../../catester-examples/ex_master/examples/blacklist"
    #scandir = "../../catester-examples/ex_master/examples/datetime"
    #scandir = "../../catester-examples/ex_master/examples/docstring"
    #scandir = "../../catester-examples/ex_master/examples/empty"
    #scandir = "../../catester-examples/ex_master/examples/errorbar"
    #scandir = "../../catester-examples/ex_master/examples/existance"
    #scandir = "../../catester-examples/ex_master/examples/full"
    #scandir = "../../catester-examples/ex_master/examples/graphics"
    #scandir = "../../catester-examples/ex_master/examples/linting"
    #scandir = "../../catester-examples/ex_master/examples/matplot"
    #scandir = "../../catester-examples/ex_master/examples/malicious"
    #scandir = "../../catester-examples/ex_master/examples/minimal"
    #scandir = "../../catester-examples/ex_master/examples/new"
    #scandir = "../../catester-examples/ex_master/examples/open"
    #scandir = "../../catester-examples/ex_master/examples/pandas"
    #scandir = "../../catester-examples/ex_master/examples/pi_int"
    #scandir = "../../catester-examples/ex_master/examples/python_types"
    #scandir = "../../catester-examples/ex_master/examples/random"
    #scandir = "../../catester-examples/ex_master/examples/stdin"
    #scandir = "../../catester-examples/ex_master/examples/stdout"
    #scandir = "../../catester-examples/ex_master/examples/strings"
    #scandir = "../../catester-examples/ex_master/examples/structural"
    #scandir = "../../catester-examples/ex_master/examples/timeout"
    #scandir = "../../catester-examples/ex_master/examples/typecheck"
    #scandir = "../../catester-examples/ex_master/examples/vector_random"
    #scandir = "../../catester-examples/ex_master/examples/Week03/Unit01"
    #scandir = "../../catester-examples/ex_master/examples/Week03/Unit02"

    #assignments:
    #scandir = "../../assignments/Week01/01_math_constants"
    #scandir = "../../assignments/Week01/02_basis1"
    #scandir = "../../assignments/Week01/03_basis2"
    #scandir = "../../assignments/Week01/04_plot_docstr"
    #scandir = "../../assignments/Week01/05_simple_taylor"
    #scandir = "../../assignments/Week01/06_chars"
    #scandir = "../../assignments/Week01/07_osterformeln"
    #scandir = "../../assignments/Week02/01_vector_compute"
    #scandir = "../../assignments/Week02/02_vector_create"
    #scandir = "../../assignments/Week02/03_vector_random"
    #scandir = "../../assignments/Week02/04_basis3"
    #scandir = "../../assignments/Week02/05_sindex"
    #scandir = "../../assignments/Week02/06_Laboruebung1"
    #scandir = "../../assignments/Week02/07_Laboruebung2"
    #scandir = "../../assignments/Week03/01_Laboruebung3"
    #scandir = "../../assignments/Week03/02_Kerrzelle"
    #scandir = "../../assignments/Week03/03_EigeneFunktionen"
    #scandir = "../../assignments/Week03/04_cosinus_funktion"
    #scandir = "../../assignments/Week03/05_schwebung"
    #scandir = "../../assignments/Week03/06_3week_summary"
    #scandir = "../../assignments/Week04/01_datentypen"
    #scandir = "../../assignments/Week04/02_machine-precision"
    #scandir = "../../assignments/Week04/03_basis-char"
    #scandir = "../../assignments/Week04/04_steuer-if"
    #scandir = "../../assignments/Week04/05_if_vocal"
    #scandir = "../../assignments/Week04/06_regpol"
    #scandir = "../../assignments/Week04/07_brutto_netto"
    #scandir = "../../assignments/Week05/01_steuer_for"
    #scandir = "../../assignments/Week05/02_steuer_while"
    #scandir = "../../assignments/Week05/03_forsum"
    #scandir = "../../assignments/Week05/04_forsum_sin"
    #scandir = "../../assignments/Week05/05_gauss1d"
    #scandir = "../../assignments/Week05/06_quadgl"
    #scandir = "../../assignments/Week05/07_password_validator"
    #scandir = "../../assignments/Week06/01_slogic"
    #scandir = "../../assignments/Week06/02_slogcomp"
    #scandir = "../../assignments/Week06/03_pivot_index"
    #scandir = "../../assignments/Week06/04_quadgl"
    #scandir = "../../assignments/Week06/05_quadgleval"
    #scandir = "../../assignments/Week06/06_quadgltest"
    #scandir = "../../assignments/Week07/01_reihenentwicklung"
    #scandir = "../../assignments/Week07/02_darstellung_torus"
    #scandir = "../../assignments/Week07/03_einfache_animation"
    #scandir = "../../assignments/Week07/04_histogram"
    #scandir = "../../assignments/Week07/05_roman_numbers"
    #scandir = "../../assignments/Week07/06_dict_und_json"
    #scandir = "../../assignments/Week08/01_lambda"
    #scandir = "../../assignments/Week08/02_damped_oscillation"
    #scandir = "../../assignments/Week08/03_radioactive_decay"
    #scandir = "../../assignments/Week08/04_interpolate"
    #scandir = "../../assignments/Week08/05_hanoi"
    #scandir = "../../assignments/Week09/01_lingl_netzwerk"
    #scandir = "../../assignments/Week09/02_lingl_diagmatrix"
    #scandir = "../../assignments/Week09/03_lingl_kegelschnitte"
    #scandir = "../../assignments/Week09/04_vector_field"
    #scandir = "../../assignments/Week09/05_caesar"
    #scandir = "../../assignments/Week10/01_differentiate"
    #scandir = "../../assignments/Week10/02_integrate"
    #scandir = "../../assignments/Week10/03_pi_int"
    #scandir = "../../assignments/Week10/04_pendulum"
    #scandir = "../../assignments/Week10/05_pendulum_animation"
    #scandir = "../../assignments/Week11/01_uncertainties"
    #scandir = "../../assignments/Week11/02_pi_random"
    #scandir = "../../assignments/Week11/03_pi_series"
    #scandir = "../../assignments/Week11/04_pi_archimedes"
    #scandir = "../../assignments/Week11/05_pytest"
    #scandir = "../../assignments/Week12/01_planets"
    #scandir = "../../assignments/Week12/02_polynom"
    scandir = "../../assignments/Week12/03_animals"

    metayaml = "../../assignments/initial-meta.yaml"

    dir = os.path.dirname(__file__)
    scandir = os.path.abspath(os.path.join(dir, scandir))
    metayaml = os.path.abspath(os.path.join(dir, metayaml))

    """ put testrunner directory outside of catester """
    testrunnerdir = "../../testrunner"
    testrunnerdir = os.path.abspath(os.path.join(dir, testrunnerdir))
    #assignmentsdir = "../../catester-examples/ex_master/_ex_"
    #assignmentsdir = "../../catester-examples/ex_master/examples"
    assignmentsdir = "../../assignments"
    assignmentsdir = os.path.abspath(os.path.join(dir, assignmentsdir))

    formatter = True #or false (if formatting of files is not required)

    convert_master(scandir, testrunnerdir, assignmentsdir, action, verbosity, pytestflags, metayaml, formatter)
