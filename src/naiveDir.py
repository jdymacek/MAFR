#!/usr/bin/python3

#naiveDir.py
#runs naive classifier on entire directory

import MAFR
import argparse
import os
import sys
import datetime

cwd = os.getcwd
parser=argparse.ArgumentParser()

#directory of files to be tested, directory to .nmf files, species code,
#number of patterns

parser.add_argument('-i', metavar='testing directory', default=cwd, help='path to directory containing .png files for testing')
parser.add_argument('-d', metavar='directory of .nmf files', default=cwd, help='path to directory containging .nmf files')
parser.add_argument('-b', metavar='block size', default=16, help='blocksize of patterns')
parser.add_argument('-o', metavar='output directory', default=cwd, help='path to where output files should go')

args = parser.parse_args()

patternDir = args.d
testingDir = args.i
blockSize = int(args.b)
outputDir = args.o

dirs = os.listdir(testingDir)
out = os.listdir(outputDir)

num = 0
outputPath = outputDir + '/' + 'naive-' + str(num).zfill(2) + '-' + str(blockSize) + '.txt'
while(1):
  if os.path.exists(outputPath):
    num += 1
    outputPath = outputDir + '/' + 'naive-' + str(num).zfill(2) + '-' + str(blockSize) + '.txt'
  else:
    break

for d in dirs:
  dPath = testingDir + '/' + d
  pngs = os.listdir(dPath)
  species = dPath[-4:]
  print(species)

  for img in pngs:
    with open(outputPath, 'w') as f:
      f.write(f'{species}\t')
      imgPath = dPath + '/' + img
      print(outputPath)
      os.system(f'python3 naiveclassifier.py -d {patternDir} -f {imgPath} -b {str(blockSize)} >> {outputPath}')

