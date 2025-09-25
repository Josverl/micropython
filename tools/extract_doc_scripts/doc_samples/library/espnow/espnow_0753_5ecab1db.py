# Source: library\espnow.rst:753
# Type: code_block

bcast = b"\xff" * 6
e.add_peer(bcast)
e.send(bcast, "Hello World!")
