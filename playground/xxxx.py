import yaml
import pytest

def parse_test_suite(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_test(test_name, variable_name, variable_value):
    @pytest.mark.parametrize(variable_name, [variable_value])
    def run_test(variable):
        # Here you can execute the user provided script 'script.py' 
        # with the variable and perform the necessary tests
        print(f"Running test '{test_name}' with variable '{variable_name}' = {variable}")
        # Your test logic using the provided variable...

    run_test.__name__ = f"test_{test_name.lower().replace(' ', '_')}_variable_{variable_name.lower().replace(' ', '_')}"
    return run_test

def create_tests_from_config(config):
    for test in config.get('tests', []):
        test_name = test['name']
        for variable in test.get('variables', []):
            test_function = generate_test(test_name, variable['name'], variable['value'])
            globals()[test_function.__name__] = test_function

if __name__ == "__main__":
    test_suite = parse_test_suite('tests.yaml')
    create_tests_from_config(test_suite)
    retcode = pytest.main()
    #retcode = pytest.main([pytestconfig, "--no-summary", "--no-header" , "-q"])
    #retcode = pytest.main(["--json-report", 'test/test_class.py'], plugins=[plugin])
    print(globals())
    print(retcode)


def test_xxx():
    assert 1==1