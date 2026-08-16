import argparse

from commands.archive_compress import archive_compress


def test_creates_tar_zst_archive(text_file):
    args = argparse.Namespace(file=str(text_file), level=15, threads=0, output=None)
    archive_compress(args)
    expected = text_file.with_name(text_file.name + ".tar.zst")

    assert expected.exists()
