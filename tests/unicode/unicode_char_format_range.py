# test bounds checking for %c and {:c} formatting (issue #13084)
# tests that invalid character codes are rejected

# test valid maximum Unicode code point
print("%c" % 0x10FFFF)
print("{:c}".format(0x10FFFF))

# test that negative values are rejected
try:
    print("%c" % -1)
except ValueError:
    print("ValueError: negative")

try:
    print("{:c}".format(-1))
except ValueError:
    print("ValueError: negative")

# test that values beyond max Unicode are rejected
try:
    print("%c" % 0x110000)
except ValueError:
    print("ValueError: beyond max")

try:
    print("{:c}".format(0x110000))
except ValueError:
    print("ValueError: beyond max")

# test with f-strings
try:
    c = -1
    print(f"{c:c}")
except ValueError:
    print("ValueError: f-string negative")

try:
    c = 0x110000
    print(f"{c:c}")
except ValueError:
    print("ValueError: f-string beyond max")
