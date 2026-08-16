import argparse
import tarfile
from pathlib import Path

import zstandard as zstd


def decompress_extract(args: argparse.Namespace) -> None:
    input_path = Path(args.file)
    output_path = Path(args.output) if args.output else Path("output_folder")
    output_path.mkdir(parents=True, exist_ok=True)

    dctx = zstd.ZstdDecompressor()

    with open(input_path, "rb") as ifh:
        reader = dctx.stream_reader(ifh)
        with tarfile.open(fileobj=reader, mode="r|") as tar:
            tar.extractall(path=output_path, filter="data")
