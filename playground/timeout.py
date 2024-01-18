import sys
import threading
from time import sleep
import _thread as thread

def quit_function(fn_name):
    print('{0} took too long'.format(fn_name), file=sys.stderr)
    sys.stderr.flush()
    thread.interrupt_main()

def exit_after(s):
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer

@exit_after(5)
def countdown(n):
    print('countdown started', flush=True)
    for i in range(n, -1, -1):
        print(i, end=', ', flush=True)
        sleep(1)
    print('countdown finished')

@exit_after(5)
def countdown1():
    print('countdown started', flush=True)
    sleep(10)
    #f.e. sleep function does not get interrupted!
    print('countdown finished')

countdown1()

