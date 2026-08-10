import argparse
from pathlib import Path

import zstandard as zstd

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()


path = Path(args.file)

out_tar_path = path.with_suffix("")


with open(path, "rb") as f:
    decompressor = zstd.ZstdDecompressor()
    with open(out_tar_path, "wb") as out:
        decompressor.copy_stream(f, out)
