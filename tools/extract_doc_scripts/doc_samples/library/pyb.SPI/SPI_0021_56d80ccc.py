# Source: library\pyb.SPI.rst:21
# Type: code_block

data = spi.send_recv(b"1234")  # send 4 bytes and receive 4 bytes
buf = bytearray(4)
spi.send_recv(b"1234", buf)  # send 4 bytes and receive 4 into buf
spi.send_recv(buf, buf)  # send/recv 4 bytes from/to buf
