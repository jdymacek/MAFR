import os




parser = argparse.ArgumentParser("Toolchain for NFC Identification and Classification")
parser.add_argument("-h", help="h5 file directory", required=True)
args = parser.parse_args()





#first call h5 extract
hFiles = os.listdir(args.h)
for hFile in hFiles:
  fpath = args.h + '/' + hFile
  os.system("python3 extract5.py" + fpath)

#now call wavToPNG
wavDirs = os.listdir(os.cwd())
for wavDir in wavDirs:
  if "Bird" in wavDir:
    continue

  os.system("python3 wavToPng.py -d " + wavDir)

#next we have to split sets since filtering relies on that they're aready split up
species = {"1-1-2":"CHSP", "1-1-3":"SAVS", "1-4-1":"AMRE", "1-4-2":"BBWA", "1-4-3":"BTBW", "1-4-5":"COYE", "1-4-7":"OVEN"}
classes = species.keys()

for wavDir in wavDirs:
  if "Bird" in wavDir:
    continue

  os.system("python3 splitSets.py " +wavDir + " " + species[wavDir]+ " 0.6")

#now call the filtering stuff
#first, reduce noise

