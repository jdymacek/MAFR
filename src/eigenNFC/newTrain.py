import MAFR
import eigenNFC
import numpy as np
import PIL
from PIL import Image
import argparse
import os
from sklearn import decomposition
import time
import random
import statistics
import itertools


parser = argparse.ArgumentParser(description='Convert an image to a vector')
parser.add_argument('-t', help='training directory')
parser.add_argument('-p', help = 'number of patterns')
parser.add_argument('-r', help = 'clip r pixels from bottom of images')
parser.add_argument('-w', help = 'width')

args = parser.parse_args()

tstDirectory = args.t
PATTERNS = int(args.p)
HEIGHT = 256 - int(args.r)
WIDTH = int(args.w)

"""
dirs = os.listdir(tstDirectory)
dirs  = [x for x in dirs if len(x) == 4]
print(dirs)
allFiles = [tstDirectory + "/" + 
"""

#allFiles = [os.path.basename(x[0])  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png")]
allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]
allFiles.sort()
#print(allFiles)

ml = []
labels = []
for f in allFiles:
    labels.append(f.split("/")[-2])
    arr = eigenNFC.imageToVector(f, x=(256-WIDTH)//2, y=0, width=WIDTH, height=HEIGHT)
    ml += [[arr]]

M = np.concatenate(ml)

model = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=30000, solver="mu")
w = model.fit_transform(M)


h = model.components_

e = M - (np.matmul(w, h))
errors = [np.linalg.norm(row) for row in e]
average = statistics.mean(errors)
stdev = statistics.stdev(errors)

w = w[[x < (average + stdev) for x in errors]]
labels = list(itertools.compress(labels, [x < (average + stdev) for x in errors]))
"""
#allFiles = list(itertools.compress(allFiles, [x < (average + 2*stdev) for x in errors]))
#random.shuffle(allFiles)
#allFiles = allFiles[:615]
allFiles.sort()
print(len(allFiles))

del(model)
del(w)
del(h)
del(M)
"""
"""
ml2 = []
labels2 = []
for f in allFiles:
    labels2.append(f.split("/")[-2])
    arr2 = eigenNFC.imageToVector(f, x=(256-WIDTH)//2, y=0, width=WIDTH, height=HEIGHT)
    ml2 += [[arr2]]

print(f"LABELS2: {len(labels2)}")
M2 = np.concatenate(ml2)
print(M2.shape)

t0 = time.time()
model2 = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=30000, solver="mu")
w2 = model2.fit_transform(M2)
print(f"W2: {w2.shape}")
print(f"ERROR: {model.reconstruction_err_}")

h2 = model2.components_
"""
MAFR.saveMatrix(h, PATTERNS, WIDTH, HEIGHT) 
filename = f"NEW-{PATTERNS}+{WIDTH}+{HEIGHT}.csv"
out = open(filename, "w")
for index, row in enumerate(w):
    line = labels[index]
    for val in row:
        line += "," + str(np.round(val, decimals=7))
    out.write(line + "\n")


