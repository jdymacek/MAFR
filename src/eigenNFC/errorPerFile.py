import eigenNFC
import MAFR
import os
import argparse
from sklearn import decomposition
import numpy as np

parser = argparse.ArgumentParser("Finds Error per File")
parser.add_argument("-d", help="directory to check")
parser.add_argument("-p", help="number of patterns")
parser.add_argument('-r', help = 'clip r pixels from bottom of images')
parser.add_argument('-w', help = 'width')

args = parser.parse_args()

tstDirectory = args.d
PATTERNS = int(args.p)
HEIGHT = 256 - int(args.r)
WIDTH = int(args.w)

allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]

### build big matrix ###
ml = []
for f in allFiles:
  arr = eigenNFC.imageToVector(f, x=(256-WIDTH)//2, y=0, width=WIDTH, height=HEIGHT)
  ml += [[arr]]
M = np.concatenate(ml)

model = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=30000, solver="mu")
W = model.fit_transform(M)
H = model.components_

### w[i] * h => find distance between that and w[i] ###
for i, row in enumerate(W):
  val = np.matmul(row, H)
  print(f"{allFiles[i]}\t{np.linalg.norm(val)}")



"""
for f in allFiles:
  name = f.split("/")[-2:]
  original = MAFR.imageToMatrix(MAFR.loadImage(f, 16), 16)
  W = model.fit_transform(original)
  patterns = model.components_

  print(f"{f}\t{MAFR.computeError(original, patterns)}")
"""