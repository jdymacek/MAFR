import os 
import argparse
import h5py 
from scipy.io.wavfile import write


parser = argparse.ArgumentParser(description= 'Get all h5 files')
parser.add_argument('-d', help='directory for h5 files')
parser.add_argument('-o', help='output directory')
parser.add_argument('-r', help='reject file')
args = parser.parse_args()

h5Dir = args.d
outputDir = args.o
#TODO if output directory is empty, outputs as file
species = {"1-1-2": "CHSP", "1-1-3":"SAVS", "1-4-1" :"AMRE", "1-4-2":"BBWA", "1-4-3":"BTBW", "1-4-5":"COYE", "1-4-7":"OVEN"}

allFiles = [x[0] + "/" + y for x in os.walk(h5Dir) for y in x[2] if y.endswith("_original.h5") and y[-17:-12] in species ]

cullSet = set()
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
        for k in h5['waveforms'].keys():
            if k not in cullSet:
                 dataset = file[:-18].split("/")[-1]
            
                 sp = species[file[-17:-12]]
                 data = h5['waveforms'][k][:]
                 
           # print(data.dtype)
                 write(outputDir + sp + "/" + k + ".wav", 22050, data)
            #with open("temp/" + k + ".wav","wb") as outfile:
            else:
                 print(k)



