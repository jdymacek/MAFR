#!/usr/bin/python3

import MAFR
import numpy as np
import os
import random
import math
from sklearn import decomposition

BLOCKSIZE = 16
PATTERNS = 16
PATH = "/scratch/prism2022data/annotatedInverseDir/"

classes = next(os.walk(PATH))[1]
classes = sorted(classes)

paths = {k:"" for k in classes}

for c in classes:
    paths[c] = PATH + c + "/" + c + "_bigAnnoatedInvBlock.png"

# open each big block as matrix:

matrices = {k:"" for k in classes}
for c in classes:
    matrices[c] = MAFR.imageToMatrix(MAFR.loadImage(paths[c], BLOCKSIZE), BLOCKSIZE)

annotation = []
ml = []
currentPatterns = {k:"" for k in classes}
model = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=10000, solver="mu")
for k,v in matrices.items():
    np.random.shuffle(v)
    population = v[:32]
    model.fit_transform(population)
    currentPatterns[k] = model.components_
    ml += [model.components_]
    for j in range(PATTERNS):
        annotation.append(k)

currentState = np.concatenate(ml)

initialTemp = 5
finalTemp = 0.1
alpha = 0.01
currentTemp = initialTemp

'''
bestScore = 0
bestPatterns = ""
'''
while(currentTemp > finalTemp):

    neighborPatterns = currentPatterns
    toChange = random.choice(classes)
    np.random.shuffle(matrices[toChange])
    newBlocks = matrices[toChange][:32]
    model.fit_transform(newBlocks)
    neighborPatterns[toChange] = model.components_

    ml = []
    for k,v in neighborPatterns.items():
        ml += [v]
    neighbor = np.concatenate(ml)

    currEstim = decomposition.NMF(n_components=PATTERNS*len(classes), init="random", random_state=0, max_iter=10000, solver="mu")
    currEstim.fit(matrices["AMRE"])
    currEstim.components_ = currentState

    total = 0
    for k,v in matrices.items():
        W = currEstim.transform(v)
        correct = k
        hits = {c:0 for c in classes}
        for block in W:
            percents = {c:0 for c in classes}
            block /= np.sum(block)
            for j in range(0, len(annotation)):
                percents[annotation[j]] += block[j]
            ss = [(x,y) for y,x in percents.items()]
            ss.sort(reverse=True)
            hits[ss[0][1]] += 1 
        total += hits[correct]
    currentScore = 1 - (total/(len(classes)*256))
    
    neighborEstim = decomposition.NMF(n_components=PATTERNS*len(classes), init="random", random_state=0, max_iter=10000, solver="mu")
    neighborEstim.fit(matrices["AMRE"])
    neighborEstim.components_ = neighbor

    neighborTotal = 0
    for k,v in matrices.items():
        W = neighborEstim.transform(v)
        correct = k
        hits = {c:0 for c in classes}
        for block in W:
            percents = {c:0 for c in classes}
            block /= np.sum(block)
            for j in range(0, len(annotation)):
                percents[annotation[j]] += block[j]
            ss = [(x,y) for y,x in percents.items()]
            ss.sort(reverse=True)
            hits[ss[0][1]] += 1 
        neighborTotal += hits[correct]
    neighborScore = 1 - (neighborTotal/(len(classes)*256))

    diff = neighborScore - currentScore
    diff *= 100
    print(f"CURR: {currentScore}\tNEIGHBOR: {neighborScore}\tTEMP: {currentTemp}")

    if diff < 0:
        currentState = neighbor
    else:
        if random.uniform(0,1) < math.exp(-diff/currentTemp):
            currentState = neighbor
    currentTemp -= alpha

MAFR.saveHitPatterns(solution, annotation, BLOCKSIZE)
	
