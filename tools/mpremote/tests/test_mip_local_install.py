#!/usr/bin/env python3
"""Pytest replacements for legacy test_mip_local_install.sh."""

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

bdev = RAMBlockDev({block_size}, {num_blocks})
os.VfsFat.mkfs(bdev)
os.mount(bdev, '{target}')
"""


def _write_example_package(root: Path, package: str) -> tuple[Path, Path]:
    base = root / "example"
    module = base / package
    module.mkdir(parents=True, exist_ok=True)
    (module / "hello.py").write_text("def hello(): print('Hello, world!')\n", encoding="utf-8")
    (module / "__init__.py").write_text("from .hello import hello\n", encoding="utf-8")
    package_json = base / "package.json"
    package_json.write_text(
        (
            "{\n"
            '    "urls": [\n'
            f'        ["{package}/__init__.py", "{package}/__init__.py"],\n'
            f'        ["{package}/hello.py", "{package}/hello.py"]\n'
            "    ],\n"
            '    "version": "0.2"\n'
            "}\n"
        ),
        encoding="utf-8",
    )
    return base, package_json


@pytest.mark.cli
def test_mip_install_from_local_sources(mpremote_cmd, cli_mode, tmp_path):
    target = "/__ramdisk"
    block_size = 512
    num_blocks = 50
    package = "mip_example"

    base_dir, manifest = _write_example_package(tmp_path, package)
    ramdisk_script = tmp_path / "ramdisk.py"
    ramdisk_script.write_text(
        RAMDISK_TEMPLATE.format(block_size=block_size, num_blocks=num_blocks, target=target),
        encoding="utf-8",
    )

    result = run_mpremote(mpremote_cmd, "run", str(ramdisk_script))
    assert result.returncode == 0, result.stderr

    result = run_mpremote(mpremote_cmd, "resume", "mkdir", f"{target}/lib")
    assert result.returncode == 0, result.stderr

    result = run_mpremote(
        mpremote_cmd,
        "resume",
        "mip",
        "install",
        f"--target={target}/lib",
        str(manifest),
    )
    assert result.returncode == 0, result.stderr
    stdout = result.stdout
    assert "Installing:" in stdout
    assert f"{target}/lib/{package}/__init__.py" in stdout

    init_path = f"{target}/lib"
    result = run_mpremote(
        mpremote_cmd,
        "resume",
        "exec",
        f"import sys; sys.path.append('{init_path}')",
    )
    assert result.returncode == 0, result.stderr

    result = run_mpremote(
        mpremote_cmd,
        "resume",
        "exec",
        f"import {package}; {package}.hello()",
    )
    assert result.returncode == 0, result.stderr
    assert "Hello, world!" in result.stdout
