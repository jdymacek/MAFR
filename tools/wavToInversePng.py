import sys
import os
import shutil

dirName = str(sys.argv[1])
filePath = os.path.abspath(__file__)
dirPath = os.path.join(os.path.dirname(filePath), dirName)

os.mkdir(dirName+"_inverse")
file_list = os.listdir(dirPath)
os.chdir(dirPath)
for filename in file_list:
    if filename.endswith(".wav"):
       #print filename, now generate png
       cmd = "sox " + filename + " -n spectrogram -X 512 -y 257 -m -r -l -o " + filename[:-4] + "_inverse.png"
       os.system(cmd)

       shutil.move(filename[:-4] + "_inverse.png", "//scratch//prism2022data//"+dirName+"_inverse")


    else:
        continue


