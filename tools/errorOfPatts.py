import os
import numpy as np
from MAFR import loadImage,imageToMatrix, computeError, saveMatrix, loadMatrix
import random
import argparse
from sklearn import decomposition
import csv
from statistics import mean

parser = argparse.ArgumentParser()
parser.add_argument('-d', help='directory of the patterns')
arg = parser.parse_args()

blockList = os.listdir(arg.d)
blockList.sort()
os.chdir(arg.d)

f = open('bigBlockErrors.csv', 'w')
writer = csv.writer(f)
header = ['Class', 'AMRE', 'BBWA', 'BTBW', 'CAWA', 'COYE', 'MOWA', 'OVEN']
writer.writerow(header)
j=0

#loop to go through each class
while j < len(blockList):
  print(j)
  if '.nmf' in blockList[j]:
     mat_list = []
     m=0
     while m < 1:
     #this is a one time thing, just for indent

       #this loop goes through each class to pick for the versus
       errList =[]
       errList.append(blockList[j])

       training_dirs = os.listdir('/scratch/prism2022data/training_inverse')
       for class_dir in training_dirs:
           avgErr = 0
           numErrs = 0
           training_list = os.listdir('/scratch/prism2022data/training_inverse/'+class_dir)
           l=0
           rand_train = []
           sum_err = []
           #this will calculate average error
           while l < 20:
                 randImg = loadImage('/scratch/prism2022data/training_inverse/'+class_dir+'/'+training_list[random.randint(0, len(training_list)-1)], 16)

                 randMat = imageToMatrix(randImg, 16)
                 curr_err = computeError(loadMatrix(blockList[j]), randMat)
                 sum_err.append(curr_err)
                 l+=1
           new_err = mean(sum_err)
           errList.append(new_err)

          
       writer.writerow(errList)
       m+=1
     j+=1
  else:
    j+=1
    continue
#f.close()

