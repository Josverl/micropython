#!/usr/bin/env python3
"""Pytest replacements for legacy test_fs_tree.sh."""

from __future__ import annotations

from pathlib import Path

import pytest
from helpers import run_mpremote

RAMDISK_TEMPLATE = """
class RAMBlockDev:
    def __init__(self, block_size, num_blocks):
        self.block_size = block_size
        self.data = bytearray(block_size * num_blocks)

    def readblocks(self, block_num, buf):
        for i in range(len(buf)):
            buf[i] = self.data[block_num * self.block_size + i]

    def writeblocks(self, block_num, buf):
        for i in range(len(buf)):
            self.data[block_num * self.block_size + i] = buf[i]

    def ioctl(self, op, arg):
        if op == 4:
            return len(self.data) // self.block_size
        if op == 5:
            return self.block_size

import os

bdev = RAMBlockDev(512, 50)
os.VfsFat.mkfs(bdev)
os.mount(bdev, '/ramdisk')
os.chdir('/ramdisk')
"""


def _mpremote(mpremote_cmd: list[str], *args: str, expect_ok: bool = True):
    result = run_mpremote(mpremote_cmd, *args)
    if expect_ok:
        assert result.returncode == 0, result.stderr
    return result


def _reset_ramdisk(mpremote_cmd: list[str], script_path: Path) -> None:
    _mpremote(mpremote_cmd, "run", str(script_path))


@pytest.fixture
def ramdisk_script(tmp_path: Path) -> Path:
    script_path = tmp_path / "ramdisk_tree.py"
    script_path.write_text(RAMDISK_TEMPLATE, encoding="utf-8")
    return script_path


def _has_line(output: str, expected: str) -> bool:
    """Check if stdout contains a line equal to the expected text."""
    return any(line.strip() == expected for line in output.splitlines())


def _seed_small_tree(mpremote_cmd: list[str]) -> None:
    _mpremote(mpremote_cmd, "resume", "touch", ":a.py")
    _mpremote(mpremote_cmd, "resume", "touch", ":b.py")
    _mpremote(mpremote_cmd, "resume", "mkdir", ":foo")
    _mpremote(mpremote_cmd, "resume", "touch", ":foo/aa.py")
    _mpremote(mpremote_cmd, "resume", "touch", ":foo/ba.py")


def _seed_large_tree(mpremote_cmd: list[str]) -> None:
    _seed_small_tree(mpremote_cmd)
    _mpremote(mpremote_cmd, "resume", "mkdir", ":bar")
    _mpremote(mpremote_cmd, "resume", "touch", ":bar/aaa.py")
    _mpremote(mpremote_cmd, "resume", "touch", ":bar/bbbb.py")
    _mpremote(mpremote_cmd, "resume", "mkdir", ":bar/baz")
    _mpremote(mpremote_cmd, "resume", "touch", ":bar/baz/aaa.py")
    _mpremote(mpremote_cmd, "resume", "touch", ":bar/baz/bbbb.py")
    _mpremote(mpremote_cmd, "resume", "mkdir", ":bar/baz/quux")
    _mpremote(mpremote_cmd, "resume", "touch", ":bar/baz/quux/aaa.py")
    _mpremote(mpremote_cmd, "resume", "touch", ":bar/baz/quux/bbbb.py")
    _mpremote(mpremote_cmd, "resume", "mkdir", ":bar/baz/quux/xen")
    _mpremote(mpremote_cmd, "resume", "touch", ":bar/baz/quux/xen/aaa.py")


@pytest.mark.cli
def test_tree_empty_and_basic(mpremote_cmd, cli_mode, ramdisk_script):
    _reset_ramdisk(mpremote_cmd, ramdisk_script)

    result = _mpremote(mpremote_cmd, "resume", "tree", ":")
    assert ":/ramdisk" in result.stdout
    assert "a.py" not in result.stdout

    _seed_small_tree(mpremote_cmd)
    result = _mpremote(mpremote_cmd, "resume", "tree", ":")
    assert "foo" in result.stdout
    assert "aa.py" in result.stdout

    for path in [None, ".", ":."]:
        args = ["resume", "tree"]
        if path:
            args.append(path)
        result = _mpremote(mpremote_cmd, *args)
        assert "foo" in result.stdout


@pytest.mark.cli
def test_tree_multiple_paths(mpremote_cmd, cli_mode, ramdisk_script):
    _reset_ramdisk(mpremote_cmd, ramdisk_script)
    _seed_large_tree(mpremote_cmd)

    result = _mpremote(mpremote_cmd, "resume", "tree", ":")
    assert "bar" in result.stdout
    assert "quux" in result.stdout

    result = _mpremote(mpremote_cmd, "resume", "tree", ":foo")
    assert _has_line(result.stdout, ":foo")
    assert result.stdout.count("aa.py") == 1

    out_bar = _mpremote(mpremote_cmd, "resume", "tree", ":bar")
    assert _has_line(out_bar.stdout, ":bar")
    assert "xen" in out_bar.stdout

    out_sub = _mpremote(mpremote_cmd, "resume", "tree", ":bar/baz")
    assert ":bar/baz" in out_sub.stdout
    assert out_sub.stdout.count("bbb") >= 1

    mount = _mpremote(mpremote_cmd, "resume", "tree", ":/ramdisk")
    assert mount.stdout.count("foo") > 0


@pytest.mark.cli
def test_tree_errors(mpremote_cmd, cli_mode, ramdisk_script):
    _reset_ramdisk(mpremote_cmd, ramdisk_script)
    _seed_small_tree(mpremote_cmd)

    result = _mpremote(mpremote_cmd, "resume", "tree", ":not_there", expect_ok=False)
    assert "not a directory" in (result.stdout + result.stderr)

    result = _mpremote(mpremote_cmd, "resume", "tree", ":a.py", expect_ok=False)
    assert "not a directory" in (result.stdout + result.stderr)


@pytest.mark.cli
def test_tree_size_outputs(mpremote_cmd, cli_mode, ramdisk_script, tmp_path):
    _reset_ramdisk(mpremote_cmd, ramdisk_script)
    _seed_large_tree(mpremote_cmd)

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    for name, size in [
        ("file1.txt", 20),
        ("file2.txt", 204),
        ("file3.txt", 1096),
        ("file4.txt", 2192),
    ]:
        (data_dir / name).write_bytes(b"0" * size)

    _mpremote(mpremote_cmd, "resume", "cp", "-r", str(data_dir), ":")

    out = _mpremote(mpremote_cmd, "resume", "tree", "-s", ":")
    assert "[       20]" in out.stdout
    assert "data" in out.stdout

    out_default = _mpremote(mpremote_cmd, "resume", "tree", "-s")
    assert "file3.txt" in out_default.stdout

    out_human = _mpremote(mpremote_cmd, "resume", "tree", "--human", ":")
    assert "1.1K" in out_human.stdout or "1.1k" in out_human.stdout

    result = _mpremote(mpremote_cmd, "resume", "tree", "-s", "--human", ":", expect_ok=False)
    assert "not allowed" in (result.stdout + result.stderr)
