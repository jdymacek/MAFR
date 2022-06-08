#!/usr/bin/python3

import MAFR
import numpy as np
import os
from sklearn import decomposition

AMRE_PATH = "/scratch/prism2022data/annotatedInverseDir/AMRE/AMRE_bigAnnoatedInvBlock.png"
BBWA_PATH = "/scratch/prism2022data/annotatedInverseDir/BBWA/BBWA_bigAnnoatedInvBlock.png"
BTBW_PATH = "/scratch/prism2022data/annotatedInverseDir/BTBW/BTBW_bigAnnoatedInvBlock.png"
COYE_PATH = "/scratch/prism2022data/annotatedInverseDir/COYE/COYE_bigAnnoatedInvBlock.png"
OVEN_PATH = "/scratch/prism2022data/annotatedInverseDir/OVEN/OVEN_bigAnnoatedInvBlock.png"
BLOCKSIZE = 16
PATTERNS = 16
# open each big block as matrix:

redstartImg = MAFR.loadImage(AMRE_PATH, BLOCKSIZE)
bayImg = MAFR.loadImage(BBWA_PATH, BLOCKSIZE)
blackthroatImg = MAFR.loadImage(BTBW_PATH, BLOCKSIZE)
yellowthroatImg = MAFR.loadImage(COYE_PATH, BLOCKSIZE)
ovenImg = MAFR.loadImage(OVEN_PATH, BLOCKSIZE)

matrices = []
redstartMatrix = MAFR.imageToMatrix(redstartImg, BLOCKSIZE)
matrices.append(redstartMatrix)
bayMatrix = MAFR.imageToMatrix(bayImg, BLOCKSIZE)
matrices.append(bayMatrix)
blackthroatMatrix = MAFR.imageToMatrix(blackthroatImg, BLOCKSIZE)
matrices.append(blackthroatMatrix)
yellowthroatMatrix = MAFR.imageToMatrix(yellowthroatImg, BLOCKSIZE)
matrices.append(yellowthroatMatrix)
ovenMatrix = MAFR.imageToMatrix(ovenImg, BLOCKSIZE)
matrices.append(ovenMatrix)

classes = ["AMRE", "BBWA", "BTBW", "COYE", "OVEN"]
bestScore = 0
bestPatterns = ""
for i in range(100):
    annotation = []
    #randomly take 50 rows of each matrix
    ml = []
    model = decomposition.NMF(n_components=PATTERNS, init="random", random_state=0, max_iter=10000, solver="mu")
    for i, m in enumerate(matrices):
        np.random.shuffle(m)
        population = m[:32]
        model.fit_transform(population)
        ml += [model.components_]
        for j in range(PATTERNS):
            annotation.append(classes[i])
    patterns = np.concatenate(ml)

    # test set of patterns against each block in each bigBlock
    # assess fitness based on hitrate

    model = decomposition.NMF(n_components=PATTERNS*len(classes), init="random", random_state=0, max_iter=10000, solver="mu")
    model.fit(matrices[0])
    model.components_ = patterns

    total = 0
    for i, m in enumerate(matrices):
        W = model.transform(m)
        correct = classes[i]
        hits = {k:0 for k in classes}
        for block in W:
            percents = {k:0 for k in classes}
            block /= np.sum(block)
            for j in range(0, len(annotation)):
                percents[annotation[j]] += block[j]
            ss = [(x,y) for y,x in percents.items()]
            ss.sort(reverse=True)
            hits[ss[0][1]] += 1 
        total += hits[correct]
    print(total/(len(classes)*256))
    
    if total/(len(classes)*256) > bestScore:
        bestScore = total/(len(classes)*256)
        best = patterns


MAFR.saveHitPatterns(best, annotation, BLOCKSIZE)
	

	






