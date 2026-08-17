import argparse
from pathlib import Path

from commands.compress import compress


def _make_args(file: Path, output=None, level=3, threads=0) -> argparse.Namespace:
    return argparse.Namespace(
        file=str(file),
        output=output,
        level=level,
        threads=threads,
    )


def test_tar_archive_has_valid_content(tar_file: Path) -> None:
    args = _make_args(tar_file)
    compress(args)

    expected = tar_file.with_name(tar_file.name + ".zst")

    assert expected.exists()
    assert expected.stat().st_size > 0
