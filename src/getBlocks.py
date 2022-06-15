import MAFR
import os
import numpy as np
import argparse
import random
from sklearn import decomposition
import PIL



parser = argparse.ArgumentParser("Tool to get n random blocks from training")
parser.add_argument("-b", required=True, help="Number of blocks to extract")
parser.add_argument("-d", required=True, help="directory to read and save to")

args = parser.parse_args()

blocks = int(args.b)

PATH = "/scratch/prism2022data/data/" + args.d + "/" 

files = [x[0] + "/" + y for x in os.walk(PATH+"training") for y in x[2] if y.endswith(".png")]


ml = []
for i in range(2*blocks):
    f = random.choice(files)
    m = MAFR.imageToMatrix(MAFR.loadImage(f,16),16)
    b = m[np.random.choice(len(m)), :]
    ml += [[b]]
M = np.concatenate(ml)
print(M.shape)


model = decomposition.NMF(n_components=blocks, init="random", random_state=0, max_iter=10000, solver="mu")
model.fit_transform(M)
img = MAFR.matrixToImage(M, 16, 16)
img.save(PATH + "bigBlocks/JUNK/JUNK_annotatedBlock.png")
