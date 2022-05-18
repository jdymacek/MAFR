#!/usr/bin/python3

import MAFR
import argparse

parser = argparse.ArgumentParser(description='Simple Classifier')
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
  path = directory + '/' + f
  m = MAFR.loadMatrix(path)
  e = MAFR.computeError(img_matrix, m)
  s = MAFR.getSpecies(f)
  t = (e, s)
  errors.append(t)
  f.close()

min_tuple = min(errors, key=errors[0])

print(min_tuple[1])
