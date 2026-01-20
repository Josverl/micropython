# Test bytes.decode() with error handlers

# Check if decode method is available (requires MICROPY_CPYTHON_COMPAT)
try:
    b''.decode()
except AttributeError:
    print("SKIP")
    raise SystemExit

# Check if error handlers are available (requires MICROPY_PY_BUILTINS_BYTES_DECODE_IGNORE)
# When feature is disabled, invalid UTF-8 raises UnicodeError even with 'ignore'
# When feature is enabled, invalid UTF-8 with 'ignore' returns a string
try:
    result = b'\xff'.decode('utf-8', 'ignore')
    # If we get here, feature is available
    has_error_handlers = True
except UnicodeError:
    # Feature not available - 'ignore' was ignored, strict mode was used
    print("SKIP")
    raise SystemExit

try:
    import unittest
except ImportError:
    print("SKIP")
    raise SystemExit


class TestBytesDecodeErrors(unittest.TestCase):
    def test_ignore_invalid_utf8(self):
        # Test ignore mode with invalid UTF-8
        self.assertEqual(b'\xff\xfe'.decode('utf-8', 'ignore'), '')

    def test_strict_mode_default(self):
        # Test strict mode (default) with invalid UTF-8
        with self.assertRaises(UnicodeError):
            b'\xff\xfe'.decode('utf-8')

    def test_strict_mode_explicit(self):
        # Test strict mode (explicit) with invalid UTF-8
        with self.assertRaises(UnicodeError):
            b'\xff\xfe'.decode('utf-8', 'strict')

    def test_ignore_valid_utf8(self):
        # Test with valid UTF-8
        self.assertEqual(b'hello'.decode('utf-8', 'ignore'), 'hello')

    def test_valid_utf8_default(self):
        # Test valid UTF-8 with default mode
        self.assertEqual(b'hello'.decode('utf-8'), 'hello')

    def test_ignore_mixed_content(self):
        # Test mixed valid and invalid UTF-8
        self.assertEqual(b'hello\xffworld'.decode('utf-8', 'ignore'), 'helloworld')

    def test_ignore_multiple_invalid(self):
        # Test multiple invalid bytes
        self.assertEqual(b'\x80\x81\x82'.decode('utf-8', 'ignore'), '')

    def test_ignore_invalid_continuation(self):
        # Test invalid continuation byte
        self.assertEqual(b'\xc0\x20'.decode('utf-8', 'ignore'), ' ')

    def test_ignore_incomplete_sequence(self):
        # Test incomplete sequence at end
        self.assertEqual(b'hello\xc0'.decode('utf-8', 'ignore'), 'hello')

    def test_ignore_valid_multibyte(self):
        # Test valid multi-byte UTF-8 (© symbol)
        self.assertEqual(b'\xc2\xa9'.decode('utf-8', 'ignore'), '\xa9')

    def test_bytearray_ignore(self):
        # Test bytearray support
        self.assertEqual(bytearray(b'\xff\xfe').decode('utf-8', 'ignore'), '')

    def test_replace_invalid_utf8(self):
        # Test replace mode - should either work or raise NotImplementedError
        try:
            result = b'\xff\xfe'.decode('utf-8', 'replace')
            # If replace is implemented, check the result
            self.assertEqual(result, '\ufffd\ufffd')
        except NotImplementedError:
            # If replace is not implemented, that's expected
            pass

    def test_replace_valid_utf8(self):
        # Test replace with valid UTF-8 - should work even if replace isn't fully enabled
        try:
            result = b'hello'.decode('utf-8', 'replace')
            self.assertEqual(result, 'hello')
        except NotImplementedError:
            # If replace is not implemented, that's expected
            pass

    def test_replace_mixed_content(self):
        # Test replace with mixed content
        try:
            result = b'hello\xffworld'.decode('utf-8', 'replace')
            self.assertEqual(result, 'hello\ufffdworld')
        except NotImplementedError:
            # If replace is not implemented, that's expected
            pass


if __name__ == "__main__":
    unittest.main()
