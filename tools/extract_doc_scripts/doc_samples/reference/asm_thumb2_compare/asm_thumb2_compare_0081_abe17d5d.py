# Source: reference\asm_thumb2_compare.rst:81
# Type: code_block

cmp(r0, r1)
ite(eq)
mov(r0, 100)  # runs if r0 == r1
mov(r0, 200)  # runs if r0 != r1
# execution continues here
