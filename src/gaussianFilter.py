import MAFR
import PIL
from PIL import ImageFilter, Image
import argparse
import os

OUT = "/scratch/prism2022data/data/blurredReducedNormal/training"

parser = argparse.ArgumentParser("Gaussian Filter")

parser.add_argument("-r", help="Radius for blur")
parser.add_argument("-t", help="Directory to blur")

args = parser.parse_args()

rad = float(args.r)
tstDirectory = args.t

allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]

for f in allFiles:
	c = f.split("/")[-2]
	print(c)
	img = MAFR.loadImage(f,16)
	img2 = img.filter(ImageFilter.GaussianBlur(radius=rad))
	img2.save(OUT + "/" + c + "/" + f.split("/")[-1])
