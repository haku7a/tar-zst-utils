import argparse
from pathlib import Path

import zstandard as zstd

from commands.compress import compress


def _make_args(file: Path, output=None, level=3, threads=0) -> argparse.Namespace:
    return argparse.Namespace(
        file=str(file),
        output=output,
        level=level,
        threads=threads,
    )


def test_tar_archive_has_valid_content(tar_file: Path) -> None:
    original_content = tar_file.read_bytes()

    args = _make_args(tar_file)
    compress(args)

    expected = tar_file.with_name(tar_file.name + ".zst")

    assert expected.exists()
    assert expected.stat().st_size > 0

    dctx = zstd.ZstdDecompressor()

    with open(expected, "rb") as f:
        with dctx.stream_reader(f) as reader:
            decompressed = reader.read()

    assert original_content == decompressed
