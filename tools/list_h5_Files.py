import os 
import argparse

import h5py 

parser = argparse.ArgumentParser(description= 'Get all h5 files')
parser.add_argument('-d', help='directory for h5 files')

args = parser.parse_args()

h5Dir = args.d


species = {"1-1-2": "CHSP", "1-1-3":"SAVS", "1-4-1" :"AMRE", "1-4-2":"BBWA", "1-4-3":"BTBW", "1-4-5":"COYE", "1-4-7":"OVEN"}

allFiles = [x[0] + "/" + y for x in os.walk(h5Dir) for y in x[2] if y.endswith("_original.h5") and y[-17:-12] in species ]


print("Set\tSp.\tFile")
for file in allFiles:

    with h5py.File(file, "r") as h5:
        for k in h5['waveforms'].keys():
            dataset = file[:-18].split("/")[-1]
            print(dataset, "\t",species[file[-17:-12]], "\t", k) 


