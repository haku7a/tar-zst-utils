import tarfile
from pathlib import Path

import pytest


@pytest.fixture
def text_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("sample text")
    return file_path


@pytest.fixture
def tar_file(text_file: Path) -> Path:

    output_path = text_file.parent / "tar_file.tar"
    with tarfile.open(output_path, mode="w") as tar:
        tar.add(text_file, arcname=text_file.name)

    return output_path
