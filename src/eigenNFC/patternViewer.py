import math
import numpy as np
from PIL import Image
import MAFR
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", help="pattern file to view")

args = parser.parse_args()

file = args.p

height = int(file.split("+")[-2])
width = int(file.split("+")[-3])

M, labels = MAFR.loadMatrix(args.p)
maximum = np.amax(M)
n = (M/maximum) * 255

size = int(math.sqrt(len(n[0])))
res = Image.new('L', (width, height*len(n)))

for i, row in enumerate(n):
    tile = row.astype(np.uint8)
    img = Image.fromarray(tile.reshape(height, width), mode="L")
    res.paste(img, (0, i*height, width, (i+1)*height))

res.save(file[:-3] + "png")
