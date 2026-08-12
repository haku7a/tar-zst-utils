import sys
from pathlib import Path

import pytest

from main import main


def test_missing_required_flag_raises_system_exit(monkeypatch, capsys, zstd_file: Path):

    print(zstd_file)

    monkeypatch.setattr(sys, "argv", ["main.py", str(zstd_file)])

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()

    assert "Please specify at least one flag: -t, -z, or --zt" in captured.err


def test_missing_file_causes_exit(monkeypatch, capsys):

    monkeypatch.setattr(sys, "argv", ["main.py", "--zt", "arch-docs.pkg.tar.zst"])

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()

    assert "File not found:" in captured.err


def verify_decompressed_file(zstd_file, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "-z", str(zstd_file[1])])

    main()

    txt_path_file = zstd_file[0] / "file.txt"

    with open(txt_path_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == "Hello"
