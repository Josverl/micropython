import fnmatch
import platform
import subprocess
import time
from functools import cache
from typing import List, Optional, Tuple

import keyboard
import pytest
from mpremote.transport_serial import SerialTransport
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo

# mark all tests
# pytestmark = [pytest.mark.mpremote, pytest.mark.serial]


@cache
def all_connected_devices() -> List[Tuple[str, str]]:
    "List serial ports with attached devices and mcu_port."
    # devices = [p.device for p in serial.tools.list_ports.comports()]
    devices = [p.device for p in filtered_comports()]

    d2: List[Tuple[str, str]] = []
    for ser_port in devices:
        cmd = ["mpremote", "connect", ser_port, "exec", "import sys;print(sys.platform)"]
        spr = subprocess.run(cmd, capture_output=True, universal_newlines=True, timeout=5)
        mcu_port = spr.stdout.strip()
        if "no device found" in mcu_port:
            continue
        if "failed to access" in mcu_port:
            continue
        d2.append((mcu_port, ser_port))
    # optionally filter the list of devices
    return sorted(d2)


def filtered_comports(
    ignore: Optional[List[str]] = None,
    include: Optional[List[str]] = None,
    bluetooth: bool = False,
) -> List[ListPortInfo]: 
    """
    Get a list of filtered comports using the include and ignore lists.
    both can be globs (e.g. COM*) or exact port names (e.g. COM1)
    """
    if not ignore:
        ignore = []
    elif not isinstance(ignore, list):  # type: ignore
        ignore = list(ignore)
    if not include:
        include = ["*"]
    elif not isinstance(include, list):  # type: ignore
        include = list(include)

    if ignore == [] and platform.system() == "Darwin":
        # By default ignore some of the irrelevant ports on macOS
        ignore = [
            "/dev/*.debug-console",
        ]

    # remove ports that are to be ignored
    print(f"{include=}, {ignore=}, {bluetooth=}")

    comports = [p for p in list_ports.comports() if not any(fnmatch.fnmatch(p.device, i) for i in ignore)]

    if platform.system() == "Linux":
        # use p.location to filter out the bogus ports on newer Linux kernels
        # filter out the bogus ports on newer Linux kernels
        comports = [p for p in comports if p.location]

    print(f"comports: {[p.device for p in comports]}")
    # remove bluetooth ports

    if include != ["*"]:
        # if there are explicit ports to include, add them to the list
        explicit = [p for p in list_ports.comports() if any(fnmatch.fnmatch(p.device, i) for i in include)]
        print(f"explicit: {[p.device for p in explicit]}")
        if ignore == []:
            # if nothing to ignore, just use the explicit list as a sinple sane default
            comports = explicit
        else:
            # if there are ports to ignore, add the explicit list to the filtered list
            comports = list(set(explicit) | set(comports))
    if platform.system() == "Darwin":
        # Failsafe: filter out debug-console ports
        comports = [p for p in comports if not p.description.endswith(".debug-console")]

    if not bluetooth:
        # filter out bluetooth ports
        comports = [p for p in comports if "bluetooth" not in p.description.lower()]
        comports = [p for p in comports if "BTHENUM" not in p.hwid]
        if platform.system() == "Darwin":
            comports = [p for p in comports if ".Bluetooth" not in p.device]
            # filter out ports with no hwid
            comports = [p for p in comports if p.hwid != "n/a"]
    print(f"filtered_comports: {[p.device for p in comports]}")
    # sort
    if platform.system() == "Windows":
        # Windows sort of comports by number - but fallback to device name
        return sorted(
            comports,
            key=lambda x: int(x.device.split()[0][3:]) if x.device.split()[0][3:].isdigit() else x,
        )
    # sort by device name
    return sorted(comports, key=lambda x: x.device)




def reset_mcu(ser_port):
    """perform a MPRemote hard reset on a MCU"""

    base = ["mpremote", "connect", ser_port] if ser_port else ["mpremote"]
    spr = subprocess.run(base + ["reset"], capture_output=True, universal_newlines=True, timeout=5)
    output = spr.stdout
    if "no device found" in output:
        return "no device found"
    if "failed to access" in output:
        return "failed to access"
    assert spr.returncode == 0
    # allow 2 secs for MCU hard reset to complete
    time.sleep(2)
    return "OK"


