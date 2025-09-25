# Source: reference\constrained.rst:222
# Type: code_block


def foo(bar):
    for x in bar:
        print(x)


foo([1, 2, 0xFF])
foo((1, 2, 0xFF))
foo(b"\1\2\xff")
