#!/usr/bin/env python3
import subprocess
from pick import pick, Option
from pathlib import Path

title = "Simple Setup for building MicroPython ports"
# TODO: parse list from tools/ci.sh
setups = [
    Option("CC3200", "cc3200"),
    Option("ESP32 idf50", "esp32_idf50"),
    Option("ESP8266", "esp8266"),
    Option("i.MXRT ", "mimxrt"),
    Option("NRF", "nrf"),
    Option("PIC 16bit", "pic16bit"),
    Option("PowerPC", "powerpc"),
    Option("Qemu ARM", "qemu_arm"),
    Option("Renesas ra", "renesas_ra"),
    Option("RP2", "rp2"),
    Option("SAMD", "samd"),
    Option("STM32", "stm32"),
    Option("Teensy", "teensy"),
    Option("Unix 32bit", "unix_32bit"),
    Option("Unix clang", "unix_clang"),
    Option("Unix Qemu ARM", "unix_qemu_arm"),
    Option("Unix Qemu MIPS", "unix_qemu_mips"),
    Option("Webassembly", "webassembly"),
    Option("Windows", "windows"),
    Option("Zephyr", "zephyr"),
]

try:
    # default to unix
    option, index = pick(setups, title, indicator="Install toolchain for =>", default_index=13)
    assert isinstance(option.value, str)

    #show the README if found
    readme = f"./ports/{option.value.split('_')[0]}/README.md"
    cmd_readme = f"code -r {readme}"
    if Path(readme).exists():
        subprocess.run(cmd_readme, shell=True, cwd="/workspaces/micropython")

    # run the ci setup for this port / variant
    cmd = f'bash -c "pwd&&source ./tools/ci.sh&&ci_{option.value}_setup"'
    subprocess.run(cmd, shell=True, cwd="/workspaces/micropython")


except KeyboardInterrupt:
    print("No worries, bye")
    exit(0)
