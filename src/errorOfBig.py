import os
import numpy as np
from MAFR import loadImage,imageToMatrix, computeError, saveMatrix
import random 
import argparse
from sklearn import decomposition
import csv

#takes each big randomly annotated blocks of each class and 
#computes the error of it versus 20 images from the training inverse set of each class
#takes the average of those errors and puts them into a .csv file

cwd = os.getcwd()
blockList = os.listdir(cwd+'/bigBlockClasses')
blockList.sort()

f = open('bigBlockErrors.csv', 'w')
writer = csv.writer(f)
header = ['Class', 'AMRE', 'BBWA', 'BTBW', 'CAWA', 'COYE', 'MOWA', 'OVEN']
writer.writerow(header)
j=0

#loop to go through each class
while j < len(blockList):
  if '.png' in blockList[j]:
     curImg = loadImage(cwd+'/bigBlockClasses/'+blockList[j], 16)
     curMat = imageToMatrix(curImg, 16)
     mat_list = []
     k=0
     while k < 16:
       random_row = curMat[random.randint(0, 255)]
       mat_list.append(random_row)
       k+=1
     m=0
     while m < 1:
     #this is a one time thing, just for indent
 

       header_list = [blockList[j][:4]]
       estim = decomposition.NMF(n_components=16, init='random', random_state=0, max_iter=10000, solver='mu')
       w_mat = estim.fit_transform(mat_list)
       patt_mat = estim.components_
 
       errOG = computeError(curMat, patt_mat)
       print("Error for given image versus its pattern: " + str(errOG))
       i = 0
       #this loop goes through each class to pick for the versus
       while i < len(blockList):
 
          if '.png' in blockList[i]:
             #this will pick 20 random training images

             training_list = os.listdir('training_inverse/'+blockList[j][:4])
             l=0
             rand_train = []
             sum_err = 0
             #this will calculate average error
             while l < 20:
                randImg = loadImage('training_inverse/'+blockList[j][:4]+'/'+training_list[random.randint(0, len(training_list)-1)], 16)

                randMat = imageToMatrix(randImg, 16)
                curr_err = computeError(randMat, patt_mat)
                sum_err+=curr_err
                l+=1
             new_err = sum_err//20
             header_list.append(str(new_err))
             print("Error for " + blockList[i] + " image: " + str(new_err))
             i+=1
          else:
             i+=1
             continue
       writer.writerow(header_list)
       m+=1
       j+=1
  else:
    j+=1
    continue
f.close()
