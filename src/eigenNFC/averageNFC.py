import MAFR
import eigenNFC
import numpy as np
import PIL
from PIL import Image
import argparse
import os
from sklearn import decomposition
import time
import argparse
import math
import statistics

parser = argparse.ArgumentParser(description='Convert an image to a vector')
parser.add_argument('-t', help='training directory')

args = parser.parse_args()

tstDirectory = args.t

dirList = os.listdir(tstDirectory)
dirList.sort()
for spec in dirList:
  fileList = os.listdir(args.t+'/'+spec)
  #splitUp=np.array_split(fileList, math.sqrt(len(fileList)*15))
  splitUp=np.array_split(fileList, len(fileList)//2)

  groupNum=0
  for group in splitUp:
    print(len(group))
    imgList = []
    for img in group:
      loadedImg = MAFR.loadImage(args.t+'/'+spec+'/'+img,16)
      total = MAFR.imageToMatrix(loadedImg, 16).astype(np.float32)
      imgList.append(total)
      
    i =0
    newMat = imgList[0]
    while i < 256:
      j=0  

      while j < len(imgList):
        if j == 0:
          newMat[i] = 0

        newMat[i] += imgList[j][i]
        j+=1

      newMat[i]=newMat[i]//len(imgList)
      i+=1
    newImg = MAFR.matrixToImage(newMat, 16, 16)
    newImg.save("/scratch/prism2022data/data/average/"+spec+"/"+spec+"_averageImage"+str(groupNum)+".png")
    groupNum+=1

