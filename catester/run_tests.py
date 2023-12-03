import pytest
from helpers import parse_yaml_file, get_argument
#from pytest_jsonreport.plugin import JSONReport
#plugin = JSONReport()

def run_tests():
    yamlfile = get_argument(("-i", "--input"), "../examples/ex1/test.yaml")
    reportfile = "test-report.json"
    config = parse_yaml_file(yamlfile)
    #print(config)
    retcode = pytest.main([
        f"--yamlfile={yamlfile}",
        #"--collect-only" ,
        f"--json-report-file={reportfile}",
        "--json-report-indent=4",
        "--json-report",
        #"--no-summary",
        #"--no-header",
        #"-v",
        #"-q"
    ])
    print(retcode)

if __name__ == '__main__':
    run_tests()
