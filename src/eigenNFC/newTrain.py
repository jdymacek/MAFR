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


allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]
random.shuffle(allFiles)
#allFiles.sort()

ml = []
for f in allFiles:
    ml += [[eigenNFC.imageToVector(f, x=(256-WIDTH)//2, y=0, width=WIDTH, height=HEIGHT)]]

M = np.concatenate(ml)

model = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=30000, solver="mu")
w = model.fit_transform(M)
h = model.components_

e = M - (np.matmul(w, h))
errors = [np.linalg.norm(row) for row in e]
average = statistics.mean(errors)
stdev = statistics.stdev(errors)
print(f"AVERAGE: {average}\tSTDEV: {stdev}")

oldLen = len(w)
toKeep = [x < (average + 0.5*stdev) for x in errors]

#w = w[toKeep]
#print(oldLen - len(w))
#allFiles = list(itertools.compress(allFiles, toKeep))

"""
ml = []
for f in allFiles:
    ml += [[eigenNFC.imageToVector(f, x=(256-WIDTH)//2, y=0, width=WIDTH, height=HEIGHT)]]

M = np.concatenate(ml)
w = model.fit_transform(M)
h = model.components_
"""

labels = [f.split("/")[-2] for f in allFiles]

MAFR.saveMatrix(h, PATTERNS, WIDTH, HEIGHT) 
filename = f"NEW-{PATTERNS}+{WIDTH}+{HEIGHT}.csv"
out = open(filename, "w")
for index, row in enumerate(w):
    line = labels[index]
    for val in row:
        line += "," + str(np.round(val, decimals=7))
    out.write(line + "\n")


