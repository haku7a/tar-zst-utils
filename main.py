import argparse
import sys
import tarfile as tar
from pathlib import Path

import zstandard as zstd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", action="store_true")
    parser.add_argument("-z", action="store_true")
    parser.add_argument("--zt", action="store_true")
    parser.add_argument("file")
    args = parser.parse_args()

    if not (args.t or args.z or args.zt):
        parser.error("Please specify at least one flag: -t, -z, or --zt")

    path = Path(args.file)

    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    out_tar_path = path.with_suffix("")

    try:
        if args.z or args.zt:
            with open(path, "rb") as f:
                decompressor = zstd.ZstdDecompressor()
                with open(out_tar_path, "wb") as out:
                    decompressor.copy_stream(f, out)

        if args.t or args.zt:
            with tar.open(out_tar_path, "r") as t:
                t.extractall(path="output_folder")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
