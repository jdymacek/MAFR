import MAFR
import eigenNFC
import numpy as np
import PIL
from PIL import Image
import argparse
import os
from sklearn import decomposition
import time
import argparse


parser = argparse.ArgumentParser(description='Convert an image to a vector')
parser.add_argument('-t', help='training directory')
parser.add_argument('-p', help = 'number of patterns')
parser.add_argument('-r', help = 'clip r pixels from bottom of images')

args = parser.parse_args()

tstDirectory = args.t
PATTERNS = int(args.p)
HEIGHT = 256 - int(args.r)


allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png")]

ml = []
labels = []
for f in allFiles:
    labels.append(f.split("/")[-2])
    arr = eigenNFC.imageToVector(f, x=72, y=0, width=96, height=HEIGHT)
    ml += [[arr]]

M = np.concatenate(ml)

t0 = time.time()
model = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=30000, solver="mu")
w = model.fit_transform(M)

out = open("test.csv", "w")
for index, row in enumerate(w):
    line = labels[index]
    for val in row:
        line += "," + str(np.round(val, decimals=7))
    out.write(line + "\n")

h = model.components_
print(f"ESTIMATED ERROR 1: {model.reconstruction_err_}")
print(f"ITERATIONS: {model.n_iter_}")
print(f"TIME TO FIND PATTERNS: {time.time() - t0}")

MAFR.saveMatrix(h, PATTERNS, 96, HEIGHT) 

