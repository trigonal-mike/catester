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
    stdout = "stdout"

class LanguageEnum(str, Enum):
    de = "de"
    en = "en"

class MetaTypeEnum(str, Enum):
    ProblemSet = "ProblemSet"

class StatusEnum(str, Enum):
    scheduled = "SCHEDULED"
    completed = "COMPLETED"
    timedout = "TIMEDOUT"
    crashed = "CRASHED"
    cancelled = "CANCELLED"
    skipped = "SKIPPED"
    failed = "FAILED"
    # following not used yet:
    #pending = "PENDING"
    #running = "RUNNING"

class ResultEnum(str, Enum):
    passed = "PASSED"
    failed = "FAILED"
    skipped = "SKIPPED"

VERSION_REGEX = "^([1-9]\d*|0)(\.(([1-9]\d*)|0)){0,3}$"
#todo:
#url + email regex

DEFAULTS = {
    "specification": {
        "executionDirectory": None,
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
        "allowedOccuranceRange": [0, 0],
        "occuranceType": "NAME",
    },
    "meta": {
        "version": "1.0",
        "type": MetaTypeEnum.ProblemSet,
        "title": "TITLE",
        "description": "DESCRIPTION",
        "language": LanguageEnum.en,
        "license": "Not specified",
    },
    "person": {
        "name": "unknown",
        "email": "unknown@tugraz.at",
        "affiliation": "TU Graz",
    },
}

class CodeAbilityBase(BaseModel):
    #todo:
    #check if coerce_numbers_to_str=True is a problem somewhere???
    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        validate_assignment=True,
        coerce_numbers_to_str=True
    )

class CodeAbilityTestCommon(BaseModel):
    failureMessage: Optional[str] = Field(min_length=1, default=None)
    successMessage: Optional[str] = Field(min_length=1, default=None)
    qualification: Optional[QualificationEnum] = Field(default=None, validate_default=True)
    relativeTolerance: Optional[float] = Field(gt=0, default=None)
    absoluteTolerance: Optional[float] = Field(ge=0, default=None)
    allowedOccuranceRange: Optional[List[int]] = Field(min_length=2, max_length=2, default=None)
    occuranceType: Optional[str] = Field(min_length=1, default=None)
    verbosity: Optional[int] = Field(ge=0, le=3, default=None)

class CodeAbilityTestCollectionCommon(CodeAbilityTestCommon):
    storeGraphicsArtifacts: Optional[bool] = Field(default=None)
    competency: Optional[str] = Field(min_length=1, default=None)
    timeout: Optional[float] = Field(ge=0, default=None)

class CodeAbilityTest(CodeAbilityBase, CodeAbilityTestCommon):
    name: str = Field(min_length=1)
    value: Optional[Any] = Field(default=None)
    evalString: Optional[str] = Field(min_length=1, default=None)
    pattern: Optional[str] = Field(min_length=1, default=None)
    countRequirement: Optional[int] = Field(ge=0, default=None)

class CodeAbilityTestCollection(CodeAbilityBase, CodeAbilityTestCollectionCommon):
    type: Optional[TypeEnum] = Field(default=TypeEnum.variable, validate_default=True)
    name: str = Field(min_length=1)
    description: Optional[str] = Field(min_length=1, default=None)
    successDependency: Optional[str | int | List[str | int]] = Field(default=None)
    setUpCodeDependency: Optional[str] = Field(min_length=1, default=None)
    entryPoint: Optional[str] = Field(min_length=1, default=None)
    inputAnswers: Optional[str | List[str]] = Field(default=None)
    setUpCode: Optional[str | List[str]] = Field(default=None)
    tearDownCode: Optional[str | List[str]] = Field(default=None)
    id: Optional[str] = Field(min_length=1, default=None)
    file: Optional[str] = Field(min_length=1, default=None)
    tests: List[CodeAbilityTest]

class CodeAbilityTestProperty(CodeAbilityBase, CodeAbilityTestCollectionCommon):
    qualification: Optional[QualificationEnum] = Field(default=DEFAULTS["properties"]["qualification"], validate_default=True)
    failureMessage: Optional[str] = Field(min_length=1, default=DEFAULTS["properties"]["failureMessage"])
    successMessage: Optional[str] = Field(min_length=1, default=DEFAULTS["properties"]["successMessage"])
    relativeTolerance: Optional[float] = Field(gt=0, default=DEFAULTS["properties"]["relativeTolerance"])
    absoluteTolerance: Optional[float] = Field(ge=0, default=DEFAULTS["properties"]["absoluteTolerance"])
    allowedOccuranceRange: Optional[List[int]] = Field(min_length=2, max_length=2, default=DEFAULTS["properties"]["allowedOccuranceRange"])
    occuranceType: Optional[str] = Field(min_length=1, default=DEFAULTS["properties"]["occuranceType"])
    timeout: Optional[float] = Field(ge=0, default=DEFAULTS["properties"]["timeout"])
    tests: List[CodeAbilityTestCollection] = Field(default=[])

