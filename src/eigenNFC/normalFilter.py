import eigenNFC
import MAFR
import argparse
import numpy as np
import os

parser = argparse.ArgumentParser()

parser = argparse.ArgumentParser()                         
parser.add_argument("-d", help="directory to classify")
parser.add_argument("-o", help="output")              
                                                           
args = parser.parse_args()                                 
tstDirectory = args.d
out = args.o

allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]

for f in allFiles:
	vector = eigenNFC.imageToVector(f)
	img = MAFR.loadImage(f, 16)
	M = MAFR.imageToMatrix(img, 16)  
	avg = 100/(np.average(vector))
	M = M.astype(np.float32)
	M *= avg
	img = MAFR.matrixToImage(M, 16, 16)
	img.save(out + "/" + f.split("/")[-2] + "/" + f.split("/")[-1])
