import MAFR
import numpy as np
import argparse

parser = argparse.ArgumentParser("Test to see if pseudoinverse ever contains a negative value")
parser.add_argument("-f", type=str, help=".nmf pattern file to test")

args = parser.parse_args()

file = args.f

m = MAFR.loadMatrix(file)

pInv = np.linalg.pinv(m)

print(type(pInv))
