import argparse
import tarfile
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
    p_decomp.add_argument(
        "-o", "--output", help="Output file path (default: input filename without .zst)"
    )
    p_decomp.set_defaults(func=decompress)

    # extract
    p_extract = subparsers.add_parser(
        "extract", aliases=["e"], help="Extract a .tar archive"
    )
    p_extract.add_argument("file")
    p_extract.add_argument(
        "-o", "--output", help="Output directory path (default: output_folder)"
    )
    p_extract.set_defaults(func=extract)

    # decompress + extract
    p_decex = subparsers.add_parser(
        "decompress-extract", aliases=["de"], help="Decompress and extract in one step"
    )
    p_decex.add_argument("file")
    p_decex.add_argument(
        "-o", "--output", help="Output directory path (default: output_folder)"
    )
    p_decex.set_defaults(func=decompress_extract)

    # compress
    p_comp = subparsers.add_parser(
        "compress", aliases=["c"], help="Compress a file to .zst"
    )
    p_comp.add_argument("file")
    p_comp.add_argument(
        "-o", "--output", help="Output file path (default: input filename + .zst)"
    )
    p_comp.add_argument(
        "-l",
        "--level",
        type=int,
        default=22,
        help="Compression level, 1-22 (default: 22)",
    )
    p_comp.set_defaults(func=compress)

    return parser


def decompress(args: argparse.Namespace) -> None:
    input_path = Path(args.file)
    output_path = Path(args.output) if args.output else input_path.with_suffix("")

    dctx = zstd.ZstdDecompressor()

    with open(input_path, "rb") as ifh:
        with open(output_path, "wb") as ofh:
            dctx.copy_stream(ifh, ofh)


def extract(args: argparse.Namespace) -> None:
    input_path = Path(args.file)
    output_path = Path(args.output) if args.output else Path("output_folder")
    output_path.mkdir(parents=True, exist_ok=True)

    with tarfile.open(input_path, "r") as tar:
        tar.extractall(path=output_path, filter="data")


def decompress_extract(args: argparse.Namespace) -> None:
    input_path = Path(args.file)
    output_path = Path(args.output) if args.output else Path("output_folder")
    output_path.mkdir(parents=True, exist_ok=True)

    dctx = zstd.ZstdDecompressor()

    with open(input_path, "rb") as ifh:
        reader = dctx.stream_reader(ifh)
        with tarfile.open(fileobj=reader, mode="r|") as tar:
            tar.extractall(path=output_path, filter="data")


def compress(args: argparse.Namespace) -> None:
    input_path = Path(args.file)
    output_path = (
        Path(args.output)
        if args.output
        else input_path.with_suffix(input_path.suffix + ".zst")
    )

    cctx = zstd.ZstdCompressor(level=args.level)

    with open(input_path, "rb") as ifh:
        with open(output_path, "wb") as ofh:
            cctx.copy_stream(ifh, ofh)


def main(argv: List[str] | None = None) -> None:

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
