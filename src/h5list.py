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
parser.add_argument('-r', help='reject file', default=None)
args = parser.parse_args()

h5Dir = args.d
#TODO if output directory is empty, outputs as file
species = {"1-1-2": "CHSP", "1-1-3":"SAVS", "1-4-1" :"AMRE", "1-4-2":"BBWA", "1-4-3":"BTBW", "1-4-5":"COYE", "1-4-7":"OVEN"}

allFiles = [x[0] + "/" + y for x in os.walk(h5Dir) for y in x[2] if y.endswith("_original.h5") and y[-17:-12] in species ]

cullSet = set()
if args.r != None:
    with open(args.r, 'r') as rejectFile:
        lines = rejectFile.readlines()
        cullSet = set([x.strip() for x in lines ]) 
    


data  = {}
for file in allFiles:

    sp = species[file[-17:-12]]
    dataset = file[:-18].split("/")[-1]
    with h5py.File(file, "r") as h5:
        good = 0
        bad = 0
        for k in h5['waveforms'].keys():
            if k not in cullSet:
                good += 1
            else:
                bad += 1
    print(sp,"\t",dataset, "\t", good, "\t", bad,"\t", (bad/(good+bad)))


