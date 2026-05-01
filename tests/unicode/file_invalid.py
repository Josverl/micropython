# Check if unicode validation is enabled (requires MICROPY_PY_BUILTINS_STR_UNICODE_CHECK)
try:
    b'\xff'.decode()
except UnicodeError:
    pass
else:
    print("SKIP")
    raise SystemExit

import unittest


class TestFileInvalidUtf8(unittest.TestCase):
    def test_read_invalid_utf8_raises(self):
        f = open("data/utf-8_invalid.txt", encoding="utf-8")
        with self.assertRaises(UnicodeError):
            f.read()


if __name__ == "__main__":
    unittest.main()
