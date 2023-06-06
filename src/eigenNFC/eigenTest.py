from EigenClassifier import EigenClassifier, EigenRegression, EigenMajority, EigenAverage, EigenVersus, EigenTrickle
import eigenNFC
import MAFR
import csv
import os
import argparse
from sklearn import decomposition
import numpy as np
import math
from collections import Counter
import time


parser = argparse.ArgumentParser()
parser.add_argument("-p", help="patternfile")
parser.add_argument("-d", help="directory to classify")
parser.add_argument("-w", help="CSV file with coefficients")

args = parser.parse_args()
patternFile = args.p
HEIGHT= int(patternFile.split("+")[-2])
WIDTH= int(patternFile.split("+")[-3])
PATTERN_NUM = int(patternFile.split("+")[-1][:-4])
CSV = args.w

tstDirectory = args.d
#print(tstDirectory)
lines = []
with open(CSV) as data:
    for line in csv.reader(data,  delimiter=","):
        lines.append(line)

weights = []
tstClasses = []
for line in lines:
  tstClasses += [line[0][:4]]
  weights.append((line[0], line[1:]))

tstClasses = list(set(tstClasses))

allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]


#tstClasses = MAFR.getClasses(tstDirectory)


tstClasses += ["JUNK"]
patterns, labels = MAFR.loadMatrix(patternFile)

for x in tstClasses:
   print(f"{x}\t\t",end="\t")
print("")

#for t in [x/100.0 for x in range(10,100,5)]:
#   regression = EigenRegression(tstClasses, PATTERN_NUM, WIDTH, HEIGHT)
#   regression.threshold = t
#   regression.updateModel(patterns, weights)
#   acc = regression.classifyAll(allFiles)
#   print(f"{round(acc,5)}")
#  print(f"{PATTERN_NUM},{WIDTH},{256-HEIGHT},{round(acc, 3)}")
   
regression = EigenRegression(tstClasses,PATTERN_NUM,WIDTH,HEIGHT)
regression.threshold = 0.75
regression.updateModel(patterns,weights)
acc = regression.classifyAll(allFiles)
print(f"{round(acc,5)}")


"""
classifier = EigenClassifier(tstClasses, PATTERN_NUM, WIDTH, HEIGHT)
classifier.updateModel(patterns, weights)
acc = classifier.classifyAll(allFiles)
"""

"""
majority = EigenMajority(tstClasses, PATTERN_NUM, WIDTH, HEIGHT)
majority.updateModel(patterns, weights)
acc = majority.classifyAll(allFiles)
print(f"MAJORITY: {acc}")
"""
"""
average = EigenAverage(tstClasses, PATTERN_NUM, WIDTH, HEIGHT)
average.updateModel(patterns, weights)
acc = average.classifyAll(allFiles)
print(f"{PATTERN_NUM},{WIDTH},{256-HEIGHT},{round(acc, 3)}")
"""
"""
trickle = EigenTrickle(tstClasses, PATTERN_NUM, WIDTH, HEIGHT)
trickle.updateModel(patterns, weights)
acc = trickle.classifyAll(allFiles)
print(f"TRICKLE: {acc}")

for c in tstClasses:
  versus = EigenVersus([c,"REST"], PATTERN_NUM, WIDTH, HEIGHT)
  versus.updateModel(patterns, weights)
  acc = versus.classifyAll(allFiles)
  print(f"{c}: {acc}")
  print(versus.confusion)

"""
