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

tstClasses   = next(os.walk(tstDirectory))[1]
allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png")]

blockSize = MAFR.getBlocksize(patternFile)

img = MAFR.loadImage(allFiles[0], blockSize)
m = MAFR.imageToMatrix(img, blockSize)

patterns, annotation = MAFR.loadMatrix(patternFile)


model = decomposition.NMF(n_components=len(patterns), init="random", random_state=0, max_iter=10000, solver="mu")
model.fit(m)
model.components_ = patterns

confusion = { x : {y: 0 for y in tstClasses} for x in tstClasses }

  
with open('pOfB.json') as f:
	pOfBFunctions = json.load(f)

with open('pOfBA.json') as f:
	pOfBAFunctions = json.load(f)

with open('pOfA.json') as f:
    pOfA = json.load(f)


#allFiles = ["/scratch/prism2022data/testing_inverse/COYE/unit04-20151001231702_017729712_06786_inverse.png"]


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

	correct = os.path.basename(os.path.dirname(f))

	#use bayes thm.
	probs = {x: 0 for x in tstClasses}

	for A in tstClasses:
		pOfBA = 1.0
		pOfB = 1.0
		for B in tstClasses:
			pOfBA *= norm.pdf(hits[B],loc=float(pOfBAFunctions[A][B][0]),scale=float(pOfBAFunctions[A][B][1]))
			pOfB  *= norm.pdf(hits[B],loc=float(pOfBFunctions[B][0]),scale=float(pOfBFunctions[B][1]))

		probs[A] = (pOfBA*float(pOfA[A]))/pOfB

	predicted = max(probs, key=probs.get)
	h = [(x,y) for y,x in probs.items()]
	h.sort(reverse=True)
	print(h)
	confusion[predicted][correct] += 1
	print(f)


print(confusion)

