#!/usr/bin/env python3
"""Pytest replacements for legacy test_mount.sh."""

from pathlib import Path

import pytest
from helpers import run_mpremote


def _write_package(root: Path) -> Path:
    pkg = root / "mount_package"
    sub = pkg / "subpackage"
    sub.mkdir(parents=True, exist_ok=True)
    (pkg / "__init__.py").write_text(
        "from .x import x\nfrom .subpackage import y\n", encoding="utf-8"
    )
    (pkg / "x.py").write_text("def x():\n  print('x')\n", encoding="utf-8")
    (sub / "__init__.py").write_text("from .y import y\n", encoding="utf-8")
    (sub / "y.py").write_text("def y():\n  print('y')\n", encoding="utf-8")
    return pkg


@pytest.mark.cli
def test_mount_execution_from_local_tree(mpremote_cmd, cli_mode, tmp_path):
    pkg = _write_package(tmp_path)
    result = run_mpremote(
        mpremote_cmd,
        "mount",
        str(tmp_path),
        "exec",
        "import mount_package; mount_package.x(); mount_package.y()",
    )
    assert result.returncode == 0, result.stderr
    assert "x" in result.stdout and "y" in result.stdout
    assert "Local directory" in result.stdout
    assert str(tmp_path) in result.stdout
    assert pkg.exists()


@pytest.mark.cli
def test_mount_writes_propagate_locally(mpremote_cmd, cli_mode, tmp_path):
    target = tmp_path / "test.txt"
    result = run_mpremote(
        mpremote_cmd,
        "mount",
        str(tmp_path),
        "exec",
        "open('test.txt', 'w').write('hello world\\n')",
    )
    assert result.returncode == 0, result.stderr
    assert target.read_text(encoding="utf-8").strip() == "hello world"
    assert "Local directory" in result.stdout


@pytest.mark.cli
def test_remote_file_readlines(mpremote_cmd, cli_mode, tmp_path):
    target = tmp_path / "test.txt"
    target.write_text("hello world\n", encoding="utf-8")

    result = run_mpremote(
        mpremote_cmd,
        "mount",
        str(tmp_path),
        "exec",
        "print(open('test.txt').readlines())",
    )
    assert result.returncode == 0, result.stderr
    assert "['hello world\\n']" in result.stdout
    assert "Local directory" in result.stdout
