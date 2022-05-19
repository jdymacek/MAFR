import argparse
import sys
import os
import numpy as np
from MAFR import loadImage, imageToMatrix
from pip.internal import main

parser = argparse.ArgumentParser()
#takes name of the program

parser.add_argument('-d', metavar = 'input_directory', required=False, default ='here', help ='directory where patterns are located')

parser.add_argument('-p',  metavar = 'patterns', required=False, default =32, help = 'output_directory')

parser.add_argument('-b', metavar = 'block size', required=False, default =16, help = 'block size')

parser.add_argument('-o', metavar = 'name for pattern file', required=False, default ='this', help = 'state what name the output file for the patterns should be')

parser.add_argument('-f', required=False, default = 'foo', help = '')
arg = parser.parse_args()
print(arg)

dirPath = '//' + arg.d
file_list = os.listdir(dirPath)

M = np.array()
for filename in file_list:
     if filename.endswith(".png"):
        #looking for the patterns in each png file
        fname_path = os.path.join(dirPath, filename)
        img = loadImage(fname_path, int(arg.p))
        m = imageToMatrix(img, int(arg.b))
        #pattern filw should involve the objec file name given by -o
        #put the files in an output directory
        M+=m


