import MAFR
import random
from PIL import Image
import numpy as np

#img is 542, 260
img = MAFR.loadImage('test-image.png', 16)
img.save('cropped.png')
print(f'WIDTH: {img.width}\nHEIGHT: {img.height}')

matrix = MAFR.imageToMatrix(img, 16)
print(matrix)

#a = np.random.rand(5,5)

a = [[0,0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3]]
nd_a = np.array(a, dtype=np.double)

MAFR.saveMatrix(nd_a, 4, 2, 'OVEN', 'test-dir')
test = MAFR.loadMatrix('test-dir+2+2+4.nmf')

print(nd_a)
print(test)

if np.array_equal(nd_a, test):
  print('same')
else:
  print('oops')

b = [[0,0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3]]
nd_b = np.array(b, dtype=np.double)

print(MAFR.computeError(a,b))
