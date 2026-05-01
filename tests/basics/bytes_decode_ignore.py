# Test bytes.decode() with error handler 'ignore'

# Check if decode method is available (requires MICROPY_CPYTHON_COMPAT)
try:
    b''.decode()
except AttributeError:
    print("SKIP")
    raise SystemExit

# Check if unicode validation is enabled (requires MICROPY_PY_BUILTINS_STR_UNICODE_CHECK)
try:
    b'\xff'.decode()
except UnicodeError:
    pass
else:
    print("SKIP")
    raise SystemExit

# Check if error handlers are available (requires MICROPY_PY_BUILTINS_BYTES_DECODE_ERRORS)
try:
    b'\xff'.decode('utf-8', 'ignore')
except (UnicodeError, LookupError):
    print("SKIP")
    raise SystemExit

import unittest


class TestBytesDecodeIgnore(unittest.TestCase):
    # Test ignore mode with invalid UTF-8: invalid bytes should be silently dropped
    def test_invalid_bytes_ignored(self):
        self.assertEqual(b'\xff\xfe'.decode('utf-8', 'ignore'), '')

    # Test strict mode (default) still raises on invalid UTF-8
    def test_strict_raises_on_invalid(self):
        with self.assertRaises(UnicodeError):
            b'\xff\xfe'.decode('utf-8')

    # Test strict mode (explicit) raises on invalid UTF-8
    def test_strict_explicit_raises(self):
        with self.assertRaises(UnicodeError):
            b'\xff\xfe'.decode('utf-8', 'strict')

    # Test with valid UTF-8 - should pass through unchanged
    def test_valid_utf8(self):
        self.assertEqual(b'hello'.decode('utf-8', 'ignore'), 'hello')

    # Test valid UTF-8 with default mode
    def test_valid_utf8_default(self):
        self.assertEqual(b'hello'.decode('utf-8'), 'hello')

    # Test mixed valid and invalid UTF-8
    def test_mixed_valid_invalid(self):
        self.assertEqual(b'hello\xffworld'.decode('utf-8', 'ignore'), 'helloworld')

    # Test multiple invalid continuation bytes (0x80-0xBF without leading byte)
    def test_multiple_invalid_bytes(self):
        self.assertEqual(b'\x80\x81\x82'.decode('utf-8', 'ignore'), '')

    # Test invalid 2-byte sequence start (0xC0) followed by non-continuation byte
    def test_invalid_continuation_byte(self):
        self.assertEqual(b'\xc0\x20'.decode('utf-8', 'ignore'), ' ')

    # Test incomplete 2-byte sequence at end of input
    def test_incomplete_sequence_at_end(self):
        self.assertEqual(b'hello\xc0'.decode('utf-8', 'ignore'), 'hello')

    # Test valid 2-byte UTF-8 sequence (© = U+00A9)
    def test_valid_multibyte_copyright(self):
        self.assertEqual(b'\xc2\xa9'.decode('utf-8', 'ignore'), '\u00a9')

    # Test bytearray input (not just bytes)
    def test_bytearray_support(self):
        self.assertEqual(bytearray(b'\xff\xfe').decode('utf-8', 'ignore'), '')

    # Test valid 3-byte UTF-8 sequence (一 = U+4E00)
    def test_valid_3byte_sequence(self):
        self.assertEqual(b'\xe4\xb8\x80'.decode('utf-8', 'ignore'), '\u4e00')

    # Test valid 4-byte UTF-8 sequence (😀 = U+1F600)
    def test_valid_4byte_sequence(self):
        self.assertEqual(b'\xf0\x9f\x98\x80'.decode('utf-8', 'ignore'), '\U0001f600')

    # Test incomplete 3-byte sequence (missing 2 continuation bytes)
    def test_incomplete_3byte_missing_2(self):
        self.assertEqual(b'\xe4'.decode('utf-8', 'ignore'), '')

    # Test incomplete 3-byte sequence (missing 1 continuation byte)
    def test_incomplete_3byte_missing_1(self):
        self.assertEqual(b'\xe4\xb8'.decode('utf-8', 'ignore'), '')

    # Test incomplete 4-byte sequence (missing 3 continuation bytes)
    def test_incomplete_4byte_missing_3(self):
        self.assertEqual(b'\xf0'.decode('utf-8', 'ignore'), '')

    # Test incomplete 4-byte sequence (missing 2 continuation bytes)
    def test_incomplete_4byte_missing_2(self):
        self.assertEqual(b'\xf0\x9f'.decode('utf-8', 'ignore'), '')

    # Test incomplete 4-byte sequence (missing 1 continuation byte)
    def test_incomplete_4byte_missing_1(self):
        self.assertEqual(b'\xf0\x9f\x98'.decode('utf-8', 'ignore'), '')

    # Test 3-byte sequence with invalid first continuation byte
    def test_3byte_invalid_first_continuation(self):
        self.assertEqual(b'\xe4\x20\x80'.decode('utf-8', 'ignore'), ' ')

    # Test 3-byte sequence with invalid second continuation byte
    def test_3byte_invalid_second_continuation(self):
        self.assertEqual(b'\xe4\xb8\x20'.decode('utf-8', 'ignore'), ' ')

    # Test 4-byte sequence with invalid continuation bytes at various positions
    def test_4byte_invalid_continuations(self):
        self.assertEqual(b'\xf0\x20\x98\x80'.decode('utf-8', 'ignore'), ' ')
        self.assertEqual(b'\xf0\x9f\x20\x80'.decode('utf-8', 'ignore'), ' ')
        self.assertEqual(b'\xf0\x9f\x98\x20'.decode('utf-8', 'ignore'), ' ')

    # Test mixed valid ASCII and incomplete multi-byte sequences
    def test_mixed_valid_and_incomplete(self):
        self.assertEqual(b'hello\xe4world'.decode('utf-8', 'ignore'), 'helloworld')
        self.assertEqual(b'hello\xf0world'.decode('utf-8', 'ignore'), 'helloworld')

    # Test valid multi-byte sequence after an invalid byte (exercises got==need path)
    def test_valid_multibyte_after_invalid(self):
        # © preserved after invalid \xff
        self.assertEqual(b'\xff\xc2\xa9'.decode('utf-8', 'ignore'), '\u00a9')
        # 一 preserved after invalid \xff
        self.assertEqual(b'\xff\xe4\xb8\x80'.decode('utf-8', 'ignore'), '\u4e00')

    # Test multiple incomplete sequences in a row
    def test_multiple_incomplete_sequences(self):
        self.assertEqual(b'\xe4\xf0\xe4'.decode('utf-8', 'ignore'), '')


if __name__ == "__main__":
    unittest.main()
