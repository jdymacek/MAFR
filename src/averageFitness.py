import MAFR
import os
import numpy as np
from sklearn import decomposition
import PIL

DIRECTORYPATH = "/scratch/prism2022data/annotatedInverseDir/"
PATTERNOUTPUT = "/scratch/prism2022data/averageFitnessPatterns/"
TRAINING = "/scratch/prism2022data/training_inverse/"

directoryList = os.listdir(DIRECTORYPATH)
for species in directoryList:
    print(species)
    path = DIRECTORYPATH + species
    if not path.endswith('/'):
      path = path + "/"

    subDirectory = os.listdir(path)
    img = MAFR.loadImage(path + subDirectory[0], 16)
    m = MAFR.imageToMatrix(img, 16)


    estim = decomposition.NMF(n_components=32, init="random", random_state=0, max_iter=10000, solver="mu")
    bestScore = 0
    best = ''
    for i in range(5):
      np.random.shuffle(m)
      population = m[:50]

      w = estim.fit_transform(population)
      h = estim.components_

      trainingList = os.listdir(TRAINING)
      selfTraining = TRAINING + species

      selfList = os.listdir(selfTraining)

      self = []
      for img in selfList:
        i = MAFR.loadImage(selfTraining + "/" + img, 16)
        self.append(i)

      trainingList.remove(species)
    
      others = []
      for s in trainingList:
        imgPath = TRAINING + s
        print(imgPath)
        temp = os.listdir(imgPath)
        for i in temp:
          image = MAFR.loadImage(imgPath + "/" + i, 16)
          others.append(image)
    
      print(len(others))
      selfAverage = MAFR.errorFromFiles(self, h)
      print(f"Self-Average: {selfAverage}")
      otherAverage = MAFR.errorFromFiles(others, h)
      print(f"Other-Average: {otherAverage}")
    
      score = otherAverage/selfAverage
      print(score)

      if score > bestScore:
        bestScore = score
        best = h

    MAFR.saveMatrix(best, 32, 16, species, out=PATTERNOUTPUT)
