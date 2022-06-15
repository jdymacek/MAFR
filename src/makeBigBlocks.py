import csv
import numpy as np
import random
import MAFR

annotationFile = "/scratch/prism2022data/data/reducedNoise/annotations.txt"
outDir = "/scratch/prism2022data/data/reducedNoise/bigBlocks"
srcDir = "/scratch/prism2022data/data/reducedNoise/training/"

annotations = []
with open(annotationFile) as csvFile:
	aFile = csv.reader(csvFile,delimiter = "\t")
	for line in aFile:
		annotations += [(line[0],int(y)) for y in line[1:] if y != ""]


classes = ["AMRE","BBWA","BTBW","COYE","OVEN"]
#classes = ["BBWA"]

for species in classes:
	bigblocks = []
	files = list(filter(lambda x: species in x[0], annotations))
	random.shuffle(files)
	blocks = []
	if len(files) < 256:
		blocks = files
		blocks += random.choices(files,k = 256-(len(files)))
#		print(len(blocks))
	else:
		blocks = files[:256]
	blocks.sort()

#	print(blocks)
#	quit()

	mat = ""
	openblock = ""
	
	for f,index in blocks:
		if f != openblock:
			openblock = f
			mat = MAFR.imageToMatrix(MAFR.loadImage(srcDir+openblock,16),16)
		bigblocks += [[mat[index, :]]]

	M = np.concatenate(bigblocks)
	img = MAFR.matrixToImage(M, 16,16)
	img.save(outDir+"/"+species+"/"+species+"_annotatedBlock.png")

			

