from pathlib import Path
from typing import List

from cli import build_parser


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
