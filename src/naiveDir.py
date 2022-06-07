#!/usr/bin/python3

#naiveDir.py
#runs naive classifier on entire directory

import MAFR
import argparse
import os
import sys
import datetime
import naiveclassifier
import csv

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
outputPath = outputDir + '/' + 'naive-' + str(num).zfill(2) + '-' + str(blockSize) + '.csv'
while(1):
  if os.path.exists(outputPath):
    num += 1
    outputPath = outputDir + '/' + 'naive-' + str(num).zfill(2) + '-' + str(blockSize) + '.csv'
  else:
    break

hits = {k:0 for k in dirs}
rv = {k:hits for k in dirs}
#print(rv)

for d in dirs:
  dPath = testingDir + '/' + d
  pngs = os.listdir(dPath)
  expect = dPath[-4:]
  print(expect)

  for img in pngs:
    imgPath = dPath + "/" + img
    guess = naiveclassifier.naiveclassifier(patternDir, imgPath, blockSize)
    rv[expect][guess] += 1

print(rv)


with open(outputPath, "w") as csvfile:
  writer = csv.DictWriter(csvfile, dirs)
  for key, val in sorted(rv.items()):
    row = {dirs[0]: key}
    row.update(val)
    writer.writerow(row)
csvfile.close()

'''
    with open(outputPath, 'a') as f:
      f.write(f'{species}\t')
    imgPath = dPath + '/' + img
#print(outputPath)
    os.system(f'python3 naiveclassifier.py -d {patternDir} -f {imgPath} -b {str(blockSize)} >> {outputPath}')
'''
