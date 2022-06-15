import MAFR
import argparse
import numpy as np
import os
import json
import statistics
from sklearn import decomposition
from scipy.stats import norm



parser = argparse.ArgumentParser("Use Classifier for NFC Classification")
parser.add_argument("-p", help="path to combined .nmf file", required=True)
parser.add_argument("-t", help="testing directory", required=True)

args = parser.parse_args()

patternFile = args.p

tstDirectory = args.t

tstClasses   = MAFR.getClasses(tstDirectory)
allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png")]
tstClasses += ["JUNK"]
blockSize = MAFR.getBlocksize(patternFile)

img = MAFR.loadImage(allFiles[0], blockSize)
m = MAFR.imageToMatrix(img, blockSize)

patterns, annotation = MAFR.loadMatrix(patternFile)


model = decomposition.NMF(n_components=len(patterns), init="random", random_state=0, max_iter=10000, solver="mu")
model.fit(m)
model.components_ = patterns

confusion = { x : {y: 0 for y in tstClasses} for x in tstClasses }

#allFiles = ["/scratch/prism2022data/testing_inverse/COYE/unit04-20151001231702_017729712_06786_inverse.png"]


for f in allFiles:
    img = MAFR.loadImage(f, 16)
    mat = MAFR.imageToMatrix(img, 16)
    W = model.transform(mat)

    best = (0, "JUNK")
    for block in W:
        percents = {k : 0 for k in tstClasses}
        block = block/ np.sum(block)

        for i in range(0,len(annotation)):
            percents[annotation[i]] += block[i]
        if percents["JUNK"] < 0.2 or (max(percents.values()) > 0.3):
            ss = [(x,y) for y,x in percents.items()]
            ss.sort(reverse=True)
            if ss[0][1] != "JUNK" and ss[0][0] > best[0]:
                best = ss[0]
			

        correct = os.path.basename(os.path.dirname(f))


    confusion[best[1]][correct] += 1
    print(f)
    print(best)


print(confusion)

