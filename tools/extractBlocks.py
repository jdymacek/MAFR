#extractBlocks -- has multiple functions: finds all the annotated blocks in the given directory from a .txt file, creates an image from a given number of blocks collected from all the class directories, and creates an image from a given number of annotated blocks inside the given class directory

import argparse
import os
import random
import numpy as np
from MAFR import imageToMatrix, matrixToImage, loadImage, closestDivisor
from PIL import Image


#random blocks for given number
def randBlocks(txtFile):
  paddedBlock = []
  j=0
#training = blank
  dirList = os.listdir('training')

  while j<int(args.n):
        randDir = dirList[random.randint(0, len(dirList)-1)]
        randDir_list = os.listdir('training/' +randDir)
        randPath = 'training/' +randDir+'/'+randDir_list[random.randint(0, len(randDir_list)-1)]

        with open(txtFile) as temp_f:
          datafile = temp_f.readlines()

        for line in datafile:
            if randPath in line:
               continue

        randImgL = loadImage(randPath, 256)
        randImgMat = imageToMatrix(randImgL, 16)
        takenBlock = randImgMat[random.randint(0, 255)]
        paddedBlock += [takenBlock]
        j+=1

  h = closestDivisor(len(paddedBlock))
  w = len(paddedBlock)//h
  paddedImg =  matrixToImage(paddedBlock, w, h)
  paddedImg.save("randomBigBlock.png")
#end



#specified number of annoatated blocks into one image
def classSpec(txtFile, numBlks, birdClass):
  allAnn = []
  with open(txtFile) as temp_f:
    datafile = temp_f.readlines()

  classCount =0
  classList = []
  for line in datafile:
     if birdClass in line:
        classCount+=1
        classList.append(line)

  while len(classList) < int(numBlks):
     classList = classList+classList


  loopVar =0
  while loopVar < int(numBlks):
      line = classList[random.randint(0, len(classList)-1)]
      lineParsed = line.split()
      if len(lineParsed) <2:
         continue

      theBlock = int(lineParsed[len(lineParsed)-1])
      imgLoaded = loadImage(lineParsed[0], 256)
      matImg = imageToMatrix(imgLoaded, 16)
      row = matImg[theBlock]
      loopVar += 1
      allAnn +=[row]

  h = closestDivisor(len(allAnn))
  w = len(allAnn)//h
  bigImg = matrixToImage(allAnn, w, h)
  bigImg.save("annotatedDir/" + birdClass + "/" + birdClass +"_bigAnnoatedBlock.png")
#end




#extract blocks from images
def allclassblocks(txtFile, dirName):
  file_list = os.listdir(dirName)
  M = []
  annCounter=0
  for filename in file_list:
      with open(txtFile) as temp_f:
          datafile = temp_f.readlines()
      for line in datafile:
          if filename in line:
             annCounter+=1
             lineParsed = line.split()
             i=1
             while i < len(lineParsed):
                 #get the blocks from the image
                 theBlock = int(lineParsed[i])

                 #convert image to matrix
                 imgLoaded = loadImage(dirName+'/'+filename, 256)
                 matImg = imageToMatrix(imgLoaded, 16)

                 #now with the block, find the part of the matrix that matches
                 row = matImg[theBlock]
                 i += 1
                 M += [row]


  h = closestDivisor(len(M))
  w = len(M)//h
  bigImg = matrixToImage(M, w, h)
  bigImg.save("allBlockSignals.png")



#arguments  
parser = argparse.ArgumentParser()
parser.add_argument('-d', metavar = 'input_directory', help='directory where pngs are located')
parser.add_argument('-t', metavar = '.txt file', help = 'file that has all the blocks containing pngs with their retrospective png')
parser.add_argument('-c', metavar = 'class', help = 'class for creating big annotate block images')
parser.add_argument('-n', metavar = 'number of blocks', help = 'number of blocks to be pulled from directory')
args = parser.parse_args()


#now we call the functions down here 
#allclassblocks(args.t, args.d)
#classSpec(args.t, args.n, args.c)
#randBlocks(args.t)

#might have to slightly tweak if we will redo this with inverse patterns, 
  #wherever you see training, just add '_inverse'
  #for searching through the .txt file, we need to take off the 'inverse.png' part for when checking if that file
