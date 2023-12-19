import argparse
import os
import pytest
from pydantic import ValidationError
from model import parse_spec_file, parse_test_file
import subprocess
#if following line is not commented out => warning: PytestAssertRewriteWarning: Module already imported so cannot be rewritten: pytest_jsonreport
#from pytest_jsonreport.plugin import JSONReport
#plugin = JSONReport()

def run_tests():
    #default yaml file for testing/debugging purposes
    spec_yaml = "../examples/ex1/specification.yaml"
    test_yaml = "../examples/ex1/test6.yaml"
    test_report = "./output/test-report.json"

    dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(dir)

    spec_yaml_resolved = os.path.abspath(os.path.join(dir, spec_yaml))
    test_yaml_resolved = os.path.abspath(os.path.join(dir, test_yaml))
    test_report_resolved = os.path.abspath(os.path.join(dir, test_report))

    # get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--specification", default=spec_yaml_resolved, help="specification yaml input file")
    parser.add_argument("-t", "--test", default=test_yaml_resolved, help="test yaml input file")
    parser.add_argument("-o", "--output", default=test_report_resolved, help="json report output file")
    args = parser.parse_args()
    spec_yamlfile = args.specification
    test_yamlfile = args.test
    reportfile = args.output

    #try parsing yaml-file:
    #it gets parsed in pytest as well
    #but do it here, to not start pytest with an unparseable yaml-file
    try:
        spec_config = parse_spec_file(spec_yamlfile)
        test_config = parse_test_file(test_yamlfile)
        #print(spec_config)
        #print(test_config)
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
