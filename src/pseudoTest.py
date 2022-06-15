import MAFR
import numpy as np
from sklearn import decomposition
import argparse
import os

parser = argparse.ArgumentParser("Test to see if pseudoinverse ever contains a negative value")
parser.add_argument("-f", type=str, help=".nmf pattern file to test")
parser.add_argument("-d", type=str, help="path to image directory to get coefficients")

args = parser.parse_args()

f = args.f
d = args.d

h, labels = MAFR.loadMatrix(f)

for species in os.listdir(d):
  subDir = d + "/" + species
  for i in os.listdir(subDir):
    path = subDir + "/" + i
    print(path)
    img = MAFR.loadImage(path, 16)
    imgMatrix = MAFR.imageToMatrix(img, 16)

    model = decomposition.NMF(n_components=64, init="custom", max_iter=10000, solver="mu")
    W = decomposition.NMF._fit_transform(imgMatrix, H=h, updateH=False)

    for row in W:
      for col in row:
        if col < 0:
          print("NEGATIVE FOUND IN COEFFICIENT")

      
