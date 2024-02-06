from enum import Enum


class TokenEnum(str, Enum):
    TESTSUITE = "TESTSUITE"
    PROPERTY = "PROPERTY"
    TEST = "TEST"
    SUBTEST = "SUBTEST"
    VARIABLETEST = "VARIABLETEST"
    GRAPHICSTEST = "GRAPHICSTEST"
    TESTVAR = "TESTVAR"


class SubTestEnum(str, Enum):
    name = "name"
    value = "value"
    evalString = "evalString"
    pattern = "pattern"
    countRequirement = "countRequirement"
    # common:
    failureMessage = "failureMessage"
    successMessage = "successMessage"
    qualification = "qualification"
    relativeTolerance = "relativeTolerance"
    absoluteTolerance = "absoluteTolerance"
    allowedOccuranceRange = "allowedOccuranceRange"
    verbosity = "verbosity"


class TestEnum(str, Enum):
    name = "name"
    type = "type"
    description = "description"
    successDependency = "successDependency"
    setUpCodeDependency = "setUpCodeDependency"
    entryPoint = "entryPoint"
    setUpCode = "setUpCode"
    tearDownCode = "tearDownCode"
    id = "id"
    file = "file"
    # common:
    failureMessage = "failureMessage"
    successMessage = "successMessage"
    qualification = "qualification"
    relativeTolerance = "relativeTolerance"
    absoluteTolerance = "absoluteTolerance"
    allowedOccuranceRange = "allowedOccuranceRange"
    verbosity = "verbosity"
    ## common:
    storeGraphicsArtifacts = "storeGraphicsArtifacts"
    competency = "competency"
    timeout = "timeout"


class PropertyEnum(str, Enum):
    # common:
    failureMessage = "failureMessage"
    successMessage = "successMessage"
    qualification = "qualification"
    relativeTolerance = "relativeTolerance"
    absoluteTolerance = "absoluteTolerance"
    allowedOccuranceRange = "allowedOccuranceRange"
    verbosity = "verbosity"
    ## common:
    storeGraphicsArtifacts = "storeGraphicsArtifacts"
    competency = "competency"
    timeout = "timeout"


class TestSuiteEnum(str, Enum):
    type = "type"
    name = "name"
    description = "description"
    version = "version"
