import os
import subprocess
import sys
from pathlib import Path


MPREMOTE = Path(__file__).resolve().parent.parent / "mpremote.py"


def normalize_device(device):
    if len(device) > 1 and device[1:].isdigit():
        prefix = device[0]
        if prefix == "a":
            return "/dev/ttyACM" + device[1:]
        if prefix == "u":
            return "/dev/ttyUSB" + device[1:]
        if prefix == "c":
            return "COM" + device[1:]
    return device


def get_devices(devices=None):
    if devices is None:
        value = os.environ.get("MPREMOTE_DEVICE", "")
        devices = value.split(",")
    return [normalize_device(device.strip()) for device in devices if device.strip()]


def run_mpremote(device, *args, encoding="utf-8", child_encoding=None):
    command = [sys.executable, str(MPREMOTE), "connect", device, *args]
    env = os.environ.copy()
    if child_encoding:
        env["PYTHONIOENCODING"] = child_encoding
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding=encoding,
        errors="replace",
        timeout=30,
        env=env,
    )


def run_mpremote_bytes(device, *args):
    command = [sys.executable, str(MPREMOTE), "connect", device, *args]
    return subprocess.run(
        command,
        capture_output=True,
        timeout=30,
        env=os.environ.copy(),
    )


def require_success(result):
    """Assert that an mpremote subprocess succeeded, reporting its stderr."""
    assert result.returncode == 0, result.stderr
