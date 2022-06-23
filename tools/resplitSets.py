import os
import csv

species = {"CHSP":"1-1-2", "SAVS":"1-1-3", "AMRE":"1-4-1", "BBWA":"1-4-2", "BTBW":"1-4-3", "COYE":"1-4-5", "OVEN":"1-4-7"}
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
