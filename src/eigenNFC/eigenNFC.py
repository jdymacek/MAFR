import MAFR
import numpy as np
import PIL
from PIL import Image
import argparse

def imageToVector(imageName, x=0, y=0, width=256, height=256):
    image = MAFR.loadImage(imageName, 16)
    tile = image.crop((x,y, x+width, y+height))
    a = np.asarray(tile)
    return a.flatten()

def arrayToImage(tile, width, height):
    tile = np.clip(np.rint(tile),a_min=0, a_max=255)
    tile = tile.astype(np.uint8)

    return Image.fromarray(tile.reshape(width,height), mode="L")


parser = argparse.ArgumentParser(description='Convert an image to a vector')
parser.add_argument('-t', help='training directory')

args = parser.parse_args()

tstDirectory = args.t

allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png")]
f = allFiles[0]

arr = imageToVector(f, x=72, y=0, width=96, height=192)
print(arr)

"""
img = arrayToImage(arr, 96, 192)
img.save("test.png")
"""