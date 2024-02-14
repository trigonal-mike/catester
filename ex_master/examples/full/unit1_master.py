"""This is the doc-string ..."""
import os


class file_reader:
    def readfile(self, filename):
        with open(filename, "r") as file:
            return file.read()


dir = os.path.dirname(__file__)
filename = os.path.abspath(os.path.join(dir, "./data/dat.txt"))
# todo: test errors/warnings
_file_reader = file_reader()
var1 = _file_reader.readfile(filename)
var2 = 2
print(var1)
pass

#$META version 2.3.7
#$META type ProblemSet
#$META title "my title"
#$META description my description
#$META language de
#$META license MIT
#$META authors {"name":"name", "email":"email", "affiliation":"affiliation"}
#$META authors {"name":"name", "email":"email", "affiliation":"affiliation"}
#$META authors {"name":"name", "email":"email", "affiliation":"affiliation"}
#$META maintainers {"name":"name", "email":"email", "affiliation":"affiliation"}
#$META maintainers {"name":"name", "email":"email", "affiliation":"affiliation"}
#$META maintainers {"name":"name", "email":"email", "affiliation":"affiliation"}
#$META links {"description":"ddd 1", "url":"url 1"}
#$META links {"description":"ddd 2", "url":"url 2"}
#$META supportingMaterial {"description":"support", "url":"support url"}
#$META supportingMaterial {"description":"support", "url":"support url"}
#$META keywords ["python", "testing"]
#$META keywords "intermediate"
#$META keywords "programming"

#$META studentSubmissionFiles ./types.py
#$META studentSubmissionFiles ./graphics.py
#$META additionalFiles ./data
#$META additionalFiles ./graphics.dat
#$META testFiles ./testfiles
#$META studentTemplates ./templates

#$TESTSUITE version 1.1
#$TESTSUITE name "my testssuite name"
#$TESTSUITE description my description

#$EXISTANCETEST existance 1
#$PROPERTY id "unit1"
#$PROPERTY file "unit1.py"
#$TESTVAR -

#$EXISTANCETEST existance 2
#$PROPERTY id "types"
#$PROPERTY file "types.py"
#$TESTVAR -

#$EXISTANCETEST existance 3
#$PROPERTY id "graphics"
#$PROPERTY file "graphics.py"
#$TESTVAR -

#$LINTINGTEST linting 1
#$PROPERTY successDependency "unit1"
#$PROPERTY file "unit1.py"
#$TESTVAR -
#$PROPERTY pattern "W"

#$LINTINGTEST linting 2
#$PROPERTY successDependency "types"
#$PROPERTY file "types.py"
#$TESTVAR -

#$LINTINGTEST linting 3
#$PROPERTY successDependency "graphics"
#$PROPERTY file "graphics.py"
#$TESTVAR -
#$PROPERTY pattern "E741"

#$STRUCTURALTEST structural 1
#$PROPERTY successDependency "unit1"
#$PROPERTY file "unit1.py"
#$TESTVAR class
#$PROPERTY allowedOccuranceRange [1,1]
#$TESTVAR pass
#$PROPERTY allowedOccuranceRange [1,1]

#$VARIABLETEST variables unit1
#$PROPERTY successDependency "unit1"
#$TESTVAR __doc__
#$PROPERTY qualification startsWith
#$PROPERTY pattern This is the doc-string

#$VARIABLETEST variables types
#$PROPERTY successDependency "types"
#$PROPERTY entryPoint "types.py"
#$TESTVAR x1
#$TESTVAR x2
#$TESTVAR x3
#$TESTVAR x4
#$TESTVAR x5
#$TESTVAR x6
#$TESTVAR x7
#$TESTVAR x8
#$TESTVAR x9
#$TESTVAR x10
#$TESTVAR x11
#$TESTVAR x12
#$TESTVAR x13
#$TESTVAR x14
#$TESTVAR x15

#$GRAPHICSTEST matplot figures
#$PROPERTY successDependency "graphics"
#$PROPERTY storeGraphicsArtifacts false
#$PROPERTY entryPoint "graphics.py"
#$TESTVAR figure(1).axes[0].lines[0]._linestyle
#$TESTVAR figure(1).axes[0].lines[0].get_linestyle()
#$TESTVAR figure(1).axes[0].get_xlabel()
#$PROPERTY qualification startsWith
#$PROPERTY pattern "x"
#$TESTVAR figure(2).axes[0].get_ylabel()
#$PROPERTY value "y"

#$VARIABLETEST test setup code
#$PROPERTY setUpCode ["x=3", "y=1"]
#$PROPERTY setUpCode "x=3\ny=1"
#$PROPERTY setUpCode "x=3"
#$PROPERTY setUpCode "y=1"
#$TESTVAR var2
#$PROPERTY evalString x-y
