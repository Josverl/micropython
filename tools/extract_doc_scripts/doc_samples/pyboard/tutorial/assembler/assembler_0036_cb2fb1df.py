# Source: pyboard\tutorial\assembler.rst:36
# Type: code_block
# Platform: unix


@micropython.asm_thumb
def led_on():
    movwt(r0, stm.GPIOA)
    movw(r1, 1 << 13)
    strh(r1, [r0, stm.GPIO_BSRRL])
