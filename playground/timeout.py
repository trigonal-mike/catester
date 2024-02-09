import platform
if platform.system() == "Windows":
    #todo: check for UNIX based os, for using signal 
    from stopit import ThreadingTimeout as Timeout, threading_timeoutable as timeoutable
else:
    from stopit import SignalTimeout as Timeout, signal_timeoutable as timeoutable

print(f"PLATFORM: {platform.system()}")

import time

@timeoutable()
def long_running(sleep_duration):
    for i in range(30):
        print(f"{i}", end=" ", flush=True)
        time.sleep(sleep_duration)
    return "something"

start = time.time()
result = long_running(sleep_duration=0.01, timeout=1)
end = time.time()
print(f"\nresult 1: {result} in {end-start}s")

start = time.time()
result = long_running(sleep_duration=0.1, timeout=1)
end = time.time()
print(f"\nresult 2: {result} in {end-start}s")

start = time.time()
result = long_running(sleep_duration=10, timeout=1)
end = time.time()
print(f"\nresult 3: {result} in {end-start}s")
