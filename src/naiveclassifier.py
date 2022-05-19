#!/usr/bin/python3

import MAFR
import argparse
import os

parser = argparse.ArgumentParser(description='Naive Classifier')
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

errors = []
for f in files:
  if f.endswith('.nmf'):
    path = directory + '/' + f
    m = MAFR.loadMatrix(path)
    e = MAFR.computeError(img_matrix, m)
    s = MAFR.getSpecies(path)
    t = (e, s)
    errors.append(t)

min_tuple = min(errors, key = lambda t: t[1])

print(f'Winner is {min_tuple}')
print(errors)
