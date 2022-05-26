import argparse
import os
import numpy as np
from MAFR import imageToMatrix, matrixToImage, loadImage, closestDivisor
from PIL import Image
parser = argparse.ArgumentParser()
parser.add_argument('-d', metavar = 'input_directory', help='directory where pngs are located')
parser.add_argument('-t', metavar = '.txt file', help = 'file that has all the blocks containing pngs with their retrospective png')

args = parser.parse_args()
file_list = os.listdir(args.d)
M = []
for filename in file_list:
    with open(args.t) as temp_f:
        datafile = temp_f.readlines()
    for line in datafile:
        if filename in line:
#print(filename)
           lineParsed = line.split()
           i=1
           while i < len(lineParsed):
                 #get the blocks from the image
                 theBlock = int(lineParsed[i])

                 #convert image to matrix
                 imgLoaded = loadImage(args.d+'/'+filename, 256)
                 matImg = imageToMatrix(imgLoaded, 16)
                 
                 #now with the block, find the part of the matrix that matches
                 row = matImg[theBlock]
#print(row)
                 i += 1
                 M += [row]
h = closestDivisor(len(M))
w = len(M)//h
print(h, w)
bigImg = matrixToImage(M, w, h)
#print(len(M))
bigImg.save("allBlockSignals.png")
