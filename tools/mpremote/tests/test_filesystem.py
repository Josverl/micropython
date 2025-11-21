#!/usr/bin/env python3
"""Pytest replacements for legacy test_filesystem.sh."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest
from helpers import run_mpremote, write_script

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


class FilesystemRig:
    """Convenience wrapper to mirror the legacy shell test flow."""

    def __init__(self, mpremote_cmd: list[str], script_path: Path):
        self._cmd = mpremote_cmd
        self._script = script_path
        self.reset()

    def reset(self) -> None:
        _reset_ramdisk(self._cmd, self._script)

    def resume(self, *args: str, expect_ok: bool = True, env: dict[str, str] | None = None):
        return _mpremote(self._cmd, "resume", *args, env=env, expect_ok=expect_ok)

    def run(self, *args: str, expect_ok: bool = True, env: dict[str, str] | None = None):
        return _mpremote(self._cmd, *args, env=env, expect_ok=expect_ok)


@pytest.fixture
def ramdisk_script(tmp_path: Path) -> Path:
    script_path = tmp_path / "ramdisk.py"
    script_path.write_text(RAMDISK_TEMPLATE, encoding="utf-8")
    return script_path


@pytest.fixture
def filesystem_rig(mpremote_cmd, ramdisk_script):
    return FilesystemRig(mpremote_cmd, ramdisk_script)


def _reset_ramdisk(mpremote_cmd: list[str], script_path: Path) -> None:
    _mpremote(mpremote_cmd, "run", str(script_path))


def _mpremote(
    mpremote_cmd: list[str], *args: str, env: dict[str, str] | None = None, expect_ok: bool = True
):
    result = run_mpremote(mpremote_cmd, *args, env=env)
    if expect_ok:
        assert result.returncode == 0, result.stderr
    return result


def _write_local_file(path: Path, contents: str) -> None:
    path.write_text(contents, encoding="utf-8")


def _write_package(root: Path) -> Path:
    pkg = root / "package"
    sub = pkg / "subpackage"
    sub.mkdir(parents=True, exist_ok=True)
    _write_local_file(pkg / "__init__.py", "from .x import x\nfrom .subpackage import y\n")
    _write_local_file(pkg / "x.py", "def x():\n  print('x')\n")
    _write_local_file(sub / "__init__.py", "from .y import y\n")
    _write_local_file(sub / "y.py", "def y():\n  print('y')\n")
    return pkg


@pytest.mark.cli
def test_basic_file_operations(filesystem_rig: FilesystemRig, cli_mode, tmp_path):
    rig = filesystem_rig

    empty_hash = hashlib.sha256(b"").hexdigest()

    result = rig.resume("ls")
    assert "ls :" in result.stdout

    rig.resume("touch", ":a.py")
    rig.resume("touch", ":b.py")

    result = rig.resume("ls")
    assert "a.py" in result.stdout and "b.py" in result.stdout

    result = rig.resume("sha256sum", ":a.py")
    assert empty_hash in result.stdout

    local_script = tmp_path / "a.py"
    write_script(local_script, "print('Hello')\nprint('World')\n")

    rig.resume("cp", str(local_script), ":")
    rig.resume("cp", str(local_script), ":b.py")
    rig.resume("exec", "import a; import b")

    result = rig.resume("sha256sum", ":a.py")
    hash_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    device_hash = hash_lines[-1].split()[0]
    with open(local_script, "rb") as f:
        local_hash = hashlib.sha256(f.read()).hexdigest()
    assert device_hash == local_hash


@pytest.mark.cli
def test_directory_copy_and_force(filesystem_rig: FilesystemRig, cli_mode, tmp_path):
    rig = filesystem_rig

    local_script = tmp_path / "a.py"
    write_script(local_script, "print('Hello')\nprint('World')\n")

    rig.resume("cp", str(local_script), ":")
    rig.resume("mkdir", ":aaa")
    rig.resume("mkdir", ":bbb")

    rig.resume("cp", str(local_script), ":aaa")
    rig.resume("cp", str(local_script), ":bbb/b.py")

    rig.resume("cp", "-f", str(local_script), ":aaa")

    rig.resume("cp", str(local_script), ":aaa/")

    result = rig.resume("cp", str(local_script), ":aaa/a.py/", expect_ok=False)
    assert result.returncode != 0
    assert "not a directory" in (result.stdout + result.stderr)


@pytest.mark.cli
def test_removal_and_edit(filesystem_rig: FilesystemRig, cli_mode, tmp_path):
    rig = filesystem_rig

    local_script = tmp_path / "a.py"
    write_script(local_script, "print('Hello')\nprint('World')\n")

    rig.resume("cp", str(local_script), ":a.py")
    rig.resume("cp", str(local_script), ":d.py")
    rig.resume("mkdir", ":aaa")
    rig.resume("mkdir", ":bbb")
    rig.resume("cp", str(local_script), ":aaa/a.py")
    rig.resume("cp", str(local_script), ":bbb/b.py")

    result = rig.resume("rm", ":b.py", "c.py", expect_ok=False)
    assert "No such file" in (result.stdout + result.stderr)
    rig.resume("rm", ":aaa/a.py", "bbb/b.py")
    rig.resume("rmdir", ":aaa", ":bbb")

    # edit command should update file contents without relying on shell tools
    editor_script = tmp_path / "editor_replace.py"
    editor_script.write_text(
        "import pathlib, sys\n"
        "path = pathlib.Path(sys.argv[1])\n"
        "data = path.read_text()\n"
        "path.write_text(data.replace('Hello', 'Goodbye'))\n",
        encoding="utf-8",
    )
    editor_cmd = f"{sys.executable} {editor_script}"
    rig.resume("edit", ":d.py", env={"EDITOR": editor_cmd})
    result = rig.resume("exec", "import sys; print(open('d.py').read())")
    assert "Goodbye" in result.stdout
    rig.resume("exec", "import d")


@pytest.mark.cli
def test_recursive_package_copy(filesystem_rig: FilesystemRig, cli_mode, tmp_path):
    rig = filesystem_rig
    pkg = _write_package(tmp_path)

    # Base copy into root and validate
    rig.resume("cp", "-r", str(pkg), ":")
    result = rig.resume("ls", ":package")
    assert "__init__.py" in result.stdout
    result = rig.resume("exec", "import package; package.x(); package.y()")
    assert "x" in result.stdout and "y" in result.stdout

    # Fresh ramdisk for package2 scenario
    rig.reset()
    rig.resume("cp", "-r", str(pkg), ":package2")
    result = rig.resume("ls", ":package2")
    assert "__init__.py" in result.stdout

    # Another reset for the test/package2 block (matches shell script ordering)
    rig.reset()
    rig.resume("mkdir", ":test")
    rig.resume("cp", "-r", str(pkg), ":test")
    rig.resume("cp", "-r", str(pkg), ":test/package2")

    copy_dir = tmp_path / "copy"
    copy_dir.mkdir(exist_ok=True)
    rig.resume("cp", "-r", ":test/package", str(copy_dir))
    assert (copy_dir / "package" / "x.py").exists()

    rig.resume("cp", "-r", ":test/package", str(copy_dir / "package2"))
    assert (copy_dir / "package2" / "subpackage" / "y.py").exists()

    # Copy from device to another location on device
    rig.reset()
    rig.resume("cp", "-r", str(pkg), ":")
    rig.resume("cp", "-r", ":package", ":package3")

    rig.reset()
    rig.resume("cp", "-r", str(pkg), ":")
    rig.resume("mkdir", ":package4")
    rig.resume("cp", "-r", ":package", ":package4")

    # modify local file and re-copy
    _write_local_file(pkg / "subpackage" / "y.py", "def y():\n  print('y2')\n")
    rig.reset()
    rig.resume("cp", "-r", str(pkg), ":")
    result = rig.resume("exec", "import package; package.y()")
    assert "y2" in result.stdout


@pytest.mark.cli
def test_rm_recursive_scenarios(filesystem_rig: FilesystemRig, cli_mode, tmp_path):
    rig = filesystem_rig
    pkg = _write_package(tmp_path)

    for scenario in ["root", "subdir", "missing", "mount_relative", "mount_absolute"]:
        rig.reset()
        if scenario == "root":
            rig.resume("touch", ":a.py")
            rig.resume("touch", ":b.py")
            rig.resume("cp", "-r", str(pkg), ":")
            rig.resume("rm", "-r", "-v", ":")
        elif scenario == "subdir":
            rig.resume("touch", ":a.py")
            rig.resume("mkdir", ":testdir")
            rig.resume("cp", "-r", str(pkg), ":testdir/package")
            rig.resume("rm", "-r", ":testdir/package")
        elif scenario == "missing":
            rig.resume("ls")
            result = rig.resume("rm", "-r", ":nonexistent", expect_ok=False)
            assert result.returncode != 0
            assert "No such file" in (result.stdout + result.stderr)
        elif scenario == "mount_relative":
            rig.resume("touch", ":a.py")
            rig.resume("cp", "-r", str(pkg), ":")
            rig.resume("exec", "import os; os.chdir('/')")
            rig.resume("rm", "-r", "-v", ":ramdisk")
        elif scenario == "mount_absolute":
            rig.resume("touch", ":a.py")
            rig.resume("cp", "-r", str(pkg), ":")
            rig.resume("exec", "import os; os.chdir('/')")
            rig.resume("rm", "-r", "-v", ":/ramdisk")


@pytest.mark.cli
def test_mount_and_fs_errors(mpremote_cmd, cli_mode, tmp_path):
    _write_package(tmp_path)
    result = _mpremote(
        mpremote_cmd, "mount", str(tmp_path), "+", "rm", "-rv", ":package", expect_ok=False
    )
    assert result.returncode != 0
    assert "not permitted" in (result.stdout + result.stderr)

    result = _mpremote(mpremote_cmd, "fs", expect_ok=False)
    assert result.returncode != 0
    error_output = result.stdout + result.stderr
    assert "the following arguments are required: command, path" in error_output
