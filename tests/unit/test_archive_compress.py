import argparse

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
