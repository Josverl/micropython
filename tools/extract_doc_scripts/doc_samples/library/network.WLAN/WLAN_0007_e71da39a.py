# Source: library\network.WLAN.rst:7
# Type: code_block
# Platform: esp32

import network

# enable station interface and connect to WiFi access point
nic = network.WLAN(network.WLAN.IF_STA)
nic.active(True)
nic.connect("your-ssid", "your-key")
# now use sockets as usual
