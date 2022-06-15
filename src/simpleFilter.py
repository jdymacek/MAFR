import MAFR
import argparse
import numpy as np
import os
import operator
import PIL
from sklearn import decomposition
np.set_printoptions(threshold=np.inf)

parser = argparse.ArgumentParser("Use Classifier for NFC Classification")
parser.add_argument("-t", help="training directory", required=True)

args = parser.parse_args()


tstDirectory = args.t

tstClasses   = next(os.walk(tstDirectory))[1]
allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png")]

tokens = tstDirectory.split("/")
outPath = "/scratch/prism2022data/reducedNoise/" + tokens[-1]

blocksize=16
for f in allFiles:
  fileTkns = f.split("/")
  c = fileTkns[-2]
  fn = fileTkns[-1]
  outPath += "/" + c + "/" + fn

  img = MAFR.loadImage(f, blocksize)
  m = MAFR.imageToMatrix(img, blocksize)
  #split into three columns
  
  for i in range(0,16):  
    firstThird = m[i*16:(i*16)+5]
    noiseAvg = [(sum(col)//len(col)) for col in zip(*firstThird)]
    for j in range(i*16, (i+1)*16):
      m[j] = list(map(lambda x,y: 0 if y>x else min((x-y)*3,255) , m[j], noiseAvg))
#print(m) 
  print(f)
  newM = MAFR.matrixToImage(m,blocksize, blocksize) 
  newM.save(outPath)  
  outPath = "/scratch/prism2022data/reducedNoise/" + tokens[-1]
quit()  
    
    



#start here








confusion = { x : {y: 0 for y in tstClasses} for x in tstClasses }

for f in allFiles:
	img = MAFR.loadImage(f, 16)
	mat = MAFR.imageToMatrix(img, 16)
	W = model.transform(mat)

	hits = {k : 0 for k in tstClasses}
	

	for block in W:
		percents = {k : 0 for k in tstClasses}
		idx = np.argmax(block)
		hits[annotation[idx]] += 1
		
		block = block/ np.sum(block)
		for i in range(0,len(annotation)):
			percents[annotation[i]] += block[i]
		ss = [(x,y) for y,x in percents.items()]
		ss.sort(reverse=True)
		print(ss)


	predicted = max(hits, key=hits.get)
	confusion[predicted][ os.path.basename(os.path.dirname(f))] += 1
	print(f)

print(confusion)

