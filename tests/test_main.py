import sys

import pytest

from main import main


def test_a(monkeypatch, capsys):

    monkeypatch.setattr(sys, "argv", ["main.py", "arch-wiki-docs.pkg.tar.zst"])

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()

    assert "Please specify at least one flag: -t, -z, or --zt" in captured.err
