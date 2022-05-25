#!/usr/bin/python3

#autopattern.py

import argparse
import MAFR
import os
import random
import numpy as np
from sklearn import decomposition
from PIL import Image

cwd = os.getcwd()
parser = argparse.ArgumentParser()

parser.add_argument('-d', metavar='D', default=cwd, help='path to directory of .pngs to generate patterns on')
parser.add_argument('-p', metavar='P', default=32, help='number of patterns to keep')
parser.add_argument('-b', metavar='B', default=16, help='size of tiles')
parser.add_argument('-o', metavar='O', default=cwd, help='output directory')
parser.add_argument('-n', metavar='N', default=5, help='how many images')
parser.add_argument('-s', metavar='S', default=3, help='how many patterns per species')

arg = parser.parse_args()

n_components = int(arg.p)
blockSize = int(arg.b)
file_num = int(arg.n)
pps = int(arg.s)

dirs = os.listdir(arg.d)

for d in dirs:
  species = d[-5:]
  print(species)
  dPath = arg.d + '/' + d
  files = os.listdir(dPath)
  patterns = []
  errors = {}
  for i in range(pps):
    print('Iter' + str(i + 1))
    pngs = [x for x in files if x.endswith('.png')]
    random.shuffle(pngs)
    pngs = pngs[:file_num]
  
    ml = []
    for i in pngs:
      filePath = dPath + '/' + i
      img = MAFR.loadImage(filePath, blockSize)
      m = MAFR.imageToMatrix(img, blockSize)
      ml += [m]

    M = np.concatenate(ml)
    print('Big M: ' + str(M.shape))

    #only keep pattern with the least average error
    print('Performing NMF')
    estim = decomposition.NMF(n_components=n_components, init='random', random_state=0, max_iter=10000, solver='mu')
    w = estim.fit_transform(M)
    h = estim.components_
    error = estim.reconstruction_err_
    patterns.append(h)

  for idx, p in enumerate(patterns):
    total = 0
    for i in files:
      path = dPath + '/' + i
      img = MAFR.loadImage(path, blockSize)
      original = MAFR.imageToMatrix(img, blockSize)
#pinv = np.linalg.pinv(p)
      e = MAFR.computeError(original, p)
      total += e
    avg = total / len(files)
    errors[idx] = avg
  for i in range(4):
    lowest = min(errors, key=errors.get)
    MAFR.saveMatrix(patterns[lowest], arg.p, arg.b, species, out=arg.o)
    errors.pop(lowest)

