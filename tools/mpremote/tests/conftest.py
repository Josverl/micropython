import pytest

from pytest_utils import get_devices


def pytest_addoption(parser):
    group = parser.getgroup("mpremote")
    # Pytest reserves lowercase short options in the public plugin API.
    # Use -t for consistency with other MicroPython test tools.
    group._addoption(
        "-t",
        "--device",
        action="append",
        dest="mpremote_devices",
        metavar="DEVICE",
        help="mpremote device (a0, u0, c1, port, or URL); may be repeated",
    )


def pytest_generate_tests(metafunc):
    if "device" not in metafunc.fixturenames:
        return

    devices = get_devices(metafunc.config.getoption("mpremote_devices"))
    if devices:
        metafunc.parametrize("device", devices, ids=devices)
    else:
        metafunc.parametrize(
            "device",
            [pytest.param(None, marks=pytest.mark.skip(reason="no mpremote device configured"))],
        )


def pytest_report_header(config):
    devices = get_devices(config.getoption("mpremote_devices"))
    if devices:
        return "mpremote devices: {}".format(", ".join(devices))
    return "mpremote devices: none (set MPREMOTE_DEVICE)"
