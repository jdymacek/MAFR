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
    filename.replace(".png", "_inverse.png")
    if s in species:
        inverseDir = "/scratch/prism2022data/" + species[s] + "/"
        newFile = "/scratch/prism2022data/training_inverse/" + s + "/" + filename.replace("_inverse.png", ".png")
        os.system("cp " + inverseDir + filename + " " + newFile)
        used.append(filename)


    