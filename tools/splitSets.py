import sys
import array
import random
import os
import shutil

dirName = str(sys.argv[1])
newSets =  str(sys.argv[2])

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

random.shuffle(random_list)
training_dir = newSets + "_training"
sixty_i = int(i*0.6)
print(sixty_i)
j=0;
os.mkdir(training_dir)
while j < sixty_i:
    fname_path = os.path.join(dirPath, random_list[j])
    shutil.copy(fname_path, training_dir)
    j+=1


testing_dir = newSets + "_testing"
j = int(sixty_i)

os.mkdir(testing_dir)
while j < i:
    fname_path = os.path.join(dirPath, random_list[j])
    shutil.copy(fname_path, testing_dir)
    j+=1
    
