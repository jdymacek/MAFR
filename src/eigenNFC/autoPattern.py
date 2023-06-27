from EigenTrainer import SimpleTrainer
from EigenClassifier import EigenRegression, EigenBayes, EigenCluster, EigenMultiCluster
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
#w = 52
#r = 128

analysis = "Shifted"
w = 52
r = 52

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

    #bayes = ProbabilityModel(weights,classes,bins=50)


    #stopwatch.start()
    #classifier = EigenBayes(classes,p, w, (256 -r))
    classifier = EigenMultiCluster(classes,p, w, (256-r))
    #stopwatch.stop()
    #stopwatch.print()


    stopwatch.start()
    classifier.updateModel(patterns,weights)

    acc = classifier.classifyAll(allTesting)
  # classifier.printConfusion()
    stopwatch.stop()
    stopwatch.print()
    results = f"{classifier}\t{p}\t{w}\t{r}\t{float(args.t)}\t{analysis}\t{round(acc,4)}"
    print(results)
    fout = open(f"{host}.txt", "a")
    fout.write(results+"\n")
    fout.close()

