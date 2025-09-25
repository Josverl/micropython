# Source: rp2\quickref.rst:84
# Type: code_block
# Platform: esp32


def do_connect():
    import machine, network

    wlan = network.WLAN()
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect("ssid", "key")
        while not wlan.isconnected():
            machine.idle()
    print("network config:", wlan.ipconfig("addr4"))
