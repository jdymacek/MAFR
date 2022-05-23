import time
import os

t0= time.time()
os.system("python3 patternMaker.py -d training -p 32 -b 16 -o patterns -s OVEN -n 4")
print("Time elapsed for first run: ", (time.time()-t0))

t1 = time.time()
os.system("python3 patternMaker.py -d training -p 32 -b 16 -o patterns -s OVEN -n 10")
print("Time elapsed for first run: ", (time.time()-t1))

t2 =  time.time()
os.system("python3 patternMaker.py -d training -p 64 -b 16 -o patterns -s OVEN -n 4")
print("Time elapsed for first run: ", (time.time()-t2))

t3 = time.time()
os.system("python3 patternMaker.py -d training -p 64 -b 16 -o patterns -s OVEN -n 10")
print("Time elapsed for first run: ", (time.time()-t3))

t4 = time.time()
os.system("python3 autoPattern.py -d training -p 64 -b 16 -o patterns -n 10 -s 4")

