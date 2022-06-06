import MAFR
import argparse
import numpy as np
from sklearn import decomposition
np.set_printoptions(threshold=np.inf)
import os

parser = argparse.ArgumentParser("Use Classifier for NFC Classification")
parser.add_argument("-p", help="path to combined .nmf file", required=True)
parser.add_argument("-t", help="path to tetsing directory", required=True)


CLASSES = ["AMRE", "BBWA", "BTBW", "CAWA", "COYE", "MOWA", "OVEN"]

args = parser.parse_args()

patternFile = args.p
trainingPath = args.t
blockSize = MAFR.getBlocksize(patternFile)

'''
img = MAFR.loadImage(imagePath, blockSize)
m = MAFR.imageToMatrix(img, blockSize)
'''

patterns, index = MAFR.loadMatrix(patternFile)

print(patterns.shape)


redstartCount = 0
bayBreastedCount = 0
blackThroatedCount = 0
canadaCount = 0
yellowthroatCount = 0
morningCount = 0
ovenCount = 0

counter = 0

training = os.listdir(trainingPath)
model = decomposition.NMF(n_components=len(patterns), init="random", random_state=0, max_iter=10000, solver="mu")

for expected in training:
  imgPath = trainingPath + "/" + expected
  imageDirectory = os.listdir(imgPath)
  for i in imageDirectory:
    hits = {k:0 for k in CLASSES}
    counter += 1
    img = MAFR.loadImage(imgPath + "/" + i, blockSize)
    m = MAFR.imageToMatrix(img, blockSize)
    model.fit(m)
    model.components_ = patterns

    W = model.transform(m)

    for row in W:
      idx = np.argmax(row)
#  idx = np.where(row == np.amax(row))
      winner = index[idx]
      hits[winner] += 1
    for key, val in hits.items():
      if key == "AMRE":
        redstartCount += val
      if key == "BBWA":
        bayBreastedCount += val
      if key == "BTBW":
        blackThroatedCount += val
      if key == "CAWA":
        canadaCount += val
      if key == "COYE":
        yellowthroatCount += val
      if key == "MOWA":
        morningCount += val
      if key == "OVEN":
        ovenCount += val

    print(hits)
    guess = max(hits, key=hits.get)
    print(guess + "\t" + expected)

print("AVERAGES")
print(f"AMRE: {redstartCount / counter}")
print(f"BBWA: {bayBreastedCount / counter}")
print(f"BTBW: {blackThroatedCount / counter}")
print(f"CAWA: {canadaCount / counter}")
print(f"COYE: {yellowthroatCount / counter}")
print(f"MOWA: {morningCount / counter}")
print(f"OVEN: {ovenCount / counter}")
