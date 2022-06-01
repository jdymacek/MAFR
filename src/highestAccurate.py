import struct
import numpy as np
from PIL import Image
from PIL import ImageOps
import os
import math
import MAFR

FILENAME1 = '/scratch/prism2022data/testing/AMRE/unit01-20150924232902_067383312_07663.png'
FILENAME2 = '/scratch/prism2022data/newFormat/06-01-22-11:38:42+16+1344.nmf'
SIZE = 16
BLOCKNUM = 10

def mostAccurateTool(filename1, filename2, size, blocknum):
  #open image
  img = MAFR.loadImage(filename1, size)
  #run the img to matrix
  matrix = MAFR.imageToMatrix(img, size) 
  print("Matrix 1 ", matrix) 
  #open the matrix
  patterns= MAFR.loadMatrix(filename2)

  #psuedo inverse johns thing
  mat = patterns[0]
  lbl = patterns[1]
  inv = np.linalg.pinv(mat)

  #multiply the 2 together to get coefficents
  mult = np.dot(matrix,inv)
  #print("This the mult: ", mult)

  print("Just row", mult[blocknum])
  row = mult[blocknum]
  print(len(row))
    
  #load in coefficents and labels (make a list of tuples with coefficent value and label)
  #[(coefficent, species),(),()...] 
  tups = []
  tups = list(zip(row,lbl))

  #sort and print
  s = sorted(tups, key=lambda tups:(-tups[0]))
  print(s)

mostAccurateTool(FILENAME1 , FILENAME2, SIZE, BLOCKNUM)




