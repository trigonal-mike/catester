from enum import Enum
from model.model import TypeEnum

class TokenEnum(str, Enum):
    META = "META"
    TESTSUITE = "TESTSUITE"
    PROPERTY = "PROPERTY"
    VARIABLETEST = "VARIABLETEST"
    GRAPHICSTEST = "GRAPHICSTEST"
    EXISTANCETEST = "EXISTANCETEST"
    LINTINGTEST = "LINTINGTEST"
    STRUCTURALTEST = "STRUCTURALTEST"
    ERRORTEST = "ERRORTEST"
    HELPTEST = "HELPTEST"
    WARNINGTEST = "WARNINGTEST"
    STDOUTTEST = "STDOUTTEST"
    TESTVAR = "TESTVAR"

ARGUMENT_VALUE_TOKENS = (
    TokenEnum.META,
    TokenEnum.TESTSUITE,
    TokenEnum.PROPERTY,
)

TEST_MAPPING = {
    TokenEnum.VARIABLETEST: TypeEnum.variable.name,
    TokenEnum.GRAPHICSTEST: TypeEnum.graphics.name,
    TokenEnum.EXISTANCETEST: TypeEnum.exist.name,
    TokenEnum.LINTINGTEST: TypeEnum.linting.name,
    TokenEnum.STRUCTURALTEST: TypeEnum.structural.name,
    TokenEnum.ERRORTEST: TypeEnum.error.name,
    TokenEnum.HELPTEST: TypeEnum.help.name,
    TokenEnum.WARNINGTEST: TypeEnum.warning.name,
    TokenEnum.STDOUTTEST: TypeEnum.stdout.name,
}

class LOCAL_TEST_DIRECTORIES(str, Enum):
    _reference = "_reference"
    _correctSolution = "_correctSolution"
    _emptySolution = "_emptySolution"

VALID_PROPS_META = [
    "version",
    "type",
    "title",
    "description",
    "authors",
    "maintainers",
    "links",
    "supportingMaterial",
    "language",
    "keywords",
    "license",
    #in properties
    "studentSubmissionFiles",
    "additionalFiles",
    "testFiles",
    "studentTemplates",
]

VALID_PROPS_TESTSUITE = [
    "type",
    "name",
    "description",
    "version",
]

VALID_PROPS_TEST_COMMON = [
    "failureMessage",
    "successMessage",
    "qualification",
    "relativeTolerance",
    "absoluteTolerance",
    "allowedOccuranceRange",
    "occuranceType",
    "verbosity",
]

VALID_PROPS_TESTCOLLECTION_COMMON = [
    *VALID_PROPS_TEST_COMMON,
    "storeGraphicsArtifacts",
    "competency",
    "timeout",
]

VALID_PROPS_TEST = [
    *VALID_PROPS_TEST_COMMON,
    "name",
    "value",
    "evalString",
    "pattern",
    "countRequirement",
]

VALID_PROPS_TESTCOLLECTION = [
    *VALID_PROPS_TESTCOLLECTION_COMMON,
    "name",
    "type",
    "description",
    "successDependency",
    "setUpCodeDependency",
    "entryPoint",
    "inputAnswers",
    "setUpCode",
    "tearDownCode",
    "id",
    "file",
]