@pytest.mark.parametrize("mcu_port, ser_port", all_connected_devices())
@pytest.mark.parametrize("reset", ["no_reset", "hard_reset"])
def test_mpremote_eval(reset, mcu_port, ser_port):
    if reset == "hard_reset":
        # initial hard reset
        result = reset_mcu(ser_port)
        if result != "OK":
            pytest.skip(result)

    base = ["mpremote", "connect", ser_port] if ser_port else ["mpremote"]
    cmd = base + ["eval", "21+21"]
    spr = subprocess.run(cmd, capture_output=True, universal_newlines=True, timeout=5)
    assert spr.returncode == 0
    output = spr.stdout.strip()
    assert output == "42"


@pytest.mark.parametrize("mcu_port, ser_port", all_connected_devices())
@pytest.mark.parametrize("reset", ["no_reset", "hard_reset"])
def test_mpremote_no_reset_on_disconnect(reset, mcu_port, ser_port):
    """
    Validate that mpremote does not issue a hard reset when terminating a session
    Requires that the MCU device does not have a 'main.py' file that runs in a loop.
    """
    if reset == "hard_reset":
        # initial hard reset
        result = reset_mcu(ser_port)
        if result != "OK":
            pytest.skip(result)

    # test that resume does not issue a hard reset between connects
    if ser_port:
        base = ["mpremote", "connect", ser_port, "resume"]
    else:
        base = ["mpremote", "resume"]

    cmd = base + ["resume", "exec", "x=1"]
    for n in range(1, 4):
        spr = subprocess.run(cmd, capture_output=True, universal_newlines=True, timeout=5)
        assert spr.returncode == 0
        output = spr.stdout
        print(f"Port {ser_port}, Test {n} : {output}")
        if "," in output:
            assert output.split(",")[0].strip() == str(n)
        mpy_cmd = "x = (x+1 if 'x' in dir() else 1);import sys;print(x, ',', sys.platform)"
        cmd = base + ["resume", "exec", mpy_cmd]


@pytest.mark.manual
@pytest.mark.parametrize("mcu_port, ser_port", all_connected_devices())
def test_espxx_rst_no_download(capsys, ser_port: str, mcu_port: str):
    # sourcery skip: invert-any-all
    TIME_OUT = 10
    if not mcu_port.lower().startswith("esp"):
        pytest.skip("Not an ESPxx device")
    device = SerialTransport(ser_port)
    flush = device.serial.read_all()
    with capsys.disabled():
        t_start = time.time()
        print("\n======================================================")
        print(
            f"Press the reset button on {mcu_port} connected to {ser_port} and [tap the spacebar]: "
            f"\nto continue or wait {TIME_OUT} seconds to skip this test."
        )
        while 1 and (time.time() - t_start) <= TIME_OUT:
            time.sleep(0.01)
            if keyboard.is_pressed("space"):
                while keyboard.is_pressed("space"):
                    time.sleep(0.01)
                break
        if (time.time() - t_start) > TIME_OUT:
            print("No human detected.")  # need someone to press the reset button
            print("======================================================\n")
            pytest.skip("No human detected.")  # need someone to press the reset button
        time.sleep(3)  # give the MCU time to reset
        output = device.serial.read_all()
        output = output.decode(errors="ignore")
        print(output)
        print("\n======================================================\n")

    # capture this
    print("\n======================================================\n")
    print(output)
    print("\n======================================================\n")

    # messages indicating the board is waiting for a firmware download
    IN_DL = [
        "DOWNLOAD_BOOT",
        "waiting for download",
        "boot mode:(1,",
        "waiting for host",
        "DOWNLOAD(USB",
    ]
    # messages indicating the board is booting up or running micropython
    NO_DL = [
        "SPI_FAST_FLASH_BOOT",
        'Type "help()" for more information.',
        ">>>",
    ]

    # NOT download message detected
    assert not any(
        msg in output for msg in IN_DL
    ), f"Board waiting for firmware download to board.\n{output}"

    # micropython detected
    assert any(msg in output for msg in NO_DL), f"Micropython not detected.\n{output}"
