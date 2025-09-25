# Source: library\rp2.DMA.rst:21
# Type: code_block
# Platform: rp2

a = bytearray(32 * 1024)
b = bytearray(32 * 1024)
d = rp2.DMA()
c = d.pack_ctrl()  # Just use the default control value.
# The count is in 'transfers', which defaults to four-byte words, so divide length by 4
d.config(read=a, write=b, count=len(a) // 4, ctrl=c, trigger=True)
# Wait for completion
while d.active():
    pass
