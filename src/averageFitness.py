import MAFR
import os
import numpy as np
from sklearn import decomposition

DIRECTORYPATH = "/scratch/prism2022data/annotatedInverseDir/")
directoryList = os.listdir(DIRECTORYPATH)

for species in directoryList:
    print(species[:-1])
    path = DIRECTORYPATH + directory
    print(path)
