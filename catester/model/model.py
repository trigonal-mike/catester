import json
import os
import yaml
from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field

DIRECTORIES = [
    "studentDirectory",
    "referenceDirectory",
    "testDirectory",
    "outputDirectory",
    "artifactDirectory",
]

class QualificationEnum(str, Enum):
    verifyEqual = "verifyEqual"
    matches = "matches"
    contains = "contains"
    startsWith = "startsWith"
    endsWith = "endsWith"
    count = "count"
    regexp = "regexp"


class TypeEnum(str, Enum):
    variable = "variable"
    graphics = "graphics"
    structural = "structural"
    linting = "linting"
    exist = "exist"
    error = "error"
    warning = "warning"
    help = "help"

VERSION_REGEX = "^([1-9]\d*|0)(\.(([1-9]\d*)|0)){0,3}$"

DEFAULT_SPECIFICATION_STUDENT_DIRECTORY = "student"
DEFAULT_SPECIFICATION_REFERENCE_DIRECTORY = "reference"
DEFAULT_SPECIFICATION_TEST_DIRECTORY = "testprograms"
DEFAULT_SPECIFICATION_OUTPUT_DIRECTORY = "output"
DEFAULT_SPECIFICATION_ARTIFACTS_DIRECTORY = "artifacts"
DEFAULT_SPECIFICATION_TEST_VERSION = "v1"
DEFAULT_SPECIFICATION_STORE_GRAPHICS_ARTIFACTS = None
DEFAULT_SPECIFICATION_OUTPUT_NAME = "testSummary.json"
DEFAULT_SPECIFICATION_IS_LOCAL_USAGE = False

DEFAULT_TESTSUITE_TYPE = "python"
DEFAULT_TESTSUITE_NAME = "Python Test Suite"
DEFAULT_TESTSUITE_DESCRIPTION = "Checks subtests and graphics"
DEFAULT_TESTSUITE_VERSION = "1.0"

DEFAULT_PROPERTY_TYPE = TypeEnum.variable
DEFAULT_PROPERTY_QUALIFICATION = QualificationEnum.verifyEqual
DEFAULT_PROPERTY_FAILURE_MESSAGE = "Some or all tests failed"
DEFAULT_PROPERTY_SUCCESS_MESSAGE = "Congratulations! All tests passed"
DEFAULT_PROPERTY_RELATIVE_TOLERANCE = 1.0e-15
DEFAULT_PROPERTY_ABSOLUTE_TOLERANCE = 0.0
DEFAULT_PROPERTY_TIMEOUT = 180


class CodeAbilityBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeAbilityTestCommon(BaseModel):
    qualification: Optional[QualificationEnum] = Field(default=None)
    relativeTolerance: Optional[float] = Field(gt=0, default=None)
    absoluteTolerance: Optional[float] = Field(ge=0, default=None)
    allowedOccuranceRange: Optional[List[int]] = Field(min_length=2, max_length=2, default=None)
    verbosity: Optional[int] = Field(ge=0, le=3, default=None)


class CodeAbilityTestCollectionCommon(CodeAbilityTestCommon):
    type: Optional[TypeEnum] = Field(default=None)
    timeout: Optional[float] = Field(ge=0, default=None)
    storeGraphicsArtifacts: Optional[bool] = Field(default=None)
    competency: Optional[str] = Field(min_length=1, default=None)


class CodeAbilityTest(CodeAbilityBase, CodeAbilityTestCommon):
    name: str = Field(min_length=1)
    #optional:
    value: Optional[Any] = Field(default=None)
    evalString: Optional[str] = Field(min_length=1, default=None)
    pattern: Optional[str] = Field(default=None)
    countRequirement: Optional[int] = Field(ge=0, default=None)
    failureMessage: Optional[str] = Field(default=None)
    successMessage: Optional[str] = Field(default=None)


class CodeAbilityTestCollection(CodeAbilityBase, CodeAbilityTestCollectionCommon):
    name: str = Field(min_length=1)
    tests: List[CodeAbilityTest]
    #optional:
    description: Optional[str] = Field(default=None)
    successDependency: Optional[str | int | List[str | int]] = Field(default=None)
    setUpCodeDependency: Optional[str] = Field(default=None)
    entryPoint: Optional[str] = Field(min_length=1, default=None)
    setUpCode: Optional[str | List[str]] = Field(default=None)
    tearDownCode: Optional[str | List[str]] = Field(default=None)
    id: Optional[str] = Field(default=None)
    file: Optional[str] = Field(default=None)
    failureMessage: Optional[str] = Field(default=None)
    successMessage: Optional[str] = Field(default=None)


