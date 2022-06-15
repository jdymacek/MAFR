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

likelihood = {"AMRE": 0.107, "BBWA": 0.091, "BTBW": 0.132, "COYE": 0.226, "OVEN": 0.441, "JUNK": 0}
#allFiles = ["/scratch/prism2022data/testing_inverse/COYE/unit04-20151001231702_017729712_06786_inverse.png"]


for f in allFiles:
    img = MAFR.loadImage(f, 16)
    mat = MAFR.imageToMatrix(img, 16)
    blank = [0]*256
    for i in range(256):
      if not ((i-5)%16<6):
            mat[i] = blank

    W = model.transform(mat)

    hits = {k : likelihood[k] for k in tstClasses}

    for index, block in enumerate(W):
        if (index-5)%16 >=6:
            continue

        
        block = np.round_(block, decimals =10)
        val = np.sum(block)
        if val > 0:
            block = block/ val
        else:
            continue

        percents = {k : 0 for k in tstClasses}

        for i in range(0,len(annotation)):
            percents[annotation[i]] += block[i]
        if percents["JUNK"] < 0.166:
            ss = [(x,y) for y,x in percents.items()]
            ss.sort(reverse=True)
#if ss[0][1] != "JUNK":
            hits[ss[0][1]]+=1
    print(hits)		

    predicted = max(hits, key=hits.get)
    confusion[predicted][ os.path.basename(os.path.dirname(f))] += 1

       
    print(f)


print(confusion)

