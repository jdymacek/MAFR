from EigenTrainer import SimpleTrainer
from EigenClassifier import EigenRegression
import os
import subprocess
import argparse
import MAFR
from Timer import Timer
import numpy as np
from PIL import Image, ImageOps

parser = argparse.ArgumentParser("Testing harness for MAFR")
parser.add_argument("-n", help="number of pattern", required=True)
parser.add_argument("-d", help="samples directory", required=True)
parser.add_argument("-t", help="training percentage", required=True)

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
classes = sorted(classes)
classes += ["all"]
img = []
for i in range(0,p):
    for c in classes:
        if c != "all":
            vals = [w[1] for w in weights if w[0] == c]
        else:
            vals = [w[1] for w in weights]
        v =[x[i] for x in vals]
        h,b = np.histogram(v, bins = 25, range = (0,1))
        h = h/sum(h)
        h *= 255 
        h = h.astype(np.uint8)
        img.append(h)
img = np.asarray(img)
pix = Image.fromarray(img)
pix= ((pix.width*3, pix.height*3))
pix.save("histogram.png")


