import MAFR
import argparse
import os
import numpy as np
import time
import operator

''' 
TODO:
    - load in all pattern files
    - calculate the pseudo inverse of each pattern
    - store in dictionary where key is species, and value is list of two-tuples (patterns, pseudo-inverse)
    - grab one random pair per species in dictionary
    - for all training images
        - for all patterns in list
            - calculate error and store in list of tuples, (species, error)

    - sort list of tuples by error
    - print species of winner

    - want to see how long it takes to run after loading all files 
'''

parser = argparse.ArgumentParser(description='Smart(ish) Classifier')
parser.add_argument('-d', help='directory of desired .nmf pattern files') #patterns
parser.add_argument('-f', help='path to training set') #file to be tested

args = parser.parse_args()

directory = args.d
trainingDir = args.f

patterns = os.listdir(directory)
speciesDict = {}
for p in patterns:
    if p.endswith('.nmf'):
        path = directory + '/' + p
        m = MAFR.loadMatrix(path)
        pInv = np.linalg.pinv(m)
        s = MAFR.getSpecies(path)
        t = (m, pInv, s)
        if s not in speciesDict:
            speciesDict[s] = [t]
        else:
            speciesDict[s].append(t)

t0 = time()
curated = {}

for key in speciesDict:
    curated[key] = speciesDict[key][np.random.randint(len(speciesDict[key]))]

training = os.listdir(trainingDir)

errors = []
for d in training:
    path = trainingDir + '/' + d
    images = os.listdir(path)
    for i in images:
        if i.endswith('.png'):
            img = MAFR.loadImage(path + '/' + i)
            original = MAFR.imageToMatrix(img)
            for key in curated:
                m = curated[key][0]
                pInv = curated[key][1]
                s = curated[key][2]
                error = MAFR.quickError(original, m, pInv)
                errors.append((s, error))

errors.sort(key=operator.itemgetter(1))
print(errors[0][0])
print(f'TIME: {time() - t0}')
    
