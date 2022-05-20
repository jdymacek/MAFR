#!/usr/bin/python3

#naiveDir.py
#runs naive classifier on entire directory

import MAFR
import argparse
import os
import sys

cwd = os.getcwd
parser=argparse.ArgumentParser()

#directory of files to be tested, directory to .nmf files, species code,
#number of patterns

parser.add_argument('-i', metavar='directory of .png files', default=cwd, help='path to directory containing .png files for testing')
parser.add_argument('-d', metavar='directory of .nmf files', default=cwd, help='path to directory containging .nmf files')
parser.add_argument('-b', metavar='block size', default=16, help='blocksize of patterns')
parser.add_argument('-o', metavar='output directory', default=cwd, help='path to where output files should go')

args = parser.parse_args()

patternDir = args.d
imageDir = args.i
blockSize = int(args.b)
outputDir = args.o
species = imageDir[-5:-1]
print(species)

pngs = os.listdir(imageDir)

for img in pngs:
  imgPath = imageDir + '/' + img
  outputPath = outputDir + '/' + 'naive-' + species + '-' + img + '-' + str(blockSize) + '.txt'
  with open(outputPath, 'w') as f:
    f.write(f'{species}\t')
  os.system(f'python3 naiveclassifier.py -d {patternDir} -f {imgPath} -b {str(blockSize)} >> {outputPath}')

