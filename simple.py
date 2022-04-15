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

blockSize = 48

src_img = Image.open('spectrogram.png')
src_img = ImageOps.grayscale(src_img)
src_img = src_img.resize(((src_img.width//blockSize)*blockSize,(src_img.height//blockSize)*blockSize))
print(src_img.size)


tile_matrix = imageToMatrix(src_img,blockSize)
print(tile_matrix)


#n_samples, n_features = tile_matrix.shape
#print('Samples: ' + str(n_samples))
#print('Features: ' + str(n_features))

n_components = 10

print("EXTRACTING THE TOP %d %s..." % (n_components, 'Non-negative components - NMF'))
#t0 = time()
estim = decomposition.NMF(n_components=n_components, init='random', random_state=0, max_iter=4000)
w = estim.fit_transform(tile_matrix)
#train_time = (time() - t0)

#print("Finished in %0.3fs" % train_time)
print(f'ERROR: {estim.reconstruction_err_}')

h = estim.components_
r_matrix = estim.inverse_transform(w)

#print(recon)

print(r_matrix)

result_img = matrixToImage(r_matrix,src_img.width//blockSize, src_img.height//blockSize)
result_img.save("recon.png")

pattern_img = matrixToImage(h,1, len(h))
pattern_img.save("patterns.png")

print(h)
