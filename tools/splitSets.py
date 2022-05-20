import sys
import array
import random
import os
import shutil

dirName = str(sys.argv[1])
newSets =  str(sys.argv[2])
#still need to update the custom percentage split sets
splitPercent = str(sys.argv[3])
splitPercent = float(splitPercent)
#the given one will be used for training

filePath = os.path.abspath(__file__)
dirPath = os.path.join(os.path.dirname(filePath), dirName)

file_list = os.listdir(dirPath)
random_list = []
i=0
for filename in file_list:
     if filename.endswith(".png"):
        random_list.insert(i, filename)
        i+=1
     else:
        continue

curDir = os.getcwd()
os.chdir('training')
random.shuffle(random_list)
trainDir = os.mkdir(newSets)
sixty_i = int(i*0.6)
sixty_i = int(i*splitPercent)
print(len(random_list))
j=0;
while j < sixty_i:
    fname_path = os.path.join(dirPath, random_list[j])
    shutil.copy(fname_path, newSets)
    j+=1

os.chdir(curDir +'/testing')
print(j)
testDir = os.mkdir(newSets)
j = int(sixty_i)
k=0
while j < i:
    fname_path = os.path.join(dirPath, random_list[j])
    shutil.copy(fname_path, newSets)
    j+=1
    k+=1
print(k)


