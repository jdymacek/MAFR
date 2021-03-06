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
labels = []
patterns = []

fileList = []
for f in allFiles:
    arr = eigenNFC.imageToVector(f, x=(256-WIDTH)//2, y=0, width=WIDTH, height=HEIGHT)
    fileList += [[arr]]

fileMatrix = np.concatenate(fileList)

for species in tstClasses:
    speciesModel = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=30000, solver="mu")
    speciesFiles = [x[0] + "/" + y for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and os.path.basename(x[0]) == species]

    ml = []
    for f in speciesFiles:
        labels.append(f.split("/")[-2] + "/" + f.split("/")[-1])
        arr = eigenNFC.imageToVector(f, x=(256-WIDTH)//2, y=0, width=WIDTH, height=HEIGHT)
        ml += [[arr]]
    M = np.concatenate(ml)

    W = speciesModel.fit_transform(M)
    print(f"{species}: {speciesModel.reconstruction_err_}")
    patterns += [speciesModel.components_]

bigPattern = np.concatenate(patterns)
print(bigPattern.shape)

MAFR.saveMatrix(bigPattern, len(tstClasses) * PATTERNS, WIDTH, HEIGHT)

model = decomposition.NMF(n_components=len(bigPattern), init="random", random_state=0, max_iter=30000, solver="mu")
ones = [np.ones(WIDTH*HEIGHT)]
temp = model.fit_transform(fileMatrix)
model.components_ = bigPattern
coefficients = model.transform(fileMatrix)
print(f"ERROR: {model.reconstruction_err_}")

filename = str(len(tstClasses) * PATTERNS) + "+" + str(WIDTH) + "+" + str(HEIGHT) + ".csv"
out = open(filename, "w")
for index, row in enumerate(coefficients):
    line = labels[index]
    for val in row:
        line += "," + str(np.round(val, decimals=7))
    out.write(line + "\n")
