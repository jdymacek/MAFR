import subprocess

DIR = "prism/MAFR/src/eigenNFC;"
systems = ["lovelace", "knuth", "babbage", "amdahl", "chomsky", "vonneumann", "dijkstra", "pascal", "kernighan", "lamport", "mccarthy", "shannon", "stroustrup", "turing", "wirth", "church"]
processes = []

baseArgs = ["ssh", "", "cd", DIR, "python3", "autoEigen.py"] 
for idx, s in enumerate(systems):
  baseArgs[1] = s
  patternVal = '"' + str((20 + 2*idx, 20+2*(idx+1))) + '"'
  removeVal = '"' + str((96,125)) + '"'
  widthVal = '"'+ str((36, 49)) + '"'
  newArgs = ["-p", patternVal, "-r", removeVal, "-w", widthVal, ";"]
  args = baseArgs + newArgs
  processes.append(subprocess.Popen(args))

for p in processes:
  p.wait()

