import argparse
import yaml
from model import CodeAbilityTestSuite

def parse_yaml_file(file_path: str) -> dict:
    with open(file_path, 'r') as stream:
        config = yaml.safe_load(stream)    
    return CodeAbilityTestSuite(**config).model_dump()

def get_argument(argument, default):
    parser = argparse.ArgumentParser()
    parser.add_argument(*argument, default=default)
    args = parser.parse_args()
    return args.input

def execute_file(filename, namespace):
    with open(filename, 'r') as file:
        exec(compile(file.read(), filename, 'exec'), namespace)
