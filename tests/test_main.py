import sys

import pytest

from main import main


def test_missing_required_flag_raises_system_exit(monkeypatch, capsys):

    monkeypatch.setattr(sys, "argv", ["main.py", "arch-wiki-docs.pkg.tar.zst"])

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()

    assert "Please specify at least one flag: -t, -z, or --zt" in captured.err
