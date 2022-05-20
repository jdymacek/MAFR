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
file_list = []
for f in files:
  if f.endswith('.nmf'):
    path = directory + '/' + f
    m = MAFR.loadMatrix(path)
    e = MAFR.computeError(img_matrix, m)
    file_list += (f, e)
    s = MAFR.getSpecies(path)
    t = (e, s)
    errors.append(t)

#file_list.sort(key=lambda y: y[1])
#print(file_list)
#print('\n\n')

errors.sort(key=lambda y: y[0])
print(f'{errors[0][1]}\t{errors}')
