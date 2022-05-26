from calendar import c
import MAFR
import argparse
import os
import numpy as np
import time
import operator

parser = argparse.ArgumentParser(description='Faster Error Computation')
parser.add_argument('-t', '--training', help='Path to training images', required=True)
parser.add_argument('-d', '--directory', help='Path to .nmf files', required=True)

args = parser.parse_args()

directory = args.directory
trainingDir = args.training

patterns = os.listdir(directory)
speciesDict = {}
counter = 0

for p in patterns:
    if p.endswith('.nmf'):
        filename = p
        idNum = str(counter).zfill(2)
        path = directory + '/' + p
        m = MAFR.loadMatrix(path)
        pInv = np.linalg.pinv(m)
        s = MAFR.getSpecies(path)
        idVal = s + '-' + idNum
        t = (m, pInv, s, filename, [])
        if s not in speciesDict:
            speciesDict[s] = [t]
        else:
            speciesDict[s].append(t)

speciesDirs = os.listdir(trainingDir)
correct =  0
total = 0

'''
for p in patterns:
    for d in speciesDirs:
        path = trainingDir + '/' + d
        images = os.listdir(path)
        for i in images:
            if i.endswith('.png'):
                img = MAFR.loadImage(path + '/' + i, 16)
                original = MAFR.imageToMatrix(img, 16)
                for key in speciesDict:
                    m = speciesDict[key][0][0]
                    pInv = speciesDict[key][0][1]
                    s = speciesDict[key][0][2]
                    filename = speciesDict[key][0][3]
                    error = MAFR.quickError(original, m, pInv)
                    errors.append((s, error, filename))

            errors.sort(key=operator.itemgetter(1))

            if errors[0][0] == d:
                correct += 1
            total += 1

    print(f'{correct} right out of {total}')
    print(f'{correct/total} percent')
'''

errors = {}
for k, v in speciesDict.items():
    for p in v:
        for d in speciesDirs:
            path = trainingDir + '/' + d
            images = os.listdir(path)
            for i in images:
                if i.endswith('.png'):
                    img = MAFR.loadImage(path + '/' + i, 16)
                    original = MAFR.imageToMatrix(img, 16)
                    error = MAFR.quickError(original, p[0], p[1])
                    p[4].append(error)
                    temp = {p[3]: error}
                    imgKey = d + '/' + i
                    errors[imgKey] += temp
            
                 

