import argparse
import os
import pytest
from pydantic import ValidationError
from model import parse_spec_file, parse_test_file

DEFAULT_SPECIFICATION = "specification.yaml"
DEFAULT_TEST = "test.yaml"
DEFAULT_OUTPUT = "report.json"
DEFAULT_INDENT = 2
DEFAULT_VERBOSITY = 0
WITH_JSON_REPORT = False

def run_tests(specification, test, output, indent, verbosity):
    cwd = os.getcwd()
    if not os.path.isabs(specification):
        specification = os.path.join(cwd, specification)
    if not os.path.isabs(test):
        test = os.path.join(cwd, test)

    #try parsing yaml-file:
    #it gets parsed in pytest as well
    #but do it here, to not start pytest with an unparseable/invalid yaml-file
    try:
        _specification = parse_spec_file(specification)
        _test = parse_test_file(test)
        #print(_specification)
        #print(_testsuite)
    except ValidationError as e:
        print("YAML File could not be validated")
        print(e)
        raise
    except FileNotFoundError as e:
        print("File not found")
        print(e)
        raise
    except Exception as e:
        print("Exception")
        print(e)
        raise
    
    dir = os.path.abspath(os.path.dirname(__file__))
    #pytest config options
    #https://docs.pytest.org/en/stable/reference/reference.html#configuration-options
    options = []
    options.extend([
        f"{dir}",
        f"--specification={specification}",
        f"--test={test}",
        f"--output={output}",
        f"--indent={indent}",
        f"--verbosity={verbosity}",
        #"--full-trace",
        #"--collect-only",
        #"--verbose",
        #"-vvvvvvv",
        #"-qqqqq",
        #"-x",
    ])
    if verbosity == 0:
        options.extend([
            #"--no-header",
            #"--no-summary",
        ])
    if WITH_JSON_REPORT:
        #json report not needed anymore!?
        options.extend([
            f"--json-report-file={None}",
            "--json-report-indent=2",
            "--json-report",
        ])

    retcode = pytest.main(options)
    print(retcode)

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--specification", default=DEFAULT_SPECIFICATION, help="specification yaml input file")
    parser.add_argument("-t", "--test", default=DEFAULT_TEST, help="test yaml input file")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="json report output file")
    parser.add_argument("-i", "--indent", default=DEFAULT_INDENT, help="json report output indentation in spaces")
    parser.add_argument("-v", "--verbosity", default=DEFAULT_VERBOSITY, help="verbosity level 0, 1, 2 or 3")

    args = parser.parse_args()
    run_tests(args.specification, args.test, args.output, args.indent, args.verbosity)
