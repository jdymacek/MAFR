import os
import csv

species = {"AMRE":"1-4-1_inverse", "BBWA":"1-4-2_inverse", "BTBW":"1-4-3_inverse", "COYE":"1-4-5_inverse", "OVEN":"1-4-7_inverse"}
classes = species.keys()

annotations = open("/scratch/prism2022data/annotations.txt", "r")
ann = []
for line in csv.reader(annotations, delimiter="\t"):
    ann.append(line[0])

used = []
for f in ann:
    s = f.split("/")[1]
    filename = f.split("/")[-1]
    inverseName = filename.replace(".png", "_inverse.png")
    if s in species:
        inverseDir = "/scratch/prism2022data/" + species[s] + "/"
        newFile = "/scratch/prism2022data/trainingTwoInverse/" + s + "/" + filename
        os.system("cp " + inverseDir + inverseName + " " + newFile)
        used.append(inverseName)

dest = "/scratch/prism2022data/testingTwoInverse/"

for k, v in species.items():
  for f in os.listdir("/scratch/prism2022data/" + v):
    if f not in used:
      newFile = f.replace("_inverse.png", ".png")
      os.system("cp /scratch/prism2022data/" + v + "/" + f + " " + dest + k + "/" + newFile)
