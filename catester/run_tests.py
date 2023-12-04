import argparse
import os
import pytest
from model import parse_yaml_file
#if not commented out => warning: PytestAssertRewriteWarning: Module already imported so cannot be rewritten: pytest_jsonreport
#from pytest_jsonreport.plugin import JSONReport
#plugin = JSONReport()

def run_tests():
    #default yaml file for testing/debugging purposes
    test_yaml = "../examples/ex1/test.yaml"
    test_report = "./output/test-report.json"

    dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(dir)

    test_yaml_resolved = os.path.abspath(os.path.join(dir, test_yaml))
    test_report_resolved = os.path.abspath(os.path.join(dir, test_report))

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default=test_yaml_resolved, help='test yaml input file')
    parser.add_argument("-o", "--output", default=test_report_resolved, help='json report output file')
    args = parser.parse_args()
    yamlfile = args.input
    reportfile = args.output

    #try parsing yaml-file:
    #it gets parsed in pytest as well
    #but do it here, to not start pytest with an unparseable yaml-file
    try:
        config = parse_yaml_file(yamlfile)
        #print(config)
    except Exception:
        raise
    
    #pytest config options
    #https://docs.pytest.org/en/stable/reference/reference.html#configuration-options
    retcode = pytest.main([
        f"--yamlfile={yamlfile}",
        f"--json-report-file={reportfile}",
        "--json-report-indent=2",
        "--json-report",
        #"--collect-only",
        #"--no-summary",
        #"--no-header",
        #"-v",
        #"-q",
    ])
    print(retcode)

if __name__ == '__main__':
    run_tests()
