import MAFR
import argparse
import numpy as np
import os
import json
import statistics
import random
import csv
from sklearn import decomposition
from scipy.stats import norm



parser = argparse.ArgumentParser("Use Classifier for NFC Classification")
parser.add_argument("-p", help="path to combined .nmf file", required=True)
parser.add_argument("-t", help="testing directory", required=True)
parser.add_argument("-a", help="annotation file", required=True)

args = parser.parse_args()

patternFile = args.p
tstDirectory = args.t
annotationFile = args.a

annotationDict = {}
lines = []
with open(annotationFile) as data:
    for line in csv.reader(data,  delimiter="\t"):
        lines.append(line)

data.close()

for l in lines:
    key = l[0][5:]
#print(key)
    annotationDict[key] = []
    for i in range(1,len(l)):
        annotationDict[key].append(l[i])

#tstClasses   = next(os.walk(tstDirectory))[1]
#tstClasses += ["JUNK"]
tstClasses = MAFR.getClasses(tstDirectory)
tstClasses = sorted(tstClasses)

allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png")]
samples = random.sample(allFiles, 8)
#samples = allFiles
blockSize = MAFR.getBlocksize(patternFile)

img = MAFR.loadImage(allFiles[0], blockSize)
m = MAFR.imageToMatrix(img, blockSize)

patterns, annotation = MAFR.loadMatrix(patternFile)

model = decomposition.NMF(n_components=len(patterns), init="random", random_state=0, max_iter=10000, solver="mu")
model.fit(m)
model.components_ = patterns

confusion = { x : {y: 0 for y in tstClasses} for x in tstClasses }


counter = 0
for f in samples:
    slashIndex = f.rfind("/") + 1
    fileName = f[slashIndex:]
    if fileName not in  annotationDict:
        counter += 1
print(counter)
#quit()
for f in samples:
    img = MAFR.loadImage(f, 16)
    mat = MAFR.imageToMatrix(img, 16)
    W = model.transform(mat)
    slashIndex = f.rfind("/") + 1
    fileName = f[slashIndex:]

    correct = os.path.basename(os.path.dirname(f))

    headers = ""
    for c in tstClasses:
        headers = headers + c + "\t"
    headers += "class"

    outName = fileName[:-3] + "csv"
    with open(outName, "w") as out:
        out.write(headers + "\n")

        for index, block in enumerate(W):
            percents = {k : 0 for k in tstClasses}
            block = block/ np.sum(block)
            line = ""
            for i in range(0,len(annotation)):
                percents[annotation[i]] += block[i]
            for v in percents.values():
                line += str(v) + "\t"
            if str(index) in annotationDict[fileName]:
                line += correct
            else:
                line += "JUNK"
            if percents["JUNK"] < 0.166:
                out.write(line + "\n")


    out.close()
