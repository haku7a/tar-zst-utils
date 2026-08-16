import argparse
import tarfile
from pathlib import Path


def archive(args: argparse.Namespace) -> None:
    input_path = Path(args.file)
    output_path = (
        Path(args.output)
        if args.output
        else input_path.with_suffix(input_path.suffix + ".tar")
    )

    with tarfile.open(output_path, "w") as tar:
        tar.add(input_path, arcname=input_path.name)
