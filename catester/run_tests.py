import argparse
import os
import pytest
from pathlib import Path
from pydantic import ValidationError
from model import parse_spec_file, parse_test_file
import subprocess
#if following line is not commented out => warning: PytestAssertRewriteWarning: Module already imported so cannot be rewritten: pytest_jsonreport
#from pytest_jsonreport.plugin import JSONReport
#plugin = JSONReport()

def get_output_directory(spec_yamlfile: str):
    dirabs = os.path.abspath(os.path.dirname(spec_yamlfile))
    specification = parse_spec_file(spec_yamlfile)
    output_dir = specification.testInfo.outputDirectory
    if not os.path.isabs(output_dir):
        output_dir = os.path.join(dirabs, output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def run_tests():
    #default yaml file for testing/debugging purposes
    spec_yaml = "../examples/ex1/specification.yaml"
    test_yaml = "../examples/ex1/test3.yaml"
    test_report = "report.json"

    dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(dir)

    spec_yaml_resolved = os.path.abspath(os.path.join(dir, spec_yaml))
    test_yaml_resolved = os.path.abspath(os.path.join(dir, test_yaml))

    # get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--specification", default=spec_yaml_resolved, help="specification yaml input file")
    parser.add_argument("-t", "--test", default=test_yaml_resolved, help="test yaml input file")
    parser.add_argument("-o", "--output", default=test_report, help="json report output file")
    args = parser.parse_args()
    spec_yamlfile = args.specification
    test_yamlfile = args.test

    test_yaml_fn = Path(test_yamlfile).stem
    reportfile = f"{test_yaml_fn}-{args.output}"

    #try parsing yaml-file:
    #it gets parsed in pytest as well
    #but do it here, to not start pytest with an unparseable yaml-file
    try:
        specification = parse_spec_file(spec_yamlfile)
        testsuite = parse_test_file(test_yamlfile)
        #print(specification)
        #print(testsuite)
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
    
    output_dir = get_output_directory(spec_yamlfile)
    reportfile = os.path.join(output_dir, reportfile)
    #pytest config options
    #https://docs.pytest.org/en/stable/reference/reference.html#configuration-options
    options = []
    options.append(f"--specyamlfile={spec_yamlfile}")
    options.append(f"--testyamlfile={test_yamlfile}")
    options.extend([
        f"--json-report-file={reportfile}",
        "--json-report-indent=2",
        "--json-report",
        # this is not working: (but when run as subprocess then it works!)
        #"--metadata xxxxx yyyyyy",
        #"--json-report-omit=collectors",
    ])
    #collectors, log, traceback, streams, warnings, keywords
    options.extend([
        #"--collect-only",
        #"--no-summary",
        #"--no-header",
        #"--verbose",
        #"-v",
        #"-q",
    ])

    # run as a subprocess
    #command = f"pytest --yamlfile={yamlfile} --verbose --json-report --json-report-file={reportfile} --json-report-indent=2 --json-report-omit collectors log traceback streams warnings keywords"
    #command = f"pytest --metadata xxxxx yyyyyy --yamlfile={yamlfile} --verbose --json-report --json-report-file={reportfile} --json-report-indent=2"
    #retcode = subprocess.run(command, shell=True)
    #print(retcode.returncode)

    retcode = pytest.main(options)
    print(retcode)

if __name__ == "__main__":
    run_tests()
