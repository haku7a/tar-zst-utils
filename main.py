import argparse
import tarfile as tar
from pathlib import Path

import zstandard as zstd

parser = argparse.ArgumentParser()
parser.add_argument("--t", action="store_true")
parser.add_argument("--z", action="store_true")
parser.add_argument("file")
args = parser.parse_args()


path = Path(args.file)

print(path)

out_tar_path = path.with_suffix("")
print(out_tar_path)

if args.z:
    with open(path, "rb") as f:
        decompressor = zstd.ZstdDecompressor()
        with open(out_tar_path, "wb") as out:
            decompressor.copy_stream(f, out)

if args.t:
    with tar.open(out_tar_path, "r") as t:
        t.extractall(path="output_folder")
