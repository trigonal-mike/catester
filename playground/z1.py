import os
import tokenize

dir = os.path.dirname(__file__)
file = os.path.join(dir, "Structural.py")

with open(file, 'rb') as f:
    tokens = tokenize.tokenize(f.readline)
    for token in tokens:
        print(f"{token.exact_type} -- {token}" )
