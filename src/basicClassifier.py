#!/usr/bin/python3

import MAFR
import argparse
import os

parser = argparse.ArgumentParser(description='Basic Classifier')
parser.add_argument('-d', help='directory of desired .nmf pattern files') #patterns
parser.add_argument('-t', help='directory of test directories') #file to be tested
parser.add_argument('-b', help='block size of tiles')

args = parser.parse_args()

srcDirectory = args.d
tstDirectory = args.t
size = int(args.b)

patternFiles = [p for p in os.listdir(srcDirectory) if p.endswith(".nmf")]
tstClasses   = next(os.walk(tstDirectory))[1]

allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png")]

errors = {}

for pat in patternFiles:
	mat = MAFR.loadMatrix(srcDirectory + pat)
	spe = MAFR.getSpecies(srcDirectory + pat)
	print(spe)
	patternError = MAFR.errorWithFiles(allFiles,mat)	
	for f in allFiles:
		if f not in errors or patternError[f] < errors[f][0]:
			errors[f] = (patternError[f],spe)

confusion = { x : {y: 0 for y in tstClasses} for x in tstClasses }

for f in allFiles:
	confusion[errors[f][1]][os.path.basename(os.path.dirname(f))] += 1

print(confusion)
