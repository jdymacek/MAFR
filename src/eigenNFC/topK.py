import eigenNFC
import MAFR
import csv
import os
import argparse
from sklearn import decomposition
import numpy as np
import math
from collections import Counter
import statistics

PATH = "/scratch/prism2022data/data/"

frequencies = {"AMRE":0.077, "BBWA":0.062, "BTBW":0.098, "CHSP":0.089, "COYE":0.161, "OVEN":0.318, "SAVS":0.194}

parser = argparse.ArgumentParser()
parser.add_argument("-p", help="patternfile")
parser.add_argument("-d", help="directory to classify (relative to /scratch/prism2022data/data")
parser.add_argument("-k", help="number to keep")


args = parser.parse_args()
patternFile = args.p
num = int(args.k)

HEIGHT= int(patternFile.split("+")[-2])
WIDTH= int(patternFile.split("+")[-3])

CSV = "test.csv"
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

data = open("data.csv", "w")
data.write("CORRECT,SIZE,NUMCORRECT,MOSTCOMMON,COMMONCOUNT")

correctTotal = 0
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

  
  #topK = sorted(errors)[:num]
  total = [x[0] for x in errors]
  stdDev = statistics.pstdev(total)
  mean = statistics.mean(total)
  topK = [x for x in errors if x[0] < mean - 0.98*stdDev]
  topK.sort()

  size = len(topK)
  acc = 0
  for val in topK:
    if val[1] == f.split("/")[-2]:
      acc += 1
      
  labels = [e[1] for e in topK]
  if len(labels) > 0:
    mostCommon = Counter(labels).most_common(1)[0][0]
    commonCount = labels.count(mostCommon)
  else:
    mostCommon = "JUNK"
    commonCount = 0

  """
  for idx, val in enumerate(topFive):
    asList = list(val)
    asList[0] += (5-idx) 
    tup = tuple(asList)
    topFive[idx] = tup
"""
#print percentage for topK for each class 
  if len(labels) == 0:
    percents = {k:0 for k in tstClasses} 
  else:
    percents = {k:labels.count(k)/len(labels) for k in tstClasses} 

#print(f.split('/')[-2])

#count how many res[0][1] == correct

  res = [(percents[x]/frequencies[x],x) for x in tstClasses]
  res.sort(reverse=True)
#print(res)

  correctLabel = f.split("/")[-2]
  correctWeight = percents[correctLabel]/frequencies[correctLabel]

  if res[0][1] != correctLabel:
    print(f"RES[0]: {res[0]}")
    print(f"{correctLabel},{size},{acc},{mostCommon},{commonCount}")
    print(f":CORRECTWEIGHT: {correctWeight}")
    correctTotal += 1

  if res[0][1] == f.split("/")[-2]:
    correctTotal += 1

  data.write(f"{f.split('/')[-2]},{size},{acc},{mostCommon},{commonCount}\n")
  confusion[res[0][1]][correctLabel] += 1

total = [confusion[x][x] for x in tstClasses]
print(sum(total)/len(allFiles))
print(confusion)
data.close()
quit()

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
  """
