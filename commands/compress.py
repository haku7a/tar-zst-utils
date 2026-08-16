import argparse
from pathlib import Path

import zstandard as zstd


def compress(args: argparse.Namespace) -> None:
    input_path = Path(args.file)
    output_path = (
        Path(args.output)
        if args.output
        else input_path.with_suffix(input_path.suffix + ".zst")
    )

    cctx = zstd.ZstdCompressor(level=args.level, threads=args.threads)

    with open(input_path, "rb") as ifh:
        with open(output_path, "wb") as ofh:
            cctx.copy_stream(ifh, ofh)
