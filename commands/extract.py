import argparse
import tarfile
from pathlib import Path


def extract(args: argparse.Namespace) -> None:
    input_path = Path(args.file)
    output_path = Path(args.output) if args.output else Path("output_folder")
    output_path.mkdir(parents=True, exist_ok=True)

    with tarfile.open(input_path, "r") as tar:
        tar.extractall(path=output_path, filter="data")
