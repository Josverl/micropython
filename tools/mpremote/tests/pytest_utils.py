import os
import subprocess
import sys
from pathlib import Path


MPREMOTE = Path(__file__).resolve().parent.parent / "mpremote.py"
TIMEOUT = 30

def normalize_device(device:str) -> str:
    """Expand a shorthand device name into its platform-specific path."""
    if len(device) > 1 and device[1:].isdigit():
        prefix = device[0]
        if prefix == "a":
            return "/dev/ttyACM" + device[1:]
        if prefix == "u":
            return "/dev/ttyUSB" + device[1:]
        if prefix == "c":
            return "COM" + device[1:]
    return device


def get_devices(devices: list[str] | None = None) -> list[str]:
    """Return normalized devices from provided arguments or the environment."""
    if devices is None:
        value = os.environ.get("MPREMOTE_DEVICE", "")
        devices = value.split(",")
    return [normalize_device(device.strip()) for device in devices if device.strip()]


def run_mpremote(device: str, *args: str, encoding: str = "utf-8", child_encoding: str | None = None) -> subprocess.CompletedProcess:
    """Run mpremote for a device and capture its decoded output."""
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
        timeout=TIMEOUT,
        env=env,
    )


def run_mpremote_bytes(device: str, *args: str) -> subprocess.CompletedProcess:
    """Run mpremote for a device and capture its raw byte output."""
    command = [sys.executable, str(MPREMOTE), "connect", device, *args]
    return subprocess.run(
        command,
        capture_output=True,
        timeout=TIMEOUT,
        env=os.environ.copy(),
    )


def assert_success(result:subprocess.CompletedProcess, message :str|None = None) -> None:
    """Assert that an mpremote subprocess succeeded, reporting its stderr."""
    assert result.returncode == 0, message or result.stderr
