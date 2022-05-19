#!/usr/bin/python3

import MAFR
import os
import argparse
import random

parser = argparse.ArgumentParser(description='Tournament Classifier')
parser.add_argument('-d', help='directory of desired .nmf pattern files') #patterns
parser.add_argument('-f', help='image file to be tested') #file to be tested
parser.add_argument('-b', help='block size of tiles')

args = parser.parse_args()

directory = args.d
img_name = args.f
size = int(args.b)


img = MAFR.loadImage(img_name, size)
img_matrix = MAFR.imageToMatrix(img, size)
files = os.listdir(directory)

errors = {}
for f in files:
  if f.endswith('.nmf'):
    path = directory + '/' + f
    m = MAFR.loadMatrix(path)
    e = MAFR.computeError(img_matrix, m)
    s = MAFR.getSpecies(path)
    if s in errors:
      errors[s] += [e]
    else:
      errors[s] = [e]

#print(errors)

keys = errors.keys()
winners = {k:0 for k in keys}

for i in range(10000):
  k = random.sample(keys,2)
  val_1 = random.sample(errors[k[0]], 1)
  val_2 = random.sample(errors[k[1]], 1)
  winner = min(val_1, val_2)
  if val_1 < val_2:
      winners[k[0]] += 1
  elif val_2 < val_1:
      winners[k[1]] += 1

min_key = (min(d, key=d.get))
print(f'The winner is {min_key} : {winners[min_key]}')
print(winners)

