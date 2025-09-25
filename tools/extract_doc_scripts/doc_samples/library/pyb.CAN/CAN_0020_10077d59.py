# Source: library\pyb.CAN.rst:20
# Type: code_block

# FD frame + BRS mode + Extended frame ID. 500 Kbit/s for arbitration phase, 1Mbit/s for data phase.
can = CAN(1, CAN.NORMAL, baudrate=500_000, brs_baudrate=1_000_000, sample_point=80)
can.setfilter(0, CAN.RANGE, 0, (0xFFF0, 0xFFFF))
can.send("a" * 64, 0xFFFF, fdf=True, brs=True, extframe=True)
can.recv(0)
