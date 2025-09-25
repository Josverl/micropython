# Source: esp8266\quickref.rst:68
# Type: code_block
# Platform: esp32


def do_connect():
    import network

    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect("ssid", "key")
        while not wlan.isconnected():
            pass
    print("network config:", wlan.ipconfig("addr4"))
