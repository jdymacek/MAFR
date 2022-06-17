import os
import subprocess

REMOVE = [96, 97, 98, 99, 100, 101, 102, 103, 104]
PATTERNS = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]

csv = open("results.csv", "w")
csv.write("PATTERNS,REMOVED,CORRECT,PERCENT\n")
i = 0
for r in REMOVE:
    for p in PATTERNS:
        if i >= 3:
            csv.close()
            quit()
        line = ""
        os.system(f"python3 eigenTrain.py -t /scratch/prism2022data/data/reducedNoise/training -r {r} -p {p}")
        patternName = f"please-00+96+{256-r}+{p}.nmf"
        output = subprocess.check_output(f"python3 eigenClassify.py -d reducedNoise/testing -p {patternName}", shell=True).decode("utf-8")
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
        i += 1

