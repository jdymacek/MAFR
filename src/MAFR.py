#MAFR.py --- Magnificent Frigatebird NFC Module

import struct
import numpy as np
from PIL import Image
from PIL import ImageOps
import os
import math
import sys
from datetime import datetime
from sklearn import decomposition
from random import shuffle

def loadImage(filename, size):
  img = Image.open(filename)
  img = ImageOps.grayscale(img)
  x_n = img.width // size
  x_diff = (img.width % size) // 2
  y_n = img.height // size

  '''print(img.getpixel((0,0)))'''

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

#tile = tile/np.max(tile)
#                       tile = tile*255

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
def saveMatrix(matrix, patterns, block_size, species_code, out=os.getcwd()):


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

  dir_list = os.listdir(out)

  new_file = ''
  filename = out + '/' + species_code + '-' + str(00).zfill(2) + '+' + str(block_size) + '+' + str(block_size) + '+' + str(patterns) + '.nmf'
  counter = 0
  while(1):
    if os.path.exists(filename):
      counter += 1
      filename = out + '/' + species_code + '-' + str(counter).zfill(2) + '+' + str(block_size) + '+' + str(block_size) + '+' + str(patterns) + '.nmf'
    else:
      break

  f = open(filename, 'wb')
  f.write(header)
  f.write(byte_array)
  f.close()

### matrixList = list of original .nmf pattern files 
'''
HEADER FORMAT:
    4 byte signature ('NMF{')
    1 byte version
    1 byte bytesPerEntry
    2 byte number of patterns
    2 byte blockSize
    2 byte number of entries
'''
def saveNewFormat(matrixPath, blockSize, out=os.getcwd()):
    sig = 'NMFC'
    sigFirst = merge_chars(sig[1], sig[0])
    sigSecond = merge_chars(sig[3], sig[2])

    header = np.ndarray(8,dtype=np.uint16)
    header[0] = sigFirst
    header[1] = sigSecond
    header[2] = 2049
    #header[3] = patterns
    header[4] = blockSize
    header[5] = 0
    header[6] = 0
    header[7] = 0

    d = os.listdir(matrixPath)
    files = [f for f in d if f.endswith('.nmf')]
    files.sort()
    print(files)

    ml = []
    indexList = []
    for f in files:
        path = matrixPath + f
        matrix, labels = loadMatrix(path)
        indexList += labels
        ml += [matrix]

    M = np.concatenate(ml)

    print("FROM SAVE:\n" + str(M))
    data = M.tobytes()

    patterns = len(indexList)
    header[3] = patterns
    indexBytes = patterns * 2

    index = np.ndarray(indexBytes, dtype=np.uint16)
    i = 0
    for e in indexList:
        sFirst = merge_chars(e[1], e[0])
        sLast = merge_chars(e[3], e[2])
        index[i] = sFirst
        index[i+1] = sLast
        i += 2
        
    '''
    for m in files:
      path = matrixPath + m
      s = getSpecies(path)
      matrix = loadMatrix(path)
      ml += [matrix]
      sFirst = merge_chars(s[1], s[0])
      sLast = merge_chars(s[3], s[2])
      index[i] = sFirst
      index[i+1] = sLast
      i += 2
    '''


    now = datetime.now()
    dt = now.strftime('%m-%d-%y-%H:%M:%S')

    filename = out + "/" + dt + "+" + str(blockSize) + "+" + str(patterns) + ".nmf"
    f = open(filename, "wb")
    f.write(header)
    f.write(index)
    f.write(data)
    f.close()

def saveHitPatterns(matrix, annotations, blockSize, out=os.getcwd()):
    sig = 'NMFC'
    sigFirst = merge_chars(sig[1], sig[0])
    sigSecond = merge_chars(sig[3], sig[2])

    header = np.ndarray(8,dtype=np.uint16)
    header[0] = sigFirst
    header[1] = sigSecond
    header[2] = 2049
    #header[3] = patterns
    header[4] = blockSize
    header[5] = 0
    header[6] = 0
    header[7] = 0

    patterns = len(annotations)
    header[3] = patterns
    indexBytes = patterns * 2

    data = matrix.tobytes()

    index = np.ndarray(indexBytes, dtype=np.uint16)
    i = 0
    for e in annotations:
        sFirst = merge_chars(e[1], e[0])
        sLast = merge_chars(e[3], e[2])
        index[i] = sFirst
        index[i+1] = sLast
        i += 2

    now = datetime.now()
    dt = now.strftime('%m-%d-%y-%H:%M:%S')

    filename = out + "/" + dt + "+" + str(blockSize) + "+" + str(patterns) + ".nmf"
    f = open(filename, "wb")
    f.write(header)
    f.write(index)
    f.write(data)
    f.close()


def loadMatrix(mat_file):
  f = open(mat_file, 'rb')

