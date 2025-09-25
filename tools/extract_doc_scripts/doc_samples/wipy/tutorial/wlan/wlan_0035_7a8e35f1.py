# Source: wipy\tutorial\wlan.rst:35
# Type: code_block
# Platform: esp32

import machine
from network import WLAN

wlan = WLAN(WLAN.IF_AP)

nets = wlan.scan()
for net in nets:
    if net.ssid == "mywifi":
        print("Network found!")
        wlan.connect(net.ssid, auth=(net.sec, "mywifikey"), timeout=5000)
        while not wlan.isconnected():
            machine.idle()  # save power while waiting
        print("WLAN connection succeeded!")
        break
