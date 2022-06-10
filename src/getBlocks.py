import MAFR
import os
import numpy as np
import argparse
from sklearn import decomposition

TRAINING = "/scratch/prism2022data/training-inverse/"

parser = argparse.ArgumentParser("Tool to get n random blocks from training")
parser.add_argument("-b", required=True, help="Number of blocks to extract")

args = parser.parse_args()

blocks = int(args.b)

files = [x[0] + "/" + y for x in os.walk(TRAINING) for y in x[2] if y.endswith(".png")]

ml = []
for i in range(2*blocks):
    f = random.choice(files)
    m = MAFR.imageToMatrix(MAFR.loadImage(f,16),16)
    b = m[np.random.choice(len(m)), :]
    ml += [b]
M = np.concatenate(ml)

model = decomposition.NMF(n_components=blocks, init="random", random_state=0, max_iter=10000, solver="mu")
model.fit_transform(M)
MAFR.saveMatrix(model.components_, blocks, 16, "JUNK")