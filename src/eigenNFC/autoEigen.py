import os
import subprocess

REMOVE = [48, 52, 64, 80, 96, 104]
PATTERNS = [24, 32, 48, 64]

csv = open("results2.csv", "w")
csv.write("PATTERNS,REMOVED,CORRECT,PERCENT\n")

for r in REMOVE:
    for p in PATTERNS:
        line = ""
        os.system(f"python3 eigenTrain.py -t /scratch/prism2022data/data/blur/training -r {r} -p {p}")
        patternName = f"please-00+96+{256-r}+{p}.nmf"
        output = subprocess.check_output(f"python3 eigenDistribution.py -d reducedFromBoth/testing2 -p {patternName}", shell=True).decode("utf-8")
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

        os.system(f"rm {patternName}")

csv.close()
