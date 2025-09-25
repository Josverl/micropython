# Source: renesas-ra\quickref.rst:188
# Type: code_block

UART.init(baudrate)  # now only 115200 is confirmed
UART.init(cts, rts)  # Pins are fixed.
UART.init(invert)
UART.init(tx, rx)  # Pins are fixed.
UART.init(txbuf)
UART.init(flow)
UART.irq(handler)
UART.irq(trigger=RX_ANY)
UART.irq(priority)
UART.irq(wake=machine.IDLE)
