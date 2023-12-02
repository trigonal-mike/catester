x1 = "Hello World" #str
x2 = 20 #int
x3 = 20.5 #float
x4 = 1j #complex
x5 = ["apple", "banana", "cherry"] #list
x6 = ("apple", "banana", "cherry") #tuple
x7 = range(6) #range
x8 = {"name" : "John", "age" : 36} #dict
x9 = {"apple", "banana", "cherry"} #set
x10 = frozenset({"apple", "banana", "cherry"}) #frozenset
x11 = True #bool
x12 = b"Hello" #bytes
x13 = bytearray(5) #bytearray
x14 = memoryview(bytes(5)) #memoryview
x15 = None #NoneType

for i in range(1, 15):
  globals()[f"y{i}"] = globals()[f"x{i}"]

#quick check which type is instance of another type
for i in range(1, 15):
  x = globals()[f"x{i}"]
  type_x = type(x)
  for j in range(1, 15):
    y = globals()[f"y{j}"]
    type_y = type(y)
    if isinstance(x, type_y) and type_x != type_y:
      print(f"{x} isinstance of {type_y}")

#True isinstance of <class 'int'>
