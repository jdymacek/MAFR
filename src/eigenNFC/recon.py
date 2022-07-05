import eigenNFC
import math
import numpy as np
from PIL import Image
import MAFR
import argparse
import csv
from sklearn import decomposition

parser = argparse.ArgumentParser()
parser.add_argument("-p", help="pattern file to view")
parser.add_argument("-w", help="weight file")
parser.add_argument("-i", help="image")

args = parser.parse_args()

file = args.p
weights = args.w

height = int(file.split("+")[-2])
width = int(file.split("+")[-3])

M, labels = MAFR.loadMatrix(args.p)
maximum = np.amax(M)
n = (M/maximum) * 255

#i = MAFR.loadImage(args.i, 16)
imgMatrix = [eigenNFC.imageToVector(args.i, x=(256-width)//2, y=0, width=width, height=height)]

lines = []
with open(weights) as data:
  for line in csv.reader(data, delimiter=","):
    lines.append(line)

weights = []
for line in lines:
  weights.append(line[1:])

weights = np.asarray(weights)
imgMatrix = np.asarray(imgMatrix)


print(imgMatrix)

print(f"IMGMARIX: {imgMatrix.shape}")
print(f"WEIGHTS: {weights.shape}")
print(f"N: {n.shape}")

model = decomposition.NMF(n_components=len(n), init="random", random_state=0, solver="mu", max_iter=10000)
model.fit(imgMatrix)
model.components_ = n
W = model.transform(imgMatrix)
recon = np.matmul(W, n)
print(np.linalg.norm(imgMatrix-np.dot(W, n)))


img = eigenNFC.arrayToImage(recon, width, height)
img.save("recon.png")
