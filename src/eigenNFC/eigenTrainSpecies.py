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
tstClasses = MAFR.getClasses(tstDirectory)
ml = []
labels = []

for species in tstClasses:
    speciesModel = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=30000, solver="mu")
    speciesFiles = [x[0] + "/" + y for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and os.path.basename(x[0]) == species]
    print(species)
    print(speciesFiles[:5])
"""
for f in allFiles:
    labels.append(f.split("/")[-2])
    arr = eigenNFC.imageToVector(f, x=(256-WIDTH)//2, y=0, width=WIDTH, height=HEIGHT)
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
"""

h = model.components_
print(f"ESTIMATED ERROR 1: {model.reconstruction_err_}")
print(f"ITERATIONS: {model.n_iter_}")
print(f"TIME TO FIND PATTERNS: {time.time() - t0}")

MAFR.saveMatrix(h, PATTERNS, WIDTH, HEIGHT) 

