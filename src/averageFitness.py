import MAFR
import os
import numpy as np
from sklearn import decomposition
import PIL

DIRECTORYPATH = "/scratch/prism2022data/annotatedInverseDir/"
PATTERNOUTPUT = "/scratch/prism2022data/averageFitnessPatterns/"
TRAINING = "/scratch/prism2022data/training/"

directoryList = os.listdir(DIRECTORYPATH)
for species in directoryList:
    path = DIRECTORYPATH + species
    if not path.endswith('/'):
      path = path + "/"

    subDirectory = os.listdir(path)
    img = MAFR.loadImage(path + subDirectory[0], 16)
    m = MAFR.imageToMatrix(img, 16)

    np.random.shuffle(m)
    population = m[:20]

    estim = decomposition.NMF(n_components=16, init="random", random_state=0, max_iter=10000, solver="mu")
    w = estim.fit_transform(population)
    h = estim.components_
    MAFR.saveMatrix(h, 16, 16, species, out=PATTERNOUTPUT)
    patterns = MAFR.matrixToImage(h, 1, len(h))
    patterns.save(species+"-AVERAGE-FITNESS.png")

    trainingList = os.listdir(TRAINING)
    selfTraining = TRAINING + species

    selfList = os.listdir(selfTraining)
    print(len(selfList))
    goodSum = 0
    for img in selfList:
      i = MAFR.loadImage(selfTraining + "/" + img, 16)
      matrix = MAFR.imageToMatrix(i, 16)
      e = MAFR.computeError(matrix, h)
      goodSum += e

    goodAverage = goodSum / len(selfList)
#print(f'GOODSUM: {goodSum} over {len(selfList)}')
    trainingList.remove(species)
    
    badSum = 0
    total = 0
    for s in trainingList:
      imgPath = TRAINING + species
      temp = os.listdir(imgPath)
      print(temp)
      for i in temp:
        image = MAFR.loadImage(imgPath + "/" + i, 16)
        matrix = MAFR.imageToMatrix(image, 16)
        badSum += MAFR.computeError(matrix, h)
        total += 1
    
    print(f'BADSUM: {badSum} over {total}')
    badAverage = badSum / total

#print(f"FOR {species}: GOOD AVERAGE = {goodAverage}\tBAD AVERAGE = {badAverage}\tTOTAL SCORE = {badAverage/goodAverage}")   
    
