#MAFR.py --- Magnificent Frigatebird NFC Module

import sys
import struct
import math
import numpy as np
from PIL import Image
from PIL import ImageOps

from time import time
from sklearn import decomposition
from skimage import color, io, img_as_ubyte
import array

def loadImage(filename, size):
  img = Image.open(filename)
  x_n = img.width // size
  x_diff = (img.width - x_n) // 2
  y_n = img.height // size

  cropped = img.crop((x_diff, 0, x_diff + (size * x_n), size * y_n))

  return cropped

### images -- PIL image file, size -- height and width of blocks
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

### tiles -- matrix, width + height -- dimensions for output image
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

def saveMatrix(matrix, patterns, block_size, bytes_per_entry, dirname):

  header = np.ndarray(8, dtype=np.uint16)
  header[0] = 19790
  header[1] = 20550
  header[2] = 2049
  header[3] = patterns
  header[4] = block_size
  header[5] = block_size
  header[6] = 0
  header[7] = 0

  file_bytes = []
  for row in matrix:
    for col in row:
      file_bytes.append(col)

  byte_array = struct.pack('%sf' % len(file_bytes), *file_bytes)

  new_file = ''
  filename = dirname + '+' + str(block_size) + '+' + str(block_size) + '+' + str(patterns) + '.nmf'
  f = open(filename, 'wb')
  f.write(header)
  f.write(byte_array)
  f.close()


def loadMatrix(mat_file):
  f = open(mat_file, 'rb')

#sig, ver, bpe, pat, b_height, b_width, junk = bytearray()
  sig = f.read(4)
  ver = f.read(1)
  bpe = f.read(1)
  patterns = f.read(2)
  height = f.read(2)
  width = f.read(2)
  junk = f.read(4)

  print(type(bpe))

  bpe = int.from_bytes(bpe, 'big')
  print(type(bpe))
  print(bpe)

  byte_arr = bytearray()
  byte_arr = f.read(int(patterns)*int(width)*int(height)*int(bpe))
  a = np.frombuffer(byte_arr, dtype=np.double)
  matrix = a.reshape(patterns, width*height)

  return matrix
