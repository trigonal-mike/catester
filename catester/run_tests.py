import argparse
import os
import pytest
from pydantic import ValidationError
from model import parse_spec_file, parse_test_file

DEFAULT_SPECIFICATION = None
DEFAULT_TEST = "test.yaml"
DEFAULT_INDENT = 2
DEFAULT_VERBOSITY = 0

def run_tests(specification, test, indent, verbosity):
    cwd = os.getcwd()
    if specification is not None and not os.path.isabs(specification):
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
    #pytest command-line-flags
    #https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags
    options = []
    options.extend([
        f"{dir}",
        f"--test={test}",
        f"--indent={indent}",
        f"--verbosity={verbosity}",
        "-rA",
        "--tb=no",
        #"--fixtures",
        #"--collect-only",
        #"--showlocals",
        #"--tb=line",
        #"--full-trace",
        #"--verbose",
        #"-vv",
        #"-qq",
        #"-x",
    ])
    if specification is not None:
        options.append(f"--specification={specification}")
    if verbosity == 0:
        options.extend([
            #"--no-header",
            #"--no-summary",
        ])

    retcode = pytest.main(options)
    print(retcode)

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--specification", default=DEFAULT_SPECIFICATION, help="specification yaml input file")
    parser.add_argument("-t", "--test", default=DEFAULT_TEST, help="test yaml input file")
    parser.add_argument("-i", "--indent", default=DEFAULT_INDENT, help="json report output indentation in spaces")
    parser.add_argument("-v", "--verbosity", default=DEFAULT_VERBOSITY, help="verbosity level 0, 1, 2 or 3")

    args = parser.parse_args()
    run_tests(args.specification, args.test, args.indent, args.verbosity)
