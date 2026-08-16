import pytest


@pytest.fixture
def text_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("sample text")
    return file_path
