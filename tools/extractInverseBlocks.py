import argparse
import os
import random
import numpy as np
from MAFR import imageToMatrix, matrixToImage, loadImage, closestDivisor
from PIL import Image


#random blocks for given number
def randBlocks(txtFile, numBlocks):
  paddedBlock = []
  j=0
  dirList = os.listdir('training_inverse')

  while j<int(numBlocks):
        randDir = dirList[random.randint(0, len(dirList)-1)]
        randDir_list = os.listdir('training_inverse/' +randDir)
        randPath = 'training_inverse/' +randDir+'/'+randDir_list[random.randint(0, len(randDir_list)-1)]

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
  paddedImg.save("randomInvBigBlock.png")
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
#now line is being parsed so now we have to match the file in lineParsed[0] 

      theBlock = int(lineParsed[len(lineParsed)-1])
      inverseList = os.listdir("//scratch//prism2022data//training_inverse//" + birdClass)
      for inv in inverseList:
          if inv[:37] in lineParsed[0]:
             imgLoaded = loadImage("/scratch/prism2022data/training_inverse/" + birdClass + '/' +inv, 256)
             matImg = imageToMatrix(imgLoaded, 16)
             row = matImg[theBlock]
             loopVar += 1
             allAnn +=[row]

  h = closestDivisor(len(allAnn))
  w = len(allAnn)//h
  bigImg = matrixToImage(allAnn, w, h)
  bigImg.save("annotatedInverseDir/" + birdClass + "/" + birdClass +"_bigAnnoatedInvBlock.png")



#extract blocks from images
def allclassblocks(txtFile, dirName):
  file_list = os.listdir(dirName)
  M = []
  annCounter=0
  for filename in file_list:
      with open(txtFile) as temp_f:
          datafile = temp_f.readlines()
      for line in datafile:
          if filename[:37] in line:
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
  bigImg.save("allInvBlockSignals.png")



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
randBlocks(args.t, args.n)

#might have to slightly tweak if we will redo this with inverse patterns,
  #wherever you see training, just add '_inverse'
  #for searching through the .txt file, we need to take off the 'inverse.png' part for when checking if that file
  #largest file names are 54 characters, so that may have to be cutoff point, line[:54]
