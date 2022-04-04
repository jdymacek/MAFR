#simple -- v2 of split
#split.py

import sys
import math
import numpy as np
from PIL import Image
from PIL import ImageOps

from time import time
from sklearn import decomposition
from skimage import color, io, img_as_ubyte


#TODO:
#Append new tiles to matrix
#Run NMF
#Reconstruct separate image with computed patterns


def imageToMatrix(image, size):
	tiles = []
	result = []
	for y in range(image.height//size):
		for x in range(image.width//size):
			tile = image.crop((x*size,y*size, (x+1)*size, (y+1)*size))
			tiles.append(tile)

	for i in range(len(tiles)):
		a = np.asarray(tiles[i])
		a = a.flatten()
		result.append(a)
	return np.array(result)

def matrixToImage(tiles, width, height):

	size = int(math.sqrt(len(tiles[0])))
	result = Image.new('L', (width*size, height*size))

	index = 0
	for y in range(height):
		for x in range(width):
			tile = tiles[index]

			tile = tile/np.max(tile)
			tile = tile*255

			tile = np.clip(np.rint(tile),a_min=0, a_max=255)
			tile = tile.astype(np.uint8)

			img = Image.fromarray(tile.reshape(size,size), mode="L")
			result.paste(img, (x*size, y*size, (x+1)*size, (y+1)*size))
			index += 1

	return result 

blockSize = 32

src_img = Image.open('spectrogram.png')
src_img = ImageOps.grayscale(src_img)
src_img = src_img.resize(((src_img.width//blockSize)*blockSize,(src_img.height//blockSize)*blockSize))
print(src_img.size)

oven_img = Image.open('oven.png')
oven_img = ImageOps.grayscale(oven_img)
oven_img = oven_img.resize(((oven_img.width//blockSize)*blockSize,(oven_img.height//blockSize)*blockSize))

auw_img = Image.open('auwaaz.png')
auw_img = ImageOps.grayscale(auw_img)


recon_img = Image.open('cmwany11.png')
recon_img = ImageOps.grayscale(recon_img)
recon_img = recon_img.resize(((recon_img.width//blockSize)*blockSize,(recon_img.height//blockSize)*blockSize))

tile_matrix = imageToMatrix(src_img,blockSize)

oven_matrix = imageToMatrix(oven_img,blockSize)
auw_matrix = imageToMatrix(auw_img,blockSize)

recon_matrix = np.array(recon_img)

tile_matrix = np.concatenate((tile_matrix,oven_matrix))
tile_matrix = np.concatenate((tile_matrix,auw_matrix))

print(tile_matrix)

#n_samples, n_features = tile_matrix.shape
#print('Samples: ' + str(n_samples))
#print('Features: ' + str(n_features))

n_components = 32

print("TRAINING SET: EXTRACTING THE TOP %d %s..." % (n_components, 'Non-negative components - NMF'))
#t0 = time()
estim = decomposition.NMF(n_components=n_components, init='random', random_state=0, max_iter=4000)
w = estim.fit_transform(tile_matrix)
h = estim.components_
#train_time = (time() - t0)

#print("Finished in %0.3fs" % train_time)
print(f'ERROR: {estim.reconstruction_err_}')

print("TEST IMAGE: GETTING W...")
estim2 = decomposition.NMF(n_components=n_components, init='random', random_state=0, max_iter=4000)
w2 = estim.fit_transform(recon_matrix)

r_matrix = estim.inverse_transform(w)

test_recon = np.matmul(w2,h)

#print(recon)

print(r_matrix)

#result_img = matrixToImage(test_recon,src_img.width//blockSize, src_img.height//blockSize)
result_img = Image.fromarray(test_recon)
result_img = result_img.convert('L')
result_img.save("recon.jpg")

pattern_img = matrixToImage(h,1, len(h))
pattern_img.save("patterns.png")

print(h)
