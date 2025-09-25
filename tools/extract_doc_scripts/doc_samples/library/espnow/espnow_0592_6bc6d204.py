# Source: library\espnow.rst:592
# Type: code_block
# Platform: esp32

try:
    e.send(peer, "Hello")
except OSError as err:
    if len(err.args) < 2:
        raise err
    if err.args[1] == "ESP_ERR_ESPNOW_NOT_INIT":
        e.active(True)
    elif err.args[1] == "ESP_ERR_ESPNOW_NOT_FOUND":
        e.add_peer(peer)
    elif err.args[1] == "ESP_ERR_ESPNOW_IF":
        network.WLAN(network.WLAN.IF_STA).active(True)
    else:
        raise err
