import MAFR
import random
from PIL import Image

#img is 542, 260
img = MAFR.loadImage('test.png', 16)
img.save('cropped.png')
print(f'WIDTH: {img.width}\nHEIGHT: {img.height}')

matrix = MAFR.imageToMatrix(img, 16)
print(matrix)

MAFR.saveMatrix(matrix, 64, 16, 2, 'test-dir')

test = MAFR.loadMatrix('test-dir+16+16+64.nmf')

if test == matrix:
  print('Success!')
else:
  print('Aw man :(')

