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

DEFAULTS = {
    "specification": {
        "studentDirectory": "student",
        "referenceDirectory": "reference",
        "testDirectory": "testprograms",
        "outputDirectory": "output",
        "artifactDirectory": "artifacts",
        "testVersion": "v1",
        "storeGraphicsArtifacts": None,
        "outputName": "testSummary.json",
        "isLocalUsage": False,
    },
    "testsuite": {
        "type": "python",
        "name": "Python Test Suite",
        "description": "Checks subtests and graphics",
        "version": "1.0",
    },
    "properties": {
        "qualification": QualificationEnum.verifyEqual,
        "failureMessage": "Some or all tests failed",
        "successMessage": "Congratulations! All tests passed",
        "relativeTolerance": 1.0e-15,
        "absoluteTolerance": 0.0,
        "timeout": 180.0,
    },
}

class CodeAbilityBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

class CodeAbilityTestCommon(BaseModel):
    qualification: Optional[QualificationEnum] = Field(default=None)
    relativeTolerance: Optional[float] = Field(gt=0, default=None)
    absoluteTolerance: Optional[float] = Field(ge=0, default=None)
    allowedOccuranceRange: Optional[List[int]] = Field(min_length=2, max_length=2, default=None)
    verbosity: Optional[int] = Field(ge=0, le=3, default=None)

class CodeAbilityTestCollectionCommon(CodeAbilityTestCommon):
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
    type: Optional[TypeEnum] = Field(default=TypeEnum.variable)
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
    qualification: Optional[QualificationEnum] = Field(default=DEFAULTS["properties"]["qualification"])
    failureMessage: Optional[str] = Field(min_length=1, default=DEFAULTS["properties"]["failureMessage"])
    successMessage: Optional[str] = Field(min_length=1, default=DEFAULTS["properties"]["successMessage"])
    relativeTolerance: Optional[float] = Field(gt=0, default=DEFAULTS["properties"]["relativeTolerance"])
    absoluteTolerance: Optional[float] = Field(ge=0, default=DEFAULTS["properties"]["absoluteTolerance"])
    timeout: Optional[float] = Field(ge=0, default=DEFAULTS["properties"]["timeout"])

class CodeAbilityTestSuite(CodeAbilityBase):
    properties: CodeAbilityTestProperty
    #optional:
    type: Optional[str] = Field(min_length=1, default=DEFAULTS["testsuite"]["type"])
    name: Optional[str] = Field(min_length=1, default=DEFAULTS["testsuite"]["name"])
    description: Optional[str] = Field(min_length=1, default=DEFAULTS["testsuite"]["description"])
    version: Optional[str] = Field(pattern=VERSION_REGEX, default=DEFAULTS["testsuite"]["version"])

class CodeAbilitySpecification(CodeAbilityBase):
    #optional:
    studentDirectory: Optional[str] = Field(min_length=1, default=DEFAULTS["specification"]["studentDirectory"])
    referenceDirectory: Optional[str] = Field(min_length=1, default=DEFAULTS["specification"]["referenceDirectory"])
    testDirectory: Optional[str] = Field(min_length=1, default=DEFAULTS["specification"]["testDirectory"])
    outputDirectory: Optional[str] = Field(min_length=1, default=DEFAULTS["specification"]["outputDirectory"])
    artifactDirectory: Optional[str] = Field(min_length=1, default=DEFAULTS["specification"]["artifactDirectory"])
    testVersion: Optional[str] = Field(min_length=1, default=DEFAULTS["specification"]["testVersion"])
    storeGraphicsArtifacts: Optional[bool] = Field(default=DEFAULTS["specification"]["storeGraphicsArtifacts"])
    outputName: Optional[str] = Field(min_length=1, default=DEFAULTS["specification"]["outputName"])
    isLocalUsage: Optional[bool] = Field(default=DEFAULTS["specification"]["isLocalUsage"])
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
