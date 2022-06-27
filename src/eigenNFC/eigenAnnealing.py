from EigenClassifier import EigenClassifier
import MAFR
import eigenNFC
import numpy as np
import PIL
from PIL import Image
import argparse
import os
from sklearn import decomposition
import time
import random
import math


parser = argparse.ArgumentParser(description='Convert an image to a vector')
parser.add_argument('-t', help='training directory')
parser.add_argument('-p', help = 'number of patterns')
parser.add_argument('-r', help = 'clip r pixels from bottom of images')
parser.add_argument('-w', help = 'width of image area')

args = parser.parse_args()

tstDirectory = args.t
PATTERNS = int(args.p)
HEIGHT = 256 - int(args.r)
width = int(args.w)

"""
dirs = os.listdir(tstDirectory)
dirs  = [x for x in dirs if len(x) == 4]
print(dirs)
allFiles = [tstDirectory + "/" + 
"""

classifier = EigenClassifier(MAFR.getClasses(tstDirectory), PATTERNS, width, HEIGHT) 
#allFiles = [os.path.basename(x[0])  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png")]
allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]
#print(allFiles)
random.shuffle(allFiles)
training = allFiles[:len(allFiles)//2]
testing = allFiles[len(allFiles)//2:]

model = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=30000, solver="mu")

currentState = training
currentAccuracy = 100
currentPatterns = None
currentWeights = None
best = currentState
bestAccuracy = currentAccuracy
bestPatterns = currentPatterns
bestWeights = currentWeights

temp = 20
alpha = 0.1
finalTemp = 0.1

while temp > finalTemp:
### SWAP THINGS ###
  random.shuffle(testing)
  random.shuffle(training)
  for j in range(2*math.ceil(temp)):
    training[j], testing[j] = testing[j], training[j]
### BUILD TRAINING MATRIX ### 
  ml = []
  labels = []
  for f in training:
    labels.append(f.split("/")[-2])
    arr = eigenNFC.imageToVector(f, x=(256/width)//2, y=0, width=width, height=HEIGHT)
    ml += [[arr]]

  M = np.concatenate(ml)

  ### FINDING PATTERNS ###
  w = model.fit_transform(M)
  w = [x for x in zip(labels, w)]
  classifier.updateModel(model.components_, w)
  accuracy = (1 - classifier.classifyAll(testing)) * 100
  print(accuracy)

  diff = accuracy - currentAccuracy

  print(f"CURR: {currentAccuracy}\tNEIGHBOR: {accuracy}\t TEMP:{temp}")

  if diff < 0:
    currentState = training
    currentAccuracy = accuracy
    currentPatterns = model.components_
    currentWeights = w
  else:
    if random.uniform(0,1) < math.exp(-diff/temp):
      currentState = training
      currentAccuracy = accuracy
      currentPatterns = model.components_
      currentWeights = w

  if currentAccuracy < bestAccuracy:
    best = currentState
    bestAccuracy = currentAccuracy
    bestPatterns = currentPatterns
    bestWeights = currentWeights

  temp -= alpha 

file = MAFR.saveMatrix(bestPatterns, PATTERNS, width, HEIGHT) 

weightName = str(PATTERNS) + "+" + str(args.r) + ".csv"
weights = open(weightName, "w")
for idx, row in enumerate(bestWeights):
  rounded = [np.round(x, decimals=5) for x in row[1]]
  line = row[0] +"," +  ",".join(map(str, rounded)) + "\n"
  weights.write(line)

#weights.write(str(row).replace("\n", "").strip("\t") + "\n")

print(file)
