# Source: library\espnow.rst:550
# Type: code_block


def recv_cb(e):
    while True:  # Read out all messages waiting in the buffer
        mac, msg = e.irecv(0)  # Don't wait if no messages left
        if mac is None:
            return
        print(mac, msg)


e.irq(recv_cb)
