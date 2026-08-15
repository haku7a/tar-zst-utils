import argparse
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
    p_decomp.set_defaults(func=decompress)

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


def decompress(args):
    input_path = Path(args.file)
    output_path = input_path.with_suffix("")

    dctx = zstd.ZstdDecompressor()

    with open(input_path, "rb") as ifh:
        with open(output_path, "wb") as ofh:
            dctx.copy_stream(ifh, ofh)


def main(argv: List[str] | None = None):

    parser = build_parser()
    args = parser.parse_args(argv)

    if not Path(args.file).exists():
        parser.error(f"File not found: {args.file}")

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
