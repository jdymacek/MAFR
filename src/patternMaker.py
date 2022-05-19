import argparse
import sys
import os
import numpy as np
from MAFR import loadImage, imageToMatrix, saveMatrix
from sklearn import decomposition
from PIL import Image

parser = argparse.ArgumentParser()
#takes name of the program

parser.add_argument('-d', metavar = 'input_directory', required=False, default ='here', help ='directory where patterns are located')

parser.add_argument('-p',  metavar = 'patterns', required=False, default =32, help = 'output_directory')

parser.add_argument('-b', metavar = 'block size', required=False, default =16, help = 'block size')

parser.add_argument('-o', metavar = 'output directory', required=False, help = 'state where the output file for the patterns should go')

parser.add_argument('-f', required=False, default = 'foo', help = '')

parser.add_argument('-s', help='species code for incoming data')

arg = parser.parse_args()
print(arg)


n_components = int(arg.p)

M = np.ndarray((1, int(arg.b)*int(arg.b)))
file_list = os.listdir(arg.d)
print(f'Initial bigM:\n{M}')

for filename in file_list:
     if filename.endswith(".png"):
        #looking for the patterns in each png file
        fname_path = arg.d + '/' + filename
        img = loadImage(fname_path, int(arg.b))
        m = imageToMatrix(img, int(arg.b))
        #pattern filw should involve the objec file name given by -o
        #put the files in an output directory
        np.concatenate((M, m), axis=0)

print(f'bigM after concatenation:\n {M}')
estim = decomposition.NMF(n_components=n_components, init='random', random_state=0, max_iter=4000)
w = estim.fit_transform(m)
h = estim.components_
saveMatrix(h, arg.p, arg.b, arg.s, arg.d, out=)
pattern_img = matrixToImage(h,1,len(h))
pattern_img.save('patterns.png')





