#!/usr/bin/env python3
"""Pytest replacements for legacy test_errno.sh."""

from pathlib import Path

import pytest
from helpers import run_mpremote

ERROR_SCRIPT = """
import os, vfs, errno

class ErrorFS:
    def __init__(self):
        self.error = Exception()

    def mount(self, *a, **k):
        pass

    def umount(self, *a, **k):
        pass

    def chdir(self, *a, **k):
        pass

    def open(self, *a, **k):
        raise self.error

fs = ErrorFS()
vfs.mount(fs, '/fs')
os.chdir('/fs')
"""

ERROR_EXPECTATIONS = {
    "ENOENT": "No such file or directory",
    "EISDIR": "Is a directory",
    "EEXIST": "File exists",
    "ENODEV": "No such device",
    "EINVAL": "Invalid argument",
    "EPERM": "Operation not permitted",
    "EOPNOTSUPP": "Operation not supported",
}


@pytest.mark.cli
def test_errno_mappings(mpremote_cmd, cli_mode, tmp_path):
    script_path = tmp_path / "errorfs.py"
    script_path.write_text(ERROR_SCRIPT, encoding="utf-8")

    result = run_mpremote(mpremote_cmd, "run", str(script_path))
    assert result.returncode == 0, result.stderr

    result = run_mpremote(mpremote_cmd, "resume", "exec", "fs.error = Exception()")
    assert result.returncode == 0, result.stderr

    result = run_mpremote(mpremote_cmd, "resume", "cat", ":Exception.py")
    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "Error with transport" in combined or "mpremote:" in combined

    for name, message in ERROR_EXPECTATIONS.items():
        result = run_mpremote(
            mpremote_cmd,
            "resume",
            "exec",
            f"import errno; fs.error = OSError(errno.{name}, '')",
        )
        assert result.returncode == 0, result.stderr

        result = run_mpremote(mpremote_cmd, "resume", "cat", f":{name}.py")
        combined = result.stdout + result.stderr
        assert result.returncode != 0
        assert f"{name}.py" in combined
        assert message in combined

    result = run_mpremote(mpremote_cmd, "resume", "exec", "vfs.umount('/fs')")
    assert result.returncode == 0, result.stderr
