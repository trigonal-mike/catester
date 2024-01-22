import os
import subprocess
from run_tests import run_tests

# this file is for development purposes only
# facilitates starting local test-examples

def start_tests():
    #specification = "../examples/specification.yaml"
    specification = None
    #test = "../examples/ex1/test1.yaml"
    test = "../examples/ex2/test2.yaml"
    #output = "I:/x/report.json"
    #output = "./x/y/report.json"
    output = "report.json"
    indent = 2
    verbosity = 0

    dir = os.path.abspath(os.path.dirname(__file__))
    if specification is not None:
        specification = os.path.join(dir, specification)
    test = os.path.join(dir, test)

    run_tests(specification, test, output, indent, verbosity)

    # or run as subprocess
    #entry_file = os.path.join(dir, "run_tests.py")
    #command = f"python {entry_file} --specification={specification} --test={test} --output={output} --indent={indent} --verbosity={verbosity}"
    #retcode = subprocess.run(command, shell=True)
    #print(command)
    #print(retcode.returncode)

    # python i:\PYTHON\catester\catester\run_tests.py

if __name__ == "__main__":
    start_tests()
