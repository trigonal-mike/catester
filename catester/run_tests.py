import pytest
from helpers import parse_yaml_file, get_argument
#from pytest_jsonreport.plugin import JSONReport
#plugin = JSONReport()

def run_tests():
    #yamlfile = get_argument(("-i", "--input"), "./codeabilityTest_1.yaml")
    yamlfile = get_argument(("-i", "--input"), "../examples/ex1/test.yaml")
    config = parse_yaml_file(yamlfile)
    print(config)
    pytestconfig = f"--yamlfile={yamlfile}"
    #retcode = pytest.main([pytestconfig])
    #retcode = pytest.main([pytestconfig, "--no-summary", "--no-header" , "-q"])
    #retcode = pytest.main(["--json-report", 'test/test_class.py'], plugins=[plugin])
    retcode = pytest.main([pytestconfig, "--json-report-indent=4", "--json-report"])
    print(retcode)

if __name__ == '__main__':
    run_tests()
