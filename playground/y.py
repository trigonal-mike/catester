x = 1

def r():
    print(globals()["x"])
    globals()["x"] = 2
    def xx():
        print(globals()["x"])
        pass
    globals()["xx"] = xx

r()
print(globals()["x"])
print(xx)
xx()

