import os
import numpy as np
from MAFR import loadImage,imageToMatrix, computeError, saveMatrix, errorFromFiles, loadMatrix
import random
import argparse
from sklearn import decomposition
import csv
import statistics

#Dionna's version of calculating fitness scores
#this takes in the given speceis big annotated bloc and tries to find the lowest error for its own with it having
#the highest error on the other speceis
#it outputs the best pattern into a file
parser = argparse.ArgumentParser()
parser.add_argument('-s', metavar = 'class')
arg = parser.parse_args()

cwd = os.getcwd()
blockList = os.listdir(cwd+'/bigBlockClasses')

j=0
overallList = []
bestPattern = decomposition.NMF(n_components=16, init='random', random_state=0, max_iter=10000, solver='mu')
while j < len(blockList):
  if arg.s in blockList[j]:
     l=0
     while l < 10:
       print(l)
       errList = []
       curImg = loadImage(cwd+'/bigBlockClasses/'+blockList[j], 16)
       curMat = imageToMatrix(curImg, 16)
       mat_list = []
       k=0
       while k < 20:
         random_row = curMat[random.randint(0, 255)]
         mat_list.append(random_row)
         k+=1
     
       estim = decomposition.NMF(n_components=16, init='random', random_state=0, max_iter=10000, solver='mu')
       w_mat = estim.fit_transform(mat_list)
       patt_mat = estim.components_

#this might be the point where you compute the error of like 20 training versus the bigBlockNMF
#after averiging error, put it in that list that has error for each class
#after every iteration, replace previous one if its extremes are more extreme than the last one
       train_list = os.listdir('training_inverse')
       train_list.sort()
       for classDir in train_list:
          sum_err=0
          curr_err=0

          m=0
          randList=[]
          fileList = os.listdir('training_inverse/'+classDir)
          while m < 20:
            randList.append(0)
            randList[m] = fileList[random.randint(0, len(fileList)-1)]
            m+=1

          n=0
          imgList=[]
          while n <20:
            imgList.append(0)
            randImg = loadImage('training_inverse/'+classDir+'/'+randList[n], 16)
#randMat = imageToMatrix(randImg, 16)
            imgList[n] = randImg
            n+=1

          newErr = errorFromFiles(imgList, patt_mat)
          errList.append(newErr)

       print("Current Best: " + str(overallList))
       print("Current Contender: " + str(errList))
       if l>0:
          r=0
          classIndex=0
          best_score=0
          curr_score=0
          while r < len(overallList):
            if arg.s== 'AMRE':
              classIndex=0
            elif arg.s== 'BBWA':
              classIndex=1
            elif arg.s == 'BTBW':
              classIndex=2
            elif arg.s == 'CAWA':
              classIndex=3
            elif arg.s == 'COYE':
              classIndex=4
            elif arg.s == 'MOWA':
              classIndex=5
            elif arg.s == 'OVEN':
              classIndex=6

            if classIndex == r:
	      #needs to be less strict here
              q=0
              curr_higher=0
              overall_higher=0
              while q < len(errList):
                if errList[r] >= errList[q]:
                  curr_higher+=1
                if overallList[r] >= overallList[q]:
                  overall_higher+=1
                q+=1

                best_score+=overall_higher
                curr_score+=curr_higher


            else:
              if errList[r] >= overallList[r]:
                 curr_score+=1

            r+=1
#gold scores, higher score = worser
          if curr_score <= best_score:
             overallList = errList
             bestPattern = patt_mat

          print("Best so far score: " + str(best_score))
          print("Current contender score: " + str(curr_score))
       else:
          overallList = errList
          bestPattern = patt_mat

       l+=1

     j+=1
  else:
     j+=1
     continue
print("Here is the best errors for " +arg.s)
print(overallList)
saveMatrix(bestPattern, 16, 16, arg.s)
