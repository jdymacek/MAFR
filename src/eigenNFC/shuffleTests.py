#shuffleTests.py -- creates new blur directories that are randomly shuffled

import os
import random
import shutil

PATH = "/scratch/prism2022data/data/blur"


allFiles = [x[0] + "/" +  y  for x in os.walk(PATH) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]

classIndexs = ["AMRE" ,"BBWA", "BTBW", "CHSP", "COYE", "OVEN", "SAVS"]

classList = [["AMRE"], ["BBWA"], ["BTBW"], ["CHSP"], ["COYE"], ["OVEN"], ["SAVS"]]

#seperating files by species
for f in allFiles:
  fClass = f[:46]
  fClass = fClass[41:].replace('/', '')
  for l in classList:
    if fClass in l:
      l.append(f)
  
#creates 7 new randomly shuffled directory
i = 0
while i < 7:
  for l in classList:
    l.pop(0)
    random.shuffle(l)

  os.mkdir("/scratch/prism2022data/data/blurTest"+str(i))
  os.mkdir("/scratch/prism2022data/data/blurTest"+str(i)+ "/training")
  os.mkdir("/scratch/prism2022data/data/blurTest"+str(i)+"/testing")

  classInd =0
  #splitting sets for each species

  for l in classList:
    os.mkdir("/scratch/prism2022data/data/blurTest"+str(i)+ "/training/"+ classIndexs[classInd])
    os.mkdir("/scratch/prism2022data/data/blurTest"+str(i)+"/testing/"+ classIndexs[classInd])

    j=1
    while j < (len(l)*0.6):
      shutil.copy(l[j], "/scratch/prism2022data/data/blurTest"+str(i)+"/training/"+ classIndexs[classInd])
      j+=1
 
    tre = 0
    while j < len(l):
      shutil.copy(l[j], "/scratch/prism2022data/data/blurTest"+str(i)+"/testing/"+ classIndexs[classInd])
      j+=1
      tre+=1
    classInd+=1
  i+=1

