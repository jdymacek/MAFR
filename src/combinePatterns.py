import MAFR
import argparse

parser = argparse.ArgumentParser(description='Combine two pattern matrices.')

parser.add_argument('-d', help="Path to .nmf pattern files")
parser.add_argument('-o', type=str, help='Path to output file.', default=".")
parser.add_argument('-b', help="blockSize")

args = parser.parse_args()

path = args.d
output = args.o
blockSize = int(args.b)

MAFR.saveNewFormat(path, blockSize, out=output)
