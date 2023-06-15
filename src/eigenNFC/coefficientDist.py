from EigenTrainer import SimpleTrainer
from EigenClassifier import EigenRegression
import os
import subprocess
import argparse
import MAFR
from Timer import Timer


parser = argparse.ArgumentParser("Testing harness for MAFR")
parser.add_argument("-n", help="number of pattern", required=True)
parser.add_argument("-d", help="samples directory", required=True)
parser.add_argument("-t", help="training percentage", required=True)

parser.add_argument("-s", help="species", required=True)
args = parser.parse_args()
p = int(args.n)

host = os.uname()[1]
w = 52
r = 116

allFiles, classes = MAFR.listAllFiles(args.d)
allTraining, allTesting = MAFR.splitSamples(allFiles, classes, float(args.t))

print(f'{len(allTraining)}\t{len(allTesting)}')


trainer = SimpleTrainer(allTraining, p) 
trainer.updateSize((256-r), w)
weights, patterns = trainer.train()

vals = [w[1] for w in weights if w[0] == args.s]
print(vals)