class CodeAbilityTestSuite(CodeAbilityBase):
    type: Optional[str] = Field(min_length=1, default=DEFAULTS["testsuite"]["type"])
    name: Optional[str] = Field(min_length=1, default=DEFAULTS["testsuite"]["name"])
    description: Optional[str] = Field(min_length=1, default=DEFAULTS["testsuite"]["description"])
    version: Optional[str] = Field(pattern=VERSION_REGEX, default=DEFAULTS["testsuite"]["version"])
    properties: CodeAbilityTestProperty = Field(default=CodeAbilityTestProperty())

class CodeAbilitySpecification(CodeAbilityBase):
    executionDirectory: Optional[str] = Field(min_length=1, default=DEFAULTS["specification"]["executionDirectory"])
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

class CodeAbilityLink(CodeAbilityBase):
    description: str = Field(min_length=1)
    url: str = Field(min_length=1)

class CodeAbilityPerson(CodeAbilityBase):
    name: Optional[str] = Field(min_length=1, default=None)
    email: Optional[str] = Field(min_length=1, default=None)
    affiliation: Optional[str] = Field(min_length=1, default=None)

class CodeAbilityMetaProperty(CodeAbilityBase):
    studentSubmissionFiles: Optional[List[str]] = Field(default=[])
    additionalFiles: Optional[List[str]] = Field(default=[])
    testFiles: Optional[List[str]] = Field(default=[])
    studentTemplates: Optional[List[str]] = Field(default=[])

class CodeAbilityMeta(CodeAbilityBase):
    version: Optional[str] = Field(pattern=VERSION_REGEX, default=DEFAULTS["meta"]["version"])
    type: Optional[MetaTypeEnum] = Field(default=DEFAULTS["meta"]["type"], validate_default=True)
    title: Optional[str] = Field(min_length=1, default=DEFAULTS["meta"]["title"])
    description: Optional[str] = Field(min_length=1, default=DEFAULTS["meta"]["description"])
    language: Optional[LanguageEnum] = Field(default=DEFAULTS["meta"]["language"], validate_default=True)
    license: Optional[str] = Field(min_length=1, default=DEFAULTS["meta"]["license"])
    authors: Optional[List[CodeAbilityPerson]] = Field(default=[])
    maintainers: Optional[List[CodeAbilityPerson]] = Field(default=[])
    links: Optional[List[CodeAbilityLink]] = Field(default=[])
    supportingMaterial: Optional[List[CodeAbilityLink]] = Field(default=[])
    keywords: Optional[List[str]] = Field(default=[])
    properties: Optional[CodeAbilityMetaProperty] = Field(default=CodeAbilityMetaProperty())

class CodeAbilityReportSummary(CodeAbilityBase):
    total: int = Field(ge=0, default=0)
    #todo: success or succeeded?
    success: int = Field(ge=0, default=0)
    failed: int = Field(ge=0, default=0)
    skipped: int = Field(ge=0, default=0)

class CodeAbilityReportProperties(CodeAbilityBase):
    #todo: timestamp or timeStamp?
    timestamp: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    version: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    status: Optional[StatusEnum] = Field(default=None, validate_default=True)
    result: Optional[ResultEnum] = Field(default=None, validate_default=True)
    summary: Optional[CodeAbilityReportSummary] = Field(default=None)
    statusMessage: Optional[str] = Field(default=None)
    resultMessage: Optional[str] = Field(default=None)
    details: Optional[str] = Field(default=None)
    setup: Optional[str] = Field(default=None)
    teardown: Optional[str] = Field(default=None)
    duration: Optional[float] = Field(ge=0, default=None)
    executionDuration: Optional[float] = Field(ge=0, default=None)
    environment: Optional[dict] = Field(default=None)
    properties: Optional[dict] = Field(default=None)
    debug: Optional[dict] = Field(default=None)

class CodeAbilityReportSub(CodeAbilityReportProperties):
    pass

class CodeAbilityReportMain(CodeAbilityReportProperties):
    tests: Optional[List[CodeAbilityReportSub]] = Field(default=None)

class CodeAbilityReport(CodeAbilityReportProperties):
    tests: Optional[List[CodeAbilityReportMain]] = Field(default=None)

def load_config(classname: BaseModel, file_path: str = None):
    config = {}
    if file_path is not None and len(file_path) > 0:
        with open(file_path, "r") as stream:
            config = yaml.safe_load(stream) or {}
    return classname(**config)

def parse_meta_file(file_path: str = None):
    return load_config(CodeAbilityMeta, file_path)

def parse_spec_file(file_path: str = None):
    return load_config(CodeAbilitySpecification, file_path)

def parse_test_file(file_path: str = None):
    return load_config(CodeAbilityTestSuite, file_path)

def parse_report_file(file_path: str = None):
    return load_config(CodeAbilityReport, file_path)

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
    get_schema(CodeAbilityMeta)
    get_schema(CodeAbilityReport)
