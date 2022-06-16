import MAFR
import numpy as np
import PIL
from PIL import Image
import argparse
import os
from sklearn import decomposition
import time

def imageToVector(imageName, x=0, y=0, width=256, height=256):
    image = MAFR.loadImage(imageName, 16)
    tile = image.crop((x,y, x+width, y+height))
    a = np.asarray(tile)
    return a.flatten()

def arrayToImage(tile, width, height):
    tile = np.clip(np.rint(tile),a_min=0, a_max=255)
    tile = tile.astype(np.uint8)

    return Image.fromarray(tile.reshape(height, width), mode="L")

