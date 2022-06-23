import eigenNFC
import MAFR
import csv
import os
import argparse
from sklearn import decomposition
import numpy as np
import math
from collections import Counter

PATH = "/scratch/prism2022data/data/"

parser = argparse.ArgumentParser()
parser.add_argument("-p", help="patternfile")
parser.add_argument("-d", help="directory to classify (relative to /scratch/prism2022data/data")

args = parser.parse_args()
patternFile = args.p

HEIGHT= int(patternFile.split("+")[-2])
WIDTH= int(patternFile.split("+")[-3])

CSV = "weights.csv"
tstDirectory = PATH + args.d
#print(tstDirectory)
lines = []
with open(CSV) as data:
    for line in csv.reader(data,  delimiter=","):
        lines.append(line)

entries = []
for line in lines:
  entries.append((line[0], line[1:]))

allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]

tstClasses = MAFR.getClasses(tstDirectory)

patterns, labels = MAFR.loadMatrix(patternFile)

M1 = [[eigenNFC.imageToVector(allFiles[0], x=72, y=0, width=WIDTH, height=HEIGHT)]]
M = np.concatenate(M1)

model = decomposition.NMF(n_components=len(patterns), init="random", random_state=0, max_iter=30000, solver="mu")
model.fit(M)
model.components_ = patterns

confusion = { x : {y: 0 for y in tstClasses} for x in tstClasses }
 
csv = open("dist.csv", "w")
csv.write("FILENAME,CORRECT_CLASS,DIST1,CLASS1,DIST2,CLASS2,DIST3,CLASS3,DIST4,CLASS4,DIST5,CLASS5\n")
for f in allFiles:
  line = ""
  line += f + "," + f.split("/")[-2] + ","
  M1 = [[eigenNFC.imageToVector(f, x=72, y=0, width=WIDTH, height=HEIGHT)]]
  M = np.concatenate(M1)
#print(f)
  W = model.transform(M)

  errors = []
  best = ("JUNK", 9999)
  for e in entries:
    vals = e[1]
    arr = np.array(vals, dtype=np.float32)
    guess = e[0]
    error = np.linalg.norm(arr - W[0])
    e = (error, e[0]) 
    errors.append(e)
    if error < best[1]:
      best = (guess, error)

  topFive = sorted(errors)[:5]
  """
  for idx, val in enumerate(topFive):
    asList = list(val)
    asList[0] += (5-idx) 
    tup = tuple(asList)
    topFive[idx] = tup
"""

  labels = [e[1] for e in topFive]
  mostCommon = Counter(labels).most_common(1)[0][0]
  commonCount = labels.count(mostCommon)

  if commonCount >= 2:
    best = (mostCommon, 0)
  
  for i in topFive:
    line += str(i[0]) + "," + str(i[1]) + ","
  line += best[0] + "\n"
  csv.write(line)
  confusion[best[0]][f.split("/")[-2]] += 1
#print(best)

#print(confusion)

correct = {k:confusion[k][k] for k in tstClasses}
#print(correct)

correctGuesses = sum(correct.values())
parameters = {"Patterns": len(patterns), "Removed": 256 - HEIGHT, "Correct":correctGuesses, "Percent": correctGuesses / len(allFiles)}
#print("PARAMETERS")
print(parameters)
#print(sum(correct.values()))
#print(errors)
csv.close()
