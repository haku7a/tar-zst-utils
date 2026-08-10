import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()


path = Path(args.file)

print(path.resolve())
