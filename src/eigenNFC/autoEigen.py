import os
import subprocess
import argparse

parser = argparse.ArgumentParser("Testing harness for MAFR")
parser.add_argument("-p", help="range of pattern values", required=True)
parser.add_argument("-r", help="range of removal values", required=True)
parser.add_argument("-w", help="range of width values", required=True)

args = parser.parse_args()
REMOVE = eval("[x for x in range" + args.r + "]")
WIDTH= eval("[x for x in range" + args.w + "]")
PATTERNS = eval("[x for x in range" + args.p + "]")


#REMOVE = [x for x in range(96,129)]
#REMOVE = [96]
#PATTERNS = [24]
#PATTERNS = [x for x in range(20,50)]
#WIDTH = [48]
#WIDTH = [x for x in range(36, 53)]

"""
csv = open("results2.csv", "w")
csv.write("PATTERNS,REMOVED,CORRECT,PERCENT\n")
"""
host = os.uname()[1]
fout = open(f"exploreOut/{host}.txt", "a")
for r in REMOVE:
    for p in PATTERNS:
      for w in WIDTH:
          line = ""
          os.system(f"python3 newTrain.py -t /scratch/prism2022data/data/blur/training -r {r} -p {p} -w {w}")
          patternName = f"please-00+{w}+{256-r}+{p}.nmf"
          csvFile = f"NEW-{p}+{w}+{256-r}.csv"
          output = subprocess.check_output(f"python3 eigenTest.py -d blur/testing -p {patternName} -w {csvFile}", shell=True).decode("utf-8")
          fout.write(output)
#print(output, end="")

          os.system(f"rm {patternName}")
          os.system(f"rm {csvFile}")

fout.close()
#csv.close()
