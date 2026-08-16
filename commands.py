import argparse
import tarfile
from pathlib import Path

import zstandard as zstd


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

    cctx = zstd.ZstdCompressor(level=args.level, threads=args.threads)

    with open(input_path, "rb") as ifh:
        with open(output_path, "wb") as ofh:
            cctx.copy_stream(ifh, ofh)


def archive(args: argparse.Namespace) -> None:
    input_path = Path(args.file)
    output_path = (
        Path(args.output)
        if args.output
        else input_path.with_suffix(input_path.suffix + ".tar")
    )

    with tarfile.open(output_path, "w") as tar:
        tar.add(input_path, arcname=input_path.name)


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
