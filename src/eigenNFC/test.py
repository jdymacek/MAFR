import subprocess

DIR = "prism/MAFR/src/eigenNFC;"
systems = ["lovelace", "knuth", "babbage", "amdahl", "chomsky", "dijkstra", "pascal", "kernighan", "lamport", "mccarthy", "shannon", "stroustrup", "turing", "church"]
processes = []

baseArgs = ["ssh", "", "cd", DIR, "python3", "autoClass.py"] 
for idx, s in enumerate(systems):
  baseArgs[1] = s
  patternVal = '"' + str((48 + 2*idx, 48+2*(idx+1))) + '"'
  removeVal = '"' + str((96,125)) + '"'
  widthVal = '"'+ str((36, 49)) + '"'
  newArgs = ["-p", patternVal, "-r", removeVal, "-w", widthVal, "-d", "/scratch/prism2022data/data/blur/training", "-t", "/scratch/prism2022data/data/blur/testing;"]
  args = baseArgs + newArgs
  processes.append(subprocess.Popen(args))

for p in processes:
  p.wait()

