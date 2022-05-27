import MAFR
import numpy as np
import os
import argparse

def combine(pathA, pathB):
    matrixA = MAFR.loadMatrix(pathA)
    matrixB = MAFR.loadMatrix(pathB)
    return np.concatenate((matrixA, matrixB), axis=0)


pathA = ''
pathB = ''
output = ''

parser = argparse.ArgumentParser(description='Combine two pattern matrices.')
parser.add_argument('-a', metavar=pathA, type=str, help='Path to first pattern matrix.')
parser.add_argument('-b', metavar=pathB, type=str, help='Path to second pattern matrix.')
parser.add_argument('-o', metavar='output', type=str, help='Path to output file.')

print(pathA.shape)
print(pathB.shape)

combined = combine(pathA, pathB)
print(combined.shape)

aPatterns = MAFR.getPatterns(pathA)
bPatterns = MAFR.getPatterns(pathB)

p = aPatterns + bPatterns
MAFR.saveMatrix(combined, p, MAFR.MAFR.getBlocksize(pathA), MAFR.getSpecies(pathA), out=output)