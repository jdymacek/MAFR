#MAFR.py --- Magnificent Frigatebird NFC Module

import struct
import numpy as np
from PIL import Image
from PIL import ImageOps

def loadImage(filename, size):
  img = Image.open(filename)
  x_n = img.width // size
  x_diff = (img.width % size) // 2
  y_n = img.height // size

  return img.crop((x_diff, 0, (img.width - x_diff), img.height - (img.height % size)))

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

### https://stackoverflow.com/questions/46700018/join-two-hex-integers-in-python
MAX_INT = 255
NUM_BITS = MAX_INT.bit_length()

def merge_chars(a,b):
  c = (ord(a) << NUM_BITS) | ord(b)
  return c

###
def saveMatrix(matrix, patterns, block_size, species_code, dirname):


  species_first = merge_chars(species_code[1], species_code[0])
  species_last = merge_chars(species_code[3], species_code[2])

  header = np.ndarray(8, dtype=np.uint16)
  header[0] = 19790
  header[1] = 20550
  header[2] = 2049
  header[3] = patterns
  header[4] = block_size
  header[5] = block_size
  header[6] = species_first
  header[7] = species_last

#file_bytes = []
#for row in matrix:
#for col in row:
#file_bytes.append(col)

  byte_array = matrix.tobytes()

#byte_array = struct.pack('%sf' % len(file_bytes), *file_bytes)

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
  print(sig)
  ver = f.read(1)
  print(ver)
  bpe = f.read(1)
  print(bpe)
  patterns = f.read(2)
  print(patterns)
  height = f.read(2)
  print(height)
  width = f.read(2)
  print(width)
  code = f.read(4)
  print(code)

  pat = int.from_bytes(patterns, byteorder='little')
  wid = int.from_bytes(width, byteorder='little')
  ht = int.from_bytes(height, byteorder='little')
  byte = int.from_bytes(bpe, byteorder='little')
  print(pat)
  print(wid)
  print(ht)
  print(byte)

  byte_arr = f.read()
  print(len(byte_arr))
  a = np.frombuffer(byte_arr, dtype=np.double)
  matrix = a.reshape(pat, wid*ht)

  return matrix

def computeError(original, patterns):
  inv = np.linalg.pinv(patterns)
  c = np.matmul(original, inv)
  m_hat = np.matmul(c, patterns)
  return np.linalg.norm(original - m_hat)

def getSpecies(mat_file):
  f = open(mat_file, 'rb')
  prev = f.read(12)
  code = f.read(4)
  s = code.decode('utf-8')
  #print(s)
  return s

def getBlocksize(mat_file):
  f = open(mat_file, 'rb')
  prev = f.read(8)
  size = f.read(2)
  return int.from_bytes(size, byteorder='little')
