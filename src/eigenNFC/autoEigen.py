import os
import subprocess

REMOVE = [96]
PATTERNS = [48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64]
WIDTH = [48]

"""
csv = open("results2.csv", "w")
csv.write("PATTERNS,REMOVED,CORRECT,PERCENT\n")
"""
for r in REMOVE:
    for p in PATTERNS:
      for w in WIDTH:
          print(f"R: {r}\tP: {p}\tW:{w}")
          line = ""
          os.system(f"python3 eigenTrain.py -t /scratch/prism2022data/data/blur/training -r {r} -p {p} -w {w}")
          patternName = f"please-00+{w}+{256-r}+{p}.nmf"
          csvFile = f"{p}+{w}+{256-r}.csv"
          output = subprocess.check_output(f"python3 eigenTest.py -d reducedFromBoth/testing2 -p {patternName} -w {csvFile}", shell=True).decode("utf-8")
          print(output)

          """
          parameters = output.split(",")
          vals = []
          for p in parameters:
              p.strip()
              val = p.split(":")[-1]
              vals.append(val)

          vals[-1] = vals[-1][:-2]
          for idx, v in enumerate(vals):
              vals[idx] = v.strip()
              line += vals[idx] + ","
          line = line[:-1]
          line += "\n"
          csv.write(line)
          """
          os.system(f"rm {patternName}")

#csv.close()
