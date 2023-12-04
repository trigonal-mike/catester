# catester
Python Testing Library

## CLI - python
### Absolute path:

python run_tests.py --input=/path/to/test.yaml --output=/path/to/report.json

python run_tests.py --input=I:\PYTHON\catester\examples\ex1\test.yaml

### Relative path:

python run_tests.py --input=../examples/ex1/test.yaml


## CLI - pytest
working directory: ./catester

### Absolute path:

pytest --yamlfile=/path/to/test.yaml

pytest --yamlfile=I:\PYTHON\catester\examples\ex1\test.yaml

### Relative path:

pytest --yamlfile=../examples/ex1/test.yaml

