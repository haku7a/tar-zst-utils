import argparse
from pathlib import Path

import zstandard as zstd


def decompress(args: argparse.Namespace) -> None:
    input_path = Path(args.file)
    output_path = Path(args.output) if args.output else input_path.with_suffix("")

    dctx = zstd.ZstdDecompressor()

    with open(input_path, "rb") as ifh:
        with open(output_path, "wb") as ofh:
            dctx.copy_stream(ifh, ofh)
