#!/usr/bin/env python3

import os 
import argparse
import h5py 
from spei import SPEI
from nofl import NOFL

from PIL import Image

#extract h5 of wavs into spectograms
# -- noise filtering should be an option
# -- mel or regular should be an option

parser = argparse.ArgumentParser(description= 'Get all h5 files')
parser.add_argument('-d', help='directory for h5 files')
parser.add_argument('-o', help='output directory')
parser.add_argument('-r', help='reject file', default=None)
parser.add_argument('-m', help='mel-bands', default=None)
parser.add_argument('-s', help='shift?' , default=None)
args = parser.parse_args()

h5Dir = args.d
outputDir = args.o
#TODO if output directory is empty, outputs as file
species = {"1-1-2": "CHSP", "1-1-3":"SAVS", "1-4-1" :"AMRE", "1-4-2":"BBWA", "1-4-3":"BTBW", "1-4-5":"COYE", "1-4-7":"OVEN"}

allFiles = [x[0] + "/" + y for x in os.walk(h5Dir) for y in x[2] if y.endswith("_original.h5") and y[-17:-12] in species ]

cullSet = set()
if args.r != None:
    with open(args.r, 'r') as rejectFile:
        lines = rejectFile.readlines()
        cullSet = set([x.strip() for x in lines ]) 
    



for file in allFiles:

    sp = species[file[-17:-12]]
    try: 
        os.makedirs(outputDir+sp)
    except FileExistsError:
        pass
    with h5py.File(file, "r") as h5:
        #print(h5.keys())
        #print(h5["sample_rate"][()])
        #print(h5["variant"][()])
        #print(h5["taxonomy_code"][()])
        #print(h5["dataset"][()])
        
        engine = SPEI()
        noiseFilter = NOFL()
        for k in h5['waveforms'].keys():
            if k not in cullSet:
                 dataset = file[:-18].split("/")[-1]
                 sp = species[file[-17:-12]]
                 data = h5['waveforms'][k][:]
                 #SHIFT OLDBIRD 12 pixels left for our orginial 7
                 shift = 0
                 if dataset == "oldbird" and args.s != None:
                     shift = -12
                 if args.m == None:
                     img = noiseFilter.filter(engine.spec_as_image(data),shift=shift)
                 else:
                     img = noiseFilter.filter(engine.mel_as_image(data,mel_bands=int(args.m)),shift=shift) 
                 img.save(outputDir + sp + "/" + k + ".png")
            else:
                 print(k)



