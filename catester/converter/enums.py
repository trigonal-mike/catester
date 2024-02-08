from enum import Enum

class TokenEnum(str, Enum):
    META = "META"
    ADDITIONALFILES = "ADDITIONALFILES"
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
    TESTVAR = "TESTVAR"

VALID_PROPS_META = [
    "version",
    "type",
    "title",
    "description",
    #"authors",
    #"maintainers",
    #"links",
    #"supportingMaterial",
    "language",
    #"keywords",
    "license",
    #"properties",
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
    "setUpCode",
    "tearDownCode",
    "id",
    "file",
]
