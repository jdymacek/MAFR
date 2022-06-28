from yaml import parse
import MAFR
import os
import argparse
from sklearn import decomposition

parser = argparse.ArgumentParser("Finds Error per File")
parser.add_argument("-d", help="directory to check")
parser.add_argument("-p", help="number of patterns")

args = parser.parse_args()

tstDirectory = args.d
PATTERNS = int(args.p)

allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]

for f in allFiles:
  name = f.split("/")[-2:]
  original = MAFR.imageToMatrix(MAFR.loadImage(f, 16), 16)
  model = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=30000, solver="mu")
  W = model.fit_transform(original)
  patterns = model.components_

  print(f"{f}\t{MAFR.computeError(original, patterns)}")
