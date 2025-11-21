#!/usr/bin/env python3
"""Pytest replacements for legacy test_recursive_cp.sh."""

from pathlib import Path

import pytest
from helpers import run_mpremote


def _setup_tree(root: Path) -> Path:
    src = root / "a"
    (src / "b").mkdir(parents=True, exist_ok=True)
    (src / "x.py").write_text("print('x')\n", encoding="utf-8")
    (src / "b" / "y.py").write_text("print('y')\n", encoding="utf-8")
    (root / "y.py").write_text("print('loose')\n", encoding="utf-8")
    return src


def _assert_has_files(folder: Path) -> None:
    assert (folder / "x.py").is_file()
    assert (folder / "b" / "y.py").is_file()


@pytest.mark.cli
def test_recursive_cp_to_missing_destination(mpremote_cmd, cli_mode, tmp_path):
    src = _setup_tree(tmp_path)

    commands = [
        ("cp", "--no-verbose", "-r", str(src), str(tmp_path / "b1")),
        ("cp", "--no-verbose", "-r", f"{src}/", str(tmp_path / "b2")),
        ("cp", "--no-verbose", "-r", str(src), f"{tmp_path / 'b3'}/"),
        ("cp", "--no-verbose", "-r", f"{src}/", f"{tmp_path / 'b4'}/"),
    ]
    for args in commands:
        result = run_mpremote(mpremote_cmd, *args)
        assert result.returncode == 0, result.stderr

    for target in ["b1", "b2", "b3", "b4"]:
        _assert_has_files(tmp_path / target)


@pytest.mark.cli
def test_recursive_cp_into_existing_destination(mpremote_cmd, cli_mode, tmp_path):
    src = _setup_tree(tmp_path)
    for idx in range(1, 5):
        (tmp_path / f"c{idx}").mkdir()

    commands = [
        ("cp", "--no-verbose", "-r", str(src), str(tmp_path / "c1")),
        ("cp", "--no-verbose", "-r", f"{src}/", str(tmp_path / "c2")),
        ("cp", "--no-verbose", "-r", str(src), f"{tmp_path / 'c3'}/"),
        ("cp", "--no-verbose", "-r", f"{src}/", f"{tmp_path / 'c4'}/"),
    ]
    for args in commands:
        result = run_mpremote(mpremote_cmd, *args)
        assert result.returncode == 0, result.stderr

    for target in ["c1", "c2", "c3", "c4"]:
        _assert_has_files(tmp_path / target / "a")

    assert (tmp_path / "y.py").is_file()
