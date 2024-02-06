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


class CodeAbilityBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeAbilityTestCommon(BaseModel):
    qualification: Optional[QualificationEnum] = Field(default=None)
    relativeTolerance: Optional[float] = Field(gt=0, default=None)
    absoluteTolerance: Optional[float] = Field(ge=0, default=None)
    allowedOccuranceRange: Optional[List[int]] = Field(min_length=2, max_length=2, default=None)
    verbosity: Optional[int] = Field(ge=0, le=3, default=None)


class CodeAbilityTestCollectionCommon(CodeAbilityTestCommon):
    storeGraphicsArtifacts: Optional[bool] = Field(default=None)
    competency: Optional[str] = Field(min_length=1, default=None)
    timeout: Optional[float] = Field(ge=0, default=None)


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
    qualification: Optional[QualificationEnum] = Field(default=QualificationEnum.verifyEqual)
    failureMessage: Optional[str] = Field(min_length=1, default="Some or all tests failed")
    successMessage: Optional[str] = Field(min_length=1, default="Congratulations! All tests passed")


class CodeAbilityTestSuite(CodeAbilityBase):
    properties: CodeAbilityTestProperty
    #optional:
    type: Optional[str] = Field(min_length=1, default="python")
    name: Optional[str] = Field(min_length=1, default="Python Test Suite")
    description: Optional[str] = Field(min_length=1, default="Checks subtests and graphics")
    version: Optional[str] = Field(pattern="^1.0$", default="1.0")


class CodeAbilitySpecification(CodeAbilityBase):
    #optional:
    studentDirectory: Optional[str] = Field(min_length=1, default="student")
    referenceDirectory: Optional[str] = Field(min_length=1, default="reference")
    testDirectory: Optional[str] = Field(min_length=1, default="testprograms")
    outputDirectory: Optional[str] = Field(min_length=1, default="output")
    artifactDirectory: Optional[str] = Field(min_length=1, default="artifacts")
    studentTestCounter: Optional[int] = Field(ge=0, default=None)
    testVersion: Optional[str] = Field(min_length=1, default="v1")
    storeGraphicsArtifacts: Optional[bool] = Field(default=None)
    outputName: Optional[str] = Field(min_length=1, default="testSummary.json")
    isLocalUsage: Optional[bool] = Field(default=False)


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

