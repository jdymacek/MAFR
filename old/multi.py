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

def norm(matrix, w, h):
  prod = np.matmul(w,h)
  return matrix - prod


blockSize = 16

src_img = Image.open('warbler-1.png')
src_img = ImageOps.grayscale(src_img)
src_img = src_img.resize(((src_img.width//blockSize)*blockSize,(src_img.height//blockSize)*blockSize))
print(src_img.size)

img_two = Image.open('warbler-2.png')
img_two = ImageOps.grayscale(img_two)
img_two = img_two.resize(((img_two.width//blockSize)*blockSize,(img_two.height//blockSize)*blockSize))

#auw_img = Image.open('images/auwaaz.png')
#auw_img = ImageOps.grayscale(auw_img)


#recon_img = Image.open('images/cmwany11.png')
#recon_img = ImageOps.grayscale(recon_img)
#recon_img = recon_img.resize(((recon_img.width//blockSize)*blockSize,(recon_img.height//blockSize)*blockSize))

tile_matrix = imageToMatrix(src_img,blockSize)

matrix_two = imageToMatrix(img_two,blockSize)
#auw_matrix = imageToMatrix(auw_img,blockSize)

#recon_matrix = np.array(recon_img)

#tile_matrix = np.concatenate((tile_matrix,oven_matrix))
#tile_matrix = np.concatenate((tile_matrix,auw_matrix))

#print(tile_matrix)

#n_samples, n_features = tile_matrix.shape
#print('Samples: ' + str(n_samples))
#print('Features: ' + str(n_features))

n_components = 32

print("TRAINING SET: EXTRACTING THE TOP %d %s..." % (n_components, 'Non-negative components - NMF'))
#t0 = time()
estim = decomposition.NMF(n_components=n_components, init='random', random_state=0, max_iter=4000)
#w = estim.fit_transform(tile_matrix)
w1 = estim.fit_transform(tile_matrix)
h1 = estim.components_
print(f'H1: {h1}')
print(f'W1 ERROR: {estim.reconstruction_err_}')
#w2 = estim.transform(matrix_two)
#h2 = estim.components_
#print(f'H2: {h2}')
#print(f'W2 ERROR: {estim.reconstruction_err_}')

#if h1.all() == h2.all():
#  print("H is the same")

inverse_h = np.linalg.pinv(h1)
#print(np.matmul(inverse_h, h1))

w3 = np.matmul(matrix_two, inverse_h)
#err = norm(tile_matrix, w3, h1)
#total = 0.0
#for val in err:
#	for j in val:
#		total += j

#print(f"Error from new w: {total}")

if w3.all() == w1.all():
  print("The same W")
else:
  print("W's are not equal")


#This is for three images.
#w3 = estim.transform(auw_matrix)
#h3 = estim.components_
#print(f'H3: {h3}')
#print(f'W3 ERROR: {estim.reconstruction_err_}')

#h = estim.components_
#train_time = (time() - t0)

#print("Finished in %0.3fs" % train_time)
#print(f'ERROR: {estim.reconstruction_err_}')

#r_matrix = estim.inverse_transform(w2)
r_matrix = np.matmul(w3, h1);

#print(recon)

#print(r_matrix)

result_img = matrixToImage(r_matrix,src_img.width//blockSize, src_img.height//blockSize)
#result_img = Image.fromarray(test_recon)
#result_img = result_img.convert('L')
result_img.save("recon.png")

pattern_img = matrixToImage(h1,1, len(h1))
pattern_img.save("patterns.png")

#print(h1)

