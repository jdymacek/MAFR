import MAFR
import argparse
import numpy as np
import os
import statistics
import json
from sklearn import decomposition
np.set_printoptions(threshold=np.inf)

parser = argparse.ArgumentParser("Use Classifier for NFC Classification")
parser.add_argument("-p", help="path to combined .nmf file", required=True)
parser.add_argument("-t", help="testing directory", required=True)

args = parser.parse_args()

patternFile = args.p

tstDirectory = args.t

tstClasses   = next(os.walk(tstDirectory))[1]
allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png")]

blockSize = MAFR.getBlocksize(patternFile)

img = MAFR.loadImage(allFiles[0], blockSize)
m = MAFR.imageToMatrix(img, blockSize)

patterns, annotation = MAFR.loadMatrix(patternFile)


model = decomposition.NMF(n_components=len(patterns), init="random", random_state=0, max_iter=10000, solver="mu")
model.fit(m)
model.components_ = patterns

#allFiles = [allFiles[0]]



averageWinners = {x : (0,0) for x in tstClasses}


histogram = {x : {y: [] for y in tstClasses} for x in tstClasses}
classInfo = {x : 0 for x in tstClasses}

overall = {x : [] for x in tstClasses}
for f in allFiles:
	img = MAFR.loadImage(f, 16)
	mat = MAFR.imageToMatrix(img, 16)
	W = model.transform(mat)

	hits = {k : 0 for k in tstClasses}	

	for block in W:
		percents = {k : 0 for k in tstClasses+["JUNK"]}
		
		block = block/ np.sum(block)
		for i in range(0,len(annotation)):
			percents[annotation[i]] += block[i]
		ss = [(x,y) for y,x in percents.items()]
		ss.sort(reverse=True)
		if ss[0][1] != "JUNK":
			hits[ss[0][1]] += 1

	print(hits)
	correct = os.path.basename(os.path.dirname(f))
	classInfo[correct] += 1
	print(correct)
	for c in tstClasses:
		histogram[correct][c] += [hits[c]]
		overall[c] += [hits[c]]


normals = {x : {y: [] for y in tstClasses} for x in tstClasses}
totals = {x:[] for x in tstClasses}
for x in tstClasses:
	for y in tstClasses:
		normals[x][y] = (statistics.mean(histogram[x][y]),statistics.stdev(histogram[x][y]))
	totals[x] = (statistics.mean(overall[x]),statistics.stdev(overall[x]))
	classInfo[x] /= len(allFiles)

print(totals)

with open("pOfA.json","w") as out:
    out.write(json.dumps(classInfo, sort_keys=True, indent=4))

with open("pOfB.json","w") as out:
	out.write(json.dumps(totals, sort_keys=True, indent=4))

with open("pOfBA.json","w") as outFile:
	outFile.write(json.dumps(normals, sort_keys=True, indent=4))
