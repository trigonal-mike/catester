import pytest

def run_tests():
    #pytest.register_assert_rewrite('pytest_jsonreport.plugin', 'JSONReport')
    #from pytest_jsonreport.plugin import JSONReport
    #plugin = JSONReport()
    # Execute pytest with the specified arguments
    #pytest.main(['-q'])  # Replace 'tests.yaml' with your test file
    #retcode = pytest.main(["--no-summary", "--no-header" , "-q"])
    #retcode = pytest.main(["--json-report", 'test/test_class.py'], plugins=[plugin])
    #retcode = pytest.main(["--json-report-indent=4"], plugins=[plugin])
    retcode = pytest.main(["--json-report-indent=4", "--json-report"])
    print(retcode)


if __name__ == "__main__":
    run_tests()
