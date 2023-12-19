import json
import os
import yaml
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class QualificationEnum(str, Enum):
    verifyEqual = "verifyEqual"
    matches = "matches"
    contains = "contains"
    startsWith = "startsWith"
    endsWith = "endsWith"
    count = "count"
    regexp = "regexp"
    verification = "verification"


class TypeEnum(str, Enum):
    variable = "variable"
    graphics = "graphics"
    structural = "structural"
    linting = "linting"
    exist = "exist"
    error = "error"
    warning = "warning"
    help = "help"


class CodeAbilityTestTemplate(BaseModel):
    evalName: Optional[str] = Field(min_length=1, default=None)
    name: str = Field(min_length=1)
    description: Optional[str] = Field(default=None)
    failureMessage: Optional[str] = Field(default=None)
    successMessage: Optional[str] = Field(default=None)
    type: Optional[TypeEnum] = None
    successDependency: Optional[str | List[str]] = Field(default=None)
    #allowedOccuranceRange: Optional[List[int]] = Field(min_length=2, max_length=2, default=None)


class CodeAbilityBaseTestTemplate(BaseModel):
    verbosity: Optional[int] = Field(ge=1, le=3, default=None)
    competency: Optional[str] = Field(min_length=1, default=None)


class CodeAbilityBaseTemplate(BaseModel):
    relativeTolerance: Optional[float] = Field(gt=0, default=None)
    absoluteTolerance: Optional[float] = Field(ge=0, default=None)
    qualification: Optional[QualificationEnum] = None


class CodeAbilitySubTest(CodeAbilityBaseTemplate, CodeAbilityTestTemplate):
    model_config = ConfigDict(extra='forbid')
    value: Optional[Any] = None
    evalString: Optional[str] = Field(min_length=1, default=None)
    pattern: Optional[str] = Field(default=None)
    countRequirement: Optional[int] = Field(ge=0, default=None)
    options: Optional[Dict] = None
    verificationFunction: Optional[str] = Field(min_length=1, default=None)


class CodeAbilityTest(CodeAbilityBaseTemplate, CodeAbilityBaseTestTemplate, CodeAbilityTestTemplate):
    model_config = ConfigDict(extra='forbid')
    setUpCode: Optional[str | List[str]] = Field(default=None)
    tearDownCode: Optional[str | List[str]] = Field(default=None)
    setUpCodeDependency: Optional[str] = Field(default=None)
    id: Optional[str] = Field(default=None)
    file: Optional[str] = Field(default=None)
    tests: Optional[List[CodeAbilitySubTest]] = Field(default=None)
    #have to exec, need the main entrypoint
    #not just as simple as "python file.py"
    #maybe put it anyway into setUpCode?
    entryPoint: Optional[str] = Field(min_length=1, default=None)


class CodeAbilityTestProperty(CodeAbilityBaseTemplate, CodeAbilityBaseTestTemplate):
    model_config = ConfigDict(extra='forbid')
    tests: List[CodeAbilityTest] = None
    #where are the following needed?
    studentFileList: Optional[List[str]] = Field(default=None)
    studentCommandList: Optional[List[str]] = Field(default=None)
    referenceFileList: Optional[List[str]] = Field(default=None)
    referenceCommandList: Optional[List[str]] = Field(default=None)


class CodeAbilityTestSuite(BaseModel):
    model_config = ConfigDict(extra='forbid')
    type: Optional[str] = Field(min_length=1, default="python")
    name: Optional[str] = Field(min_length=1, default="Python Test Suite")
    description: Optional[str] = Field(min_length=1, default="Checks subtests and graphics")
    version: Optional[str] = Field(pattern="^1.0$", default="1.0")
    failureMessage: Optional[str] = Field(min_length=1, default="Some or all tests failed")
    successMessage: Optional[str] = Field(min_length=1, default="Congratulations! All tests passed")
    storeGraphicsArtefacts: Optional[bool] = Field(default=False)
    properties: CodeAbilityTestProperty


class CodeAbilityTestInfo(BaseModel):
    model_config = ConfigDict(extra='forbid')
    executionDirectory: Optional[str] = Field(min_length=1, default=os.getcwd())
    referenceDirectory: Optional[str] = Field(min_length=1, default="reference")
    studentDirectory: Optional[str] = Field(min_length=1, default="student")
    testDirectory: Optional[str] = Field(min_length=1, default="testprograms")
    outputDirectory: Optional[str] = Field(min_length=1, default="output")
    artefactDirectory: Optional[str] = Field(min_length=1, default="artefacts")
    studentTestCounter: Optional[int] = Field(ge=0, default=None)
    testVersion: Optional[str] = Field(min_length=1, default="v1")
    studentTestCounter: Optional[int] = Field(ge=0, default=None)


class CodeAbilitySpecification(BaseModel):
    model_config = ConfigDict(extra='forbid')
    testInfo: CodeAbilityTestInfo


def parse_spec_file(file_path: str) -> dict:
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)
    return CodeAbilitySpecification(**config).model_dump()


def parse_test_file(file_path: str) -> dict:
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)
    return CodeAbilityTestSuite(**config).model_dump()


def get_spec_schema():
    schema = CodeAbilityTestSuite.model_json_schema()
    pretty = json.dumps(schema, indent=2)
    print(pretty)

    dir = os.path.abspath(os.path.dirname(__file__))
    name = f"{CodeAbilityTestSuite.__name__}_schema.json"
    schemafile = os.path.join(dir, "../output", name)
    with open(schemafile, "w") as file:
        file.write(pretty)


def get_test_schema():
    schema = CodeAbilitySpecification.model_json_schema()
    pretty = json.dumps(schema, indent=2)
    print(pretty)

    dir = os.path.abspath(os.path.dirname(__file__))
    name = f"{CodeAbilitySpecification.__name__}_schema.json"
    schemafile = os.path.join(dir, "../output", name)
    with open(schemafile, "w") as file:
        file.write(pretty)


#if this file is called directly, print json schema and save to file
if __name__ == "__main__":
    get_spec_schema()
    get_test_schema()
