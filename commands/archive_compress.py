import argparse
import tarfile
from pathlib import Path

import zstandard as zstd


def archive_compress(args: argparse.Namespace) -> None:
    input_path = Path(args.file)
    output_path = (
        Path(args.output)
        if args.output
        else input_path.with_suffix(input_path.suffix + ".tar.zst")
    )

    cctx = zstd.ZstdCompressor(level=args.level, threads=args.threads)

    with open(output_path, "wb") as ofh:
        with cctx.stream_writer(ofh) as compressor:
            with tarfile.open(fileobj=compressor, mode="w|") as tar:
                tar.add(input_path, arcname=input_path.name)
