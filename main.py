import argparse
import sys
import tarfile as tar
from pathlib import Path
from typing import List

import zstandard as zstd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tar-zst-utils")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # decompress
    p_decomp = subparsers.add_parser(
        "decompress", aliases=["d"], help="Decompress .zst to .tar"
    )
    p_decomp.add_argument("file")

    # extract
    p_extract = subparsers.add_parser(
        "extract", aliases=["e"], help="Extract a .tar archive"
    )
    p_extract.add_argument("file")

    # decompress + extract
    p_decex = subparsers.add_parser(
        "decompress-extract", aliases=["de"], help="Decompress and extract in one step"
    )
    p_decex.add_argument("file")

    return parser


def main(argv: List[str] | None = None):

    parser = build_parser()
    args = parser.parse_args(argv)

    if not Path(args.file).exists():
        parser.error(f"File not found: {args.file}")

    try:
        path = args.file

        if args.command in ("decompress", "decompress-extract", "d", "de"):
            out_tar_path = Path(args.file).with_suffix("")
            with open(path, "rb") as f:
                decompressor = zstd.ZstdDecompressor()
                with open(out_tar_path, "wb") as out:
                    decompressor.copy_stream(f, out)
            tar_path = out_tar_path
        else:
            tar_path = Path(args.file)

        if args.command in ("extract", "decompress-extract", "e", "de"):
            with tar.open(tar_path, "r") as t:
                t.extractall(path="output_folder", filter="data")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    main()
