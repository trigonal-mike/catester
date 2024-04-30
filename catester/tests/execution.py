import types
import platform

if platform.system() == "Windows":
    #todo: check for UNIX based os, for using signal 
    from stopit import ThreadingTimeout as Timeout, threading_timeoutable as timeoutable
else:
    from stopit import SignalTimeout as Timeout, signal_timeoutable as timeoutable

def execute_code(code, filename, namespace):
    exec(compile(code, filename, "exec"), namespace)

def execute_code_list(code_list, namespace):
    for code in code_list:
        execute_code(code, "", namespace)

@timeoutable()
def execute_file(file, filename, namespace):
    execute_code(file.read(), filename, namespace)
    return 0

def get_imported_modules(namespace):
    mlist: list[str] = []
    for name, val in namespace.items():
        if isinstance(val, types.ModuleType):
            mlist.append(val.__name__)
    return mlist
