import pandas as pd

data = {
    'Column1': [1, 2, 3],
    'Column2': ['a', 'B', 'C'],
    'Column3': [True, False, True]
}

df = pd.DataFrame(data)
print(df)
print(type(df))

d = {'a': 1, 'b': 2, 'c': 3}
ser = pd.Series(data=d, index=['a', 'b', 'c'])
print(ser)
print(type(ser))


