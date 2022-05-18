import sys
import os

dirName = str(sys.argv[1])
filePath = os.path.abspath(__file__)
dirPath = os.path.join(os.path.dirname(filePath), dirName)

file_list = os.listdir(dirPath)
os.chdir(dirPath)

for filename in file_list:
    if filename.endswith(".wav"):
       #print filename, now generate png
       cmd = "sox " + filename + " -n spectrogram -X 256 -y 256 -l -m -r -o " + filename[:-3] + "png"
       os.system(cmd)
    else:
	continue

