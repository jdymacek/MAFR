import MAFR
import argparse
import numpy as np
import os
import json
import statistics
import random
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

tstClasses   = next(os.walk(tstDirectory))[1]
tstClasses += ["JUNK"]
tstClasses = sorted(tstClasses)

allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png")]
samples = random.choice(allFiles, 12)

blockSize = MAFR.getBlocksize(patternFile)

img = MAFR.loadImage(allFiles[0], blockSize)
m = MAFR.imageToMatrix(img, blockSize)

patterns, annotation = MAFR.loadMatrix(patternFile)

model = decomposition.NMF(n_components=len(patterns), init="random", random_state=0, max_iter=10000, solver="mu")
model.fit(m)
model.components_ = patterns

confusion = { x : {y: 0 for y in tstClasses} for x in tstClasses }


for f in samples:
	img = MAFR.loadImage(f, 16)
	mat = MAFR.imageToMatrix(img, 16)
	W = model.transform(mat)


    headers = ""
    for c in tstClasses:
        headers = headers + c + "\t"
    headers += "class"

    outName = f[:-3] + "csv"
    out = f.open(outName, "w")
    out.write(headers)

	for index, block in enumerate(W):
		percents = {k : 0 for k in tstClasses}
		
		block = block/ np.sum(block)
		for i in range(0,len(annotation)):
			percents[annotation[i]] += block[i]

        line = ""
        for v in percents.values():
            line += v + "\t"
        out.write(line)

    out.close()
	correct = os.path.basename(os.path.dirname(f))

