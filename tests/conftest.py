from pathlib import Path

import pytest
import zstandard as zstd


@pytest.fixture(scope="session")
def zstd_file(tmp_path_factory: Path):

    data_dir = tmp_path_factory.mktemp("shared_data")

    txt = data_dir / "file.txt"
    txt.write_text("Hello", encoding="utf-8")

    compressed = zstd.ZstdCompressor(level=3).compress(txt.read_bytes())

    zstd_path = data_dir / "compress.zst"
    zstd_path.write_bytes(compressed)

    return data_dir, zstd_path
