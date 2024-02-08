import json
import os
import yaml

dir = os.path.dirname(__file__)
file = os.path.join(dir, "meta-default.yaml")

with open(file, "r") as stream:
    config = yaml.safe_load(stream)

x = json.dumps(config, indent=2)
print(x)
