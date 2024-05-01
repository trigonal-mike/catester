import os
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
def execute_timeoutable(code, filename, namespace):
    execute_code(code, filename, namespace)
    return 0

def execute_file(directory, entry_point, namespace, timeout):
    isUnix = hasattr(os, "chroot")
    if isUnix:
        real_root = os.open("/", os.O_RDONLY)
        os.chroot(directory)
    try:
        with open(entry_point, "r") as file:
            result = execute_timeoutable(file.read(), entry_point, namespace, timeout=timeout)
    finally:
        if isUnix:
            os.fchdir(real_root)
            os.chroot(".")
            os.close(real_root)

    if result is None:
        return None
    return 0
