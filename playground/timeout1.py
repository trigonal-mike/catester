import time
from itertools import count
from multiprocessing import Process

counter = count(0)

def inc_forever():
    print('Starting function inc_forever()...')
    while True:
        time.sleep(0.01)
        print(next(counter))

if __name__ == '__main__':
    # counter is an infinite iterator
    p1 = Process(target=inc_forever, name='Process_inc_forever')
    p1.start()
    p1.join(timeout=1)
    p1.terminate()
    print(p1.exitcode)
    if p1.exitcode is None:
        print(f'Oops, {p1} timeouts!')
