# Check if unicode validation is enabled (requires MICROPY_PY_BUILTINS_STR_UNICODE_CHECK)
try:
    b'\xff'.decode()
except UnicodeError:
    pass
else:
    print("SKIP")
    raise SystemExit

try:
    f = open("data/utf-8_invalid.txt", encoding="utf-8")
    f.read()
except UnicodeError:
    print("UnicodeError")
