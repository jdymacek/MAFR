import os

REMOVE = [96, 97, 98, 99, 100, 101, 102, 103, 104]
PATTERNS = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]
CSV = "test.csv"

for r in REMOVE:
    for p in PATTERNS:
        os.system(f"python3 eigenTrain.py -t /scratch/prism2022data/data/reducedNoise/training -r {r} -p {p}")
        patternName = f"please-00+{256-r}+{p}"
        os.system(f"python3 eigenClassify.py -t reducedNoise/testing -p {patternName}")
        quit()