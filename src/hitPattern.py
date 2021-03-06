#!/usr/bin/python3

import MAFR
import numpy as np
import os
import random
import math
from sklearn import decomposition
import argparse


BLOCKSIZE = 16
PATTERNS = 40
SAMPLES = 3*PATTERNS
PATH = "/scratch/prism2022data/data/"

parser = argparse.ArgumentParser()
parser.add_argument('-d', help='directory')
args = parser.parse_args()

PATH+=args.d

classes = MAFR.getClasses(PATH+'/bigBlocks')

paths = {k: PATH+'/bigBlocks/'+k+'/'+k+'_annotatedBlock.png' for k in classes}
# open each big block as matrix:

matrices = {m: MAFR.imageToMatrix(MAFR.loadImage(paths[m], BLOCKSIZE), BLOCKSIZE) for m in classes}

currEstim = decomposition.NMF(n_components=PATTERNS*len(classes), init="random", random_state=0, max_iter=10000, solver="mu")
currEstim.fit(matrices["AMRE"])

annotation = []
ml = []

rows = {x:random.sample(range(0,256), SAMPLES) for x in classes}

currentPatterns = {k:"" for k in classes}
model = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=10000, solver="mu")
for k,v in matrices.items():
    #np.random.shuffle(v)
    #population = v[:PATTERNS*2]
    ll = [[v[x]] for x in rows[k]]
#print(ll)
    population = np.concatenate(ll)
    model.fit_transform(population)
    currentPatterns[k] = model.components_
    ml += [model.components_]
    for j in range(PATTERNS):
        annotation.append(k)

def calcScore(state):
    currEstim.components_ = state

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
        print(hits)
        total += hits[correct]
    currentScore = 1 - (total/(len(classes)*256))
    return currentScore * 100


currentState = np.concatenate(ml)
currentScore = calcScore(currentState)
solution = currentState
solutionScore = currentScore

initialTemp = 20
finalTemp = 0.1
alpha = 0.1
currentTemp = initialTemp

while(currentTemp > finalTemp):

    changeVal = SAMPLES//2
    neighborPatterns = currentPatterns
    toChange = random.choice(classes)
    random.shuffle(rows[toChange])
    rows[toChange] = rows[toChange][changeVal:]
    while len(rows[toChange]) < SAMPLES:
        r = random.randint(0,255)
        if r not in rows[toChange]:
            rows[toChange].append(r)
    #np.random.shuffle(matrices[toChange])
    #rows[toChange] = random.sample(range(0,256), 2*PATTERNS)
    newBlocks = matrices[toChange][rows[toChange]]
    model.fit_transform(newBlocks)
    neighborPatterns[toChange] = model.components_

    ml = []
    for k,v in neighborPatterns.items():
        ml += [v]
    neighbor = np.concatenate(ml)

    
    neighborScore = calcScore(neighbor)

    diff = neighborScore - currentScore

    print(f"CURR: {currentScore}\tNEIGHBOR: {neighborScore}\tTEMP: {currentTemp}")

    if diff < 0:
        currentState = neighbor
        currentScore = neighborScore
        currentPatterns = neighborPatterns
    else:
        if random.uniform(0,1) < math.exp(-diff/currentTemp):
            currentState = neighbor
            currentScore = neighborScore
            currentPatterns = neighborPatterns

    if currentScore < solutionScore:
        solution = currentState
        solutionScore = currentScore
    currentTemp -= alpha

MAFR.saveHitPatterns(solution, annotation, BLOCKSIZE)
	
