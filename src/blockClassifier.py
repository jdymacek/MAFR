import MAFR
import argparse
import numpy as np
import os
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

allFiles = [allFiles[0]]





confusion = { x : {y: 0 for y in tstClasses} for x in tstClasses }

for f in allFiles:
	img = MAFR.loadImage(f, 16)
	mat = MAFR.imageToMatrix(img, 16)
	W = model.transform(mat)

	hits = {k : 0 for k in tstClasses}
	

	for block in W:
		percents = {k : 0 for k in tstClasses}
		idx = np.argmax(block)
		hits[annotation[idx]] += 1
		
		block = block/ np.sum(block)
		for i in range(0,len(annotation)):
			percents[annotation[i]] += block[i]
		ss = [(x,y) for y,x in percents.items()]
		ss.sort(reverse=True)
		print(ss)


	predicted = max(hits, key=hits.get)
	confusion[predicted][ os.path.basename(os.path.dirname(f))] += 1
	print(f)

print(confusion)