#sig, ver, bpe, pat, b_height, b_width, junk = bytearray()
  sig = f.read(4)
  if sig.decode("utf-8") == "NMFP":
      ver = f.read(1)
      bpe = f.read(1)
      patterns = f.read(2)
      height = f.read(2)
      width = f.read(2)
      code = f.read(4)

      pat = int.from_bytes(patterns, byteorder='little')
      wid = int.from_bytes(width, byteorder='little')
      ht = int.from_bytes(height, byteorder='little')
      byte = int.from_bytes(bpe, byteorder='little')

      byte_arr = f.read()
      a = np.frombuffer(byte_arr, dtype=np.double)
      matrix = a.reshape(pat, wid*ht)

      rowLabels = []
      for i in range(pat):
        rowLabels.append(code.decode("utf-8"))

      return (matrix, rowLabels)

  elif sig.decode("utf-8") == "NMFC":
      ver = f.read(1)
      bpe = f.read(1)
      patterns = f.read(2)
      blockSize = f.read(2)
      junk = f.read(6)

      p = int.from_bytes(patterns, byteorder='little')
      b = int.from_bytes(blockSize, byteorder='little')
      bpe = int.from_bytes(bpe, byteorder='little')

      index = []
      for i in range(p):
          code = f.read(4)
          codeString = code.decode("utf-8")
          index.append(codeString)

      pos = f.tell()

      #byte_arr = f.read(p*((b*b) * bpe))
      byte_arr = f.read()
      pos = f.tell()

      a = np.frombuffer(byte_arr, dtype=np.double)
      data = a.reshape(p, b*b)
      '''
      byte_arr = bytearray()
      for e in index:
        byte_arr += f.read((b*b) * bpe)
      a = np.frombuffer(byte_arr, dtype=np.double)
      data = a.reshape(p, b*b)
      '''
      '''
      for idx, species in enumerate(index):
        byte_arr = f.read(p * ((b * b) * 8))
        a = np.frombuffer(byte_arr, dtype=np.double)
        matrix = a.reshape(p, b*b)
        if species not in data:
          data[species] = [matrix]
        else:
          data[species] += [matrix]
      '''

      pos = f.tell()
      return (data, index)


def computeError(original, patterns):
#inv = np.linalg.pinv(patterns)
  
  print(original.shape)
  print(patterns.shape)
  custom = decomposition.NMF(n_components=len(patterns), init="random", random_state=0, max_iter=10000, solver="mu")
  custom = custom.fit(original)
  custom.components_ = patterns
  c = custom.transform(original)

  return np.linalg.norm(original-np.dot(c, patterns))

  '''
  fileList - list of PIL image objects (loaded in with loadImage to ensure on a 16 pixel boundary)
  pattern - pattern matrix to use as the components for the NMF model

  RETURN: average error for reconstructing all images in list with the given pattern
  '''

def errorFromFiles(fileList, pattern):
  
  custom = decomposition.NMF(n_components=len(pattern), init="random", random_state=0, max_iter=10000,
      solver="mu")

  m = imageToMatrix(fileList[0], 16)
  custom = custom.fit(m)
  custom.components_ = pattern

  total = 0
  for i in fileList:
    m = imageToMatrix(i, 16)
    W = custom.transform(m)
    total += np.linalg.norm(m-np.dot(W, pattern))

  return total / len(fileList)
  


def errorWithFiles(fileList, pattern):
  pattern = pattern[0]
  custom = decomposition.NMF(n_components=len(pattern), init="random", random_state=0, max_iter=10000,
      solver="mu")

  img = loadImage(fileList[0], 16) 
  m = imageToMatrix(img, 16)
  custom = custom.fit(m)
  custom.components_ = pattern


  errors = {}	
  for i in fileList:
    img = loadImage(i, 16)
    m = imageToMatrix(img, 16)
    W = custom.transform(m)
    errors[i] = np.linalg.norm(m-np.dot(W, pattern))

  return errors


 
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

'''
def quickError(original, patterns, inv):
  c = np.matmul(original, inv)
  m_hat = np.matmul(c, patterns)
  return np.linalg.norm(original-m_hat)
'''

#def getTimeStr():
#return datetime.now().strftime(

def closestDivisor(n):
  divisors = []
  for i in range(1, n+1):
    if n % i == 0:
      divisors += [i]

  target = math.floor(math.sqrt(n))

  for index, d in enumerate(divisors):
    if d > target:
      return divisors[index - 1]

def getPatterns(mat_file):
  f = open(mat_file, 'rb')
  prev = f.read(6)
  size = f.read(2)
  return int.from_bytes(size, byteorder='little')

def getClasses(directory):
  classes = next(os.walk(directory))[1]
  classes = list(filter(lambda x:len(x)==4, classes))
  classes = sorted(classes)
  return classes 


def listAllFiles(directory):
    
    allFiles = [x[0] + "/" + y for x in os.walk(directory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]
    
    classes = sorted(list(set([y for y in [x.split("/")[-2] for x in allFiles] if len(y) ==4])))
    
    return allFiles, classes


def splitSamples(files, trainingClasses, trainPercent, seed=None):
    
    trainingSamples = []
    testingSamples = []
    #testingSamples = [x for x in files if x.split("/")[-2] not in trainingClasses]
    for c in trainingClasses:
        classSamples = [x for x in files if x.split("/")[-2] == c]
       
        shuffle(classSamples)
        
        s = math.ceil(len(classSamples)*trainPercent)
        trainingSamples += classSamples[0:s]
        testingSamples += classSamples[s:]
    
    return trainingSamples, testingSamples






