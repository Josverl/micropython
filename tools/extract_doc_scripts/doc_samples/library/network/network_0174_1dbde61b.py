# Source: library\network.rst:174
# Type: code_block

# Set WiFi access point name (formally known as SSID) and WiFi channel
ap.config(ssid="My AP", channel=11)
# Query params one by one
print(ap.config("ssid"))
print(ap.config("channel"))
