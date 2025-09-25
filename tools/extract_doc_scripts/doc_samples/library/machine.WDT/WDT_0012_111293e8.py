# Source: library\machine.WDT.rst:12
# Type: code_block

from machine import WDT

wdt = WDT(timeout=2000)  # enable it with a timeout of 2s
wdt.feed()
