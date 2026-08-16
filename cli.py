import argparse

from commands import (
    archive,
    archive_compress,
    compress,
    decompress,
    decompress_extract,
    extract,
)


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
    p_comp.add_argument(
        "-t",
        "--threads",
        type=int,
        default=0,
        help="Number of threads (0 = all CPUs, default: 0)",
    )
    p_comp.set_defaults(func=compress)

    # archive
    p_arch = subparsers.add_parser(
        "archive", aliases=["a"], help="Create a .tar archive"
    )
    p_arch.add_argument("file")
    p_arch.add_argument(
        "-o", "--output", help="Output file path (default: source name + .tar)"
    )
    p_arch.set_defaults(func=archive)

    # archive + compress
    p_archcomp = subparsers.add_parser(
        "archive-compress",
        aliases=["ac"],
        help="Archive and compress to .tar.zst in one step",
    )
    p_archcomp.add_argument("file")
    p_archcomp.add_argument(
        "-o", "--output", help="Output file path (default: source name + .tar.zst)"
    )
    p_archcomp.add_argument(
        "-l",
        "--level",
        type=int,
        default=22,
        help="Compression level, 1-22 (default: 22)",
    )
    p_archcomp.add_argument(
        "-t",
        "--threads",
        type=int,
        default=0,
        help="Number of threads (0 = all CPUs, default: 0)",
    )
    p_archcomp.set_defaults(func=archive_compress)

    return parser
