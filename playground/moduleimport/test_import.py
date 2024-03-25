import importlib

def is_module(x):
    return str(type(x)) == "<class 'module'>"

def show_deps(mod, recursive=False):
    for name in dir(mod):
        val = getattr(mod, name)
        if is_module(val):
            if val.__name__ not in mlist:
                mlist.append(val.__name__)
                if recursive:
                    show_deps(val, True)

module_name = "add1"
y = importlib.import_module(module_name)

recursive = False
#recursive = True

mlist: list[str] = []
show_deps(y, recursive)
mlist.sort()
for x in mlist:
    print(x)
print(f"{len(mlist)} Modules found")
