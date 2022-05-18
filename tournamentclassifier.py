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
  path = directory + '/' + f
  m = MAFR.loadMatrix(path)
  e = MAFR.computeError(img_matrix, m)
  s = MAFR.getSpecies(f)
  if s in errors:
    errors[s] += e
  else:
    errors[s] = [e]

  print(errors)

  keys = errors.keys()
  winners = {}

for i in range(10000):
  key_1 = keys[random.randint(0,len(keys))]
  key_2 = keys[random.randint(0,len(keys))]
  val_1 = errors[key_1][random.randint(0,len(errors[key_1]))]
  val_2 = errors[key_2][random.randint(0,len(errors[key_2]))]
  winner = min(val_1, val_2)
  if winner == val_1:
    if key_1 in winners:
      winners[key_1] += 1
    else:
      winners[key_1] = 1
  else if winner == val_2:
    if key_2 in winners:
      winners[key_2] += 1
    else:
      winners[key_2] = 1

print(min(d, key=d.get))

