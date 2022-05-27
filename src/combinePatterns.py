import MAFR
import numpy as np
import os
import argparse

def combine(pathA, pathB):
    matrixA = MAFR.loadMatrix(pathA)
    matrixB = MAFR.loadMatrix(pathB)
    print(matrixA.shape)
    print(matrixB.shape)
    return np.concatenate((matrixA, matrixB), axis=0)



parser = argparse.ArgumentParser(description='Combine two pattern matrices.')
parser.add_argument('-a', type=str, help='Path to first pattern matrix.')
parser.add_argument('-b', type=str, help='Path to second pattern matrix.')
parser.add_argument('-o', type=str, help='Path to output file.')
#parser.add_argument('-s', type=str, help = 'Species Code')

args = parser.parse_args()

pathA = args.a
pathB = args.b
output = args.o

combined = combine(pathA, pathB)
print(combined.shape)

aPatterns = MAFR.getPatterns(pathA)
bPatterns = MAFR.getPatterns(pathB)

p = aPatterns + bPatterns
MAFR.saveMatrix(combined, p, MAFR.getBlocksize(pathA), MAFR.getSpecies(pathA), out=output)
