import argparse
from pathlib import Path

import pytest

from commands.archive_compress import archive_compress


def _make_args(file, output=None, level=3, threads=0):
    return argparse.Namespace(
        file=str(file),
        output=output,
        level=level,
        threads=threads,
    )


def test_creates_non_empty_tar_zst_archive(text_file):
    args = _make_args(text_file)
    archive_compress(args)
    expected = text_file.with_name(text_file.name + ".tar.zst")

    assert expected.exists()
    assert expected.stat().st_size > 0


def test_creates_archive_with_custom_output(text_file: Path) -> None:
    output_path = text_file.parent / "test_name.txt.tar.zst"

    args = _make_args(text_file, output=str(output_path))
    archive_compress(args)

    assert output_path.exists()


def test_raises_error_if_input_file_missing(tmp_path) -> None:
    missing_file = tmp_path / "missing.txt"
    args = _make_args(missing_file)

    with pytest.raises(FileNotFoundError):
        archive_compress(args)
