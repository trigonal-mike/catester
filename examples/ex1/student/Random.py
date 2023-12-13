import os
import random
import time


var1 = random.randint(1, 100)
var2 = random.random()

# failing, because of different seed!
random.seed()
var3 = random.randint(1, 100)

var4 = os.getcwd()

time.sleep(1.5)
var5 = time.time()