class CodeAbilityTestProperty(CodeAbilityBase, CodeAbilityTestCollectionCommon):
    tests: List[CodeAbilityTestCollection]
    #optional:
    type: Optional[TypeEnum] = Field(default=DEFAULT_PROPERTY_TYPE)
    qualification: Optional[QualificationEnum] = Field(default=DEFAULT_PROPERTY_QUALIFICATION)
    failureMessage: Optional[str] = Field(min_length=1, default=DEFAULT_PROPERTY_FAILURE_MESSAGE)
    successMessage: Optional[str] = Field(min_length=1, default=DEFAULT_PROPERTY_SUCCESS_MESSAGE)
    relativeTolerance: Optional[float] = Field(gt=0, default=DEFAULT_PROPERTY_RELATIVE_TOLERANCE)
    absoluteTolerance: Optional[float] = Field(ge=0, default=DEFAULT_PROPERTY_ABSOLUTE_TOLERANCE)
    timeout: Optional[float] = Field(ge=0, default=DEFAULT_PROPERTY_TIMEOUT)


class CodeAbilityTestSuite(CodeAbilityBase):
    properties: CodeAbilityTestProperty
    #optional:
    type: Optional[str] = Field(min_length=1, default=DEFAULT_TESTSUITE_TYPE)
    name: Optional[str] = Field(min_length=1, default=DEFAULT_TESTSUITE_NAME)
    description: Optional[str] = Field(min_length=1, default=DEFAULT_TESTSUITE_DESCRIPTION)
    version: Optional[str] = Field(pattern=VERSION_REGEX, default=DEFAULT_TESTSUITE_VERSION)


class CodeAbilitySpecification(CodeAbilityBase):
    #optional:
    studentDirectory: Optional[str] = Field(min_length=1, default=DEFAULT_SPECIFICATION_STUDENT_DIRECTORY)
    referenceDirectory: Optional[str] = Field(min_length=1, default=DEFAULT_SPECIFICATION_REFERENCE_DIRECTORY)
    testDirectory: Optional[str] = Field(min_length=1, default=DEFAULT_SPECIFICATION_TEST_DIRECTORY)
    outputDirectory: Optional[str] = Field(min_length=1, default=DEFAULT_SPECIFICATION_OUTPUT_DIRECTORY)
    artifactDirectory: Optional[str] = Field(min_length=1, default=DEFAULT_SPECIFICATION_ARTIFACTS_DIRECTORY)
    testVersion: Optional[str] = Field(min_length=1, default=DEFAULT_SPECIFICATION_TEST_VERSION)
    storeGraphicsArtifacts: Optional[bool] = Field(default=DEFAULT_SPECIFICATION_STORE_GRAPHICS_ARTIFACTS)
    outputName: Optional[str] = Field(min_length=1, default=DEFAULT_SPECIFICATION_OUTPUT_NAME)
    isLocalUsage: Optional[bool] = Field(default=DEFAULT_SPECIFICATION_IS_LOCAL_USAGE)
    studentTestCounter: Optional[int] = Field(ge=0, default=None)


def parse_spec_file(file_path: str):
    # returns default if file_path is None
    config = {}
    if file_path is not None and len(file_path) > 0:
        with open(file_path, "r") as stream:
            config = yaml.safe_load(stream) or {}
    return CodeAbilitySpecification(**config)


def parse_test_file(file_path: str):
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)
    return CodeAbilityTestSuite(**config)


def get_schema(classname: BaseModel):
    schema = classname.model_json_schema()
    pretty = json.dumps(schema, indent=2)
    dir = os.path.abspath(os.path.dirname(__file__))
    name = f"{classname.__name__}_schema.json"
    schemafile = os.path.join(dir, "output", name)
    with open(schemafile, "w") as file:
        file.write(pretty)
    print(pretty)


#if this file is called directly, print json schema and save to file
if __name__ == "__main__":
    get_schema(CodeAbilitySpecification)
    get_schema(CodeAbilityTestSuite)

