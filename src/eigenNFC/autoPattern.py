from EigenTrainer import SimpleTrainer
from EigenClassifier import EigenRegression, EigenBayes
import os
import subprocess
import argparse
import MAFR
from ProbabilityModel import ProbabilityModel
from Timer import Timer


parser = argparse.ArgumentParser("Testing harness for MAFR")
parser.add_argument("-n", help="range of pattern values", required=True)
parser.add_argument("-d", help="samples directory", required=True)
parser.add_argument("-t", help="training percentage", required=True)

args = parser.parse_args()
PATTERNS = eval("[x for x in range" + args.n + "]")

host = os.uname()[1]
w = 52
r = 128

allFiles, classes = MAFR.listAllFiles(args.d)
allTraining, allTesting = MAFR.splitSamples(allFiles, classes, float(args.t))

print(f'{len(allTraining)}\t{len(allTesting)}')

stopwatch = Timer()
for p in PATTERNS:
    stopwatch.start()
    trainer = SimpleTrainer(allTraining, p) 
    trainer.updateSize((256-r), w)
    weights, patterns = trainer.train()

    stopwatch.stop()
    stopwatch.print()

    stopwatch.start()
    bayes = ProbabilityModel(weights,classes,bins=50)


    stopwatch.stop()
    stopwatch.print()

    stopwatch.start()
    classifier = EigenBayes(classes,p, w, (256 -r))
    classifier.updateModel(patterns,bayes)

    acc = classifier.classifyAll(allTesting)
    print(acc)
    classifier.printConfusion()
    stopwatch.stop()
    stopwatch.print()
  #  fout = open(f"{host}.txt", "a")
  #  fout.write(f"{p},{w},{r},{round(acc,3)}\n")
  #  fout.close()

