import MAFR
import argparse
import numpy as np
from sklearn import decomposition
np.set_printoptions(threshold=np.inf)

parser = argparse.ArgumentParser("Use Classifier for NFC Classification")
parser.add_argument("-p", help="path to combined .nmf file", required=True)
parser.add_argument("-i", help="image to classify", required=True)


CLASSES = ["AMRE", "BBWA", "BTBW", "CAWA", "COYE", "MOWA", "OVEN"]

args = parser.parse_args()

patternFile = args.p
imagePath = args.i
blockSize = MAFR.getBlocksize(patternFile)

img = MAFR.loadImage(imagePath, blockSize)
m = MAFR.imageToMatrix(img, blockSize)

patterns, index = MAFR.loadMatrix(patternFile)

print(patterns.shape)

hits = {k:0 for k in CLASSES}
print(hits)


model = decomposition.NMF(n_components=len(patterns), init="random", random_state=0, max_iter=10000, solver="mu")
model.fit(m)
model.components_ = patterns

W = model.transform(patterns)

print(W)

for row in W:
  idx = np.where(row == np.amax(row))
  winner = index[idx[0][0]]
  hits[winner] += 1

print(hits)
