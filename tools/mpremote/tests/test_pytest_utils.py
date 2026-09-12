import subprocess

import pytest

from pytest_utils import get_devices, normalize_device, require_success


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("a0", "/dev/ttyACM0"),
        ("u12", "/dev/ttyUSB12"),
        ("c3", "COM3"),
        ("/dev/ttyACM0", "/dev/ttyACM0"),
        ("rfc2217://localhost:2217", "rfc2217://localhost:2217"),
    ],
)
def test_normalize_device(value, expected):
    assert normalize_device(value) == expected


def test_command_line_devices_override_environment(monkeypatch):
    monkeypatch.setenv("MPREMOTE_DEVICE", "a1,u1")
    assert get_devices(["c3", "a0"]) == ["COM3", "/dev/ttyACM0"]


def test_environment_devices_are_normalized(monkeypatch):
    monkeypatch.setenv("MPREMOTE_DEVICE", "a1, u2")
    assert get_devices() == ["/dev/ttyACM1", "/dev/ttyUSB2"]


def test_plural_environment_variable_is_ignored(monkeypatch):
    monkeypatch.delenv("MPREMOTE_DEVICE", raising=False)
    monkeypatch.setenv("MPREMOTE_DEVICES", "a1,u2")
    assert get_devices() == []


def test_require_success():
    require_success(subprocess.CompletedProcess([], 0, stderr=""))

    with pytest.raises(AssertionError, match="mpremote failed"):
        require_success(subprocess.CompletedProcess([], 1, stderr="mpremote failed"))
