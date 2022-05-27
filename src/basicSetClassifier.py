import MAFR
import random
import argparse
import numpy as np
import os
import time

parser = argparse.ArgumentParser(description='Faster Error Computation')
parser.add_argument('-t', '--training', help='Path to training images', required=True)
parser.add_argument('-d', '--directory', help='Path to .nmf files', required=True)

args = parser.parse_args()

directory = args.directory
trainingDir = args.training

patterns = [p for p in os.listdir(directory) if p.endswith(".nmf")]

dirs = os.listdir(trainingDir)
trainingFiles = []
for d in dirs:
	f = [d+ "/" + p for p in os.listdir(trainingDir + d) if p.endswith(".png")]
#	random.shuffle(f)
#	if len(f) > 64:
#		f = f[-64:]
	trainingFiles += f;


species = {}
#Error values for all files for all patterns
errorValues = {k:{} for k in trainingFiles}
t0 = time.time()
for pat in patterns:
	print(pat)
	mat = MAFR.loadMatrix(directory + pat)
	inv = np.linalg.pinv(mat)
	sps = MAFR.getSpecies(directory + pat)
	if sps not in species:
		species[sps] = [pat]	
	else:
		species[sps] += [pat]

	for imgFile in trainingFiles:
		img = MAFR.loadImage(trainingDir + imgFile, 16)
		org = MAFR.imageToMatrix(img, 16)
		#err = MAFR.quickError(org,mat,inv)
                #errorValues[imgFile][pat] = (err,sps)
print(f'Time to open files: {time.time() - t0}')

best = 0
for i in range(5000):
	classifier = [random.choice(species[k]) for k in species]
#	print(classifier)
	correct = 0
	for imgFile in trainingFiles:
		results = [errorValues[imgFile][s] for s in classifier]
		results.sort()
#		print(results)
		expect = imgFile.split("/")[0]
#		print(results[0][1] + "\t" + expect)
		if results[0][1] == expect:
			correct += 1

	if correct > best:
		best = correct
	print(str(correct) + "/" + str(len(trainingFiles)) + "\t" + str(correct/len(trainingFiles)))

print(str(best) + "/" + str(len(trainingFiles)) + "\t" + str(best/len(trainingFiles)))

