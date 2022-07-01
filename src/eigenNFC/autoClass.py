from EigenTrainer import SimpleTrainer
from EigenClassifier import EigenAverage
import os
import subprocess
import argparse
import MAFR

parser = argparse.ArgumentParser("Testing harness for MAFR")
parser.add_argument("-p", help="range of pattern values", required=True)
parser.add_argument("-r", help="range of removal values", required=True)
parser.add_argument("-w", help="range of width values", required=True)
parser.add_argument("-d", help="training directory", required=True)
parser.add_argument("-t", help="testing directory", required=True)

args = parser.parse_args()
REMOVE = eval("[x for x in range" + args.r + "]")
WIDTH= eval("[x for x in range" + args.w + "]")
PATTERNS = eval("[x for x in range" + args.p + "]")
trainingDir = args.d
tstDirectory = args.t

host = os.uname()[1]
 
allTraining = [x[0] + "/" +  y  for x in os.walk(trainingDir) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]
allTraining.sort()
allTesting = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]
classes = MAFR.getClasses(trainingDir)

for p in PATTERNS:
    trainer = SimpleTrainer(allTraining, p) 
    for r in REMOVE:
      for w in WIDTH:
          trainer.updateSize((256-r), w)
          classifier = EigenAverage(classes, p, w, (256 - r))
          weights, patterns = trainer.train()

          classifier.updateModel(patterns, weights)
          acc = classifier.classifyAll(allTesting)

          fout = open(f"exploreOut/{host}.txt", "a")
          fout.write(f"{p},{w},{r},{round(acc,3)}\n")
          fout.close()

