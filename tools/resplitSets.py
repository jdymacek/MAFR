import os
import csv

species = {"AMRE":"1-4-1_inverse", "BBWA":"1-4-2_inverse", "BTBW":"1-4-3_inverse", "COYE":"1-4-5_inverse", "OVEN":"1-4-7_inverse"}
classes = species.keys()

annotations = open("/scratch/prism2022data/annotations.txt", "r")
ann = []
for line in csv.reader(annotations, delimiter="\t"):
    ann.append(line[0])

for f in ann:
    species = f.split("/")[1]
    print(species)