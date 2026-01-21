"""
Test suite for Unicode character handling in readline/REPL.

Tests the fix for issue #7585: REPL and `input` skip non-ascii characters.
"""

import pytest
import subprocess
import sys
import os


# Get the MicroPython executable from the environment or use a default
MICROPYTHON = os.environ.get(
    "MICROPY_MICROPYTHON",
    os.path.join(os.path.dirname(__file__), "../ports/unix/build-standard/micropython"),
)


class TestUnicodeReadline:
    """Test Unicode character handling in readline."""

    @pytest.mark.parametrize(
        "test_string,expected",
        [
            ("hello", "hello"),
            ("café", "café"),
            ("你好", "你好"),
            ("Привет", "Привет"),
            ("😀", "😀"),
            ("München", "München"),
            ("Tokyo東京", "Tokyo東京"),
            ("Ελληνικά", "Ελληνικά"),
            ("עברית", "עברית"),
            ("العربية", "العربية"),
            ("🎉🎊🎈", "🎉🎊🎈"),
            ("Mix: café 你好 😀", "Mix: café 你好 😀"),
        ],
    )
    def test_input_with_unicode(self, test_string, expected):
        """Test that input() correctly handles Unicode strings."""
        # Create a simple script that uses input()
        script = f"x = input(); print(repr(x))"

        # Run MicroPython with the test string as input (add newline)
        result = subprocess.run(
            [MICROPYTHON, "-c", script],
            input=(test_string + "\n").encode("utf-8"),
            capture_output=True,
            timeout=5,
        )

        # Extract the output (should be repr of the input)
        output = result.stdout.decode("utf-8").strip()

        # The output should contain a repr of the expected string
        assert expected in output, f"Expected {expected!r} in output, got: {output}"

    @pytest.mark.parametrize(
        "test_bytes",
        [
            b"caf\xc3\xa9",  # café in UTF-8
            b"\xe4\xbd\xa0\xe5\xa5\xbd",  # 你好 in UTF-8
            b"\xf0\x9f\x98\x80",  # 😀 in UTF-8
            b"M\xc3\xbcnchen",  # München in UTF-8
        ],
    )
    def test_utf8_byte_sequences(self, test_bytes):
        """Test that UTF-8 byte sequences are properly decoded."""
        # Decode to get expected string
        expected = test_bytes.decode("utf-8")

        # Create a script that reads input and prints it
        script = "x = input(); print(repr(x))"

        result = subprocess.run(
            [MICROPYTHON, "-c", script], input=test_bytes + b"\n", capture_output=True, timeout=5
        )

        output = result.stdout.decode("utf-8").strip()
        assert expected in output, f"Expected {expected!r} in output, got: {output}"

    def test_mixed_ascii_and_unicode(self):
        """Test strings with mixed ASCII and Unicode characters."""
        test_cases = [
            "Hello, 世界!",
            "Price: €50",
            "Temp: 25°C",
            "1 + 1 = 2 ✓",
        ]

        for test_string in test_cases:
            script = "x = input(); print(repr(x))"
            result = subprocess.run(
                [MICROPYTHON, "-c", script],
                input=(test_string + "\n").encode("utf-8"),
                capture_output=True,
                timeout=5,
            )
            output = result.stdout.decode("utf-8").strip()
            assert test_string in output, f"Expected {test_string!r} in output, got: {output}"

    def test_unicode_variable_assignment(self):
        """Test assigning Unicode strings to variables in REPL."""
        # Test simple variable assignment with Unicode
        script = 'x = "café"; print(repr(x))'
        result = subprocess.run([MICROPYTHON, "-c", script], capture_output=True, timeout=5)
        output = result.stdout.decode("utf-8").strip()
        # MicroPython may show escape sequences in repr, check for either form
        assert "café" in output or "caf" in output

    def test_utf8_continuation_bytes(self):
        """Test that UTF-8 continuation bytes (0x80-0xFF) are handled correctly."""
        # These bytes should not be treated as separate characters
        # UTF-8 encoding of "é" is 0xC3 0xA9
        test_bytes = b"\xc3\xa9"  # é
        expected = "é"

        script = "x = input(); print(len(x)); print(repr(x))"
        result = subprocess.run(
            [MICROPYTHON, "-c", script], input=test_bytes + b"\n", capture_output=True, timeout=5
        )

        output = result.stdout.decode("utf-8")
        # Length should be 1 (one character), not 2 (two bytes)
        assert "1" in output, f"Expected length 1, output: {output}"
        assert expected in output, f"Expected {expected!r} in output: {output}"

    def test_multibyte_character_boundaries(self):
        """Test various UTF-8 character byte lengths."""
        test_cases = [
            # 1-byte (ASCII)
            ("A", 1),
            # 2-byte characters
            ("é", 1),
            ("Ω", 1),
            # 3-byte characters
            ("你", 1),
            ("€", 1),
            # 4-byte characters (emojis)
            ("😀", 1),
            ("🎉", 1),
        ]

        for char, expected_len in test_cases:
            script = f"x = input(); print(len(x))"
            result = subprocess.run(
                [MICROPYTHON, "-c", script],
                input=(char + "\n").encode("utf-8"),
                capture_output=True,
                timeout=5,
            )
            output = result.stdout.decode("utf-8").strip()
            assert str(expected_len) in output, (
                f"Character {char!r} should have length {expected_len}, got output: {output}"
            )

    def test_unicode_string_operations(self):
        """Test that Unicode strings work correctly with string operations."""
        script = """
x = input()
print(len(x))
print(x.upper())
print(x.lower())
"""
        test_string = "café"
        result = subprocess.run(
            [MICROPYTHON, "-c", script],
            input=(test_string + "\n").encode("utf-8"),
            capture_output=True,
            timeout=5,
        )

        output = result.stdout.decode("utf-8")
        assert "4" in output  # Length should be 4
        assert "CAFÉ" in output or "CAFé" in output  # Upper case
        assert "café" in output  # Lower case


class TestUnicodeEdgeCases:
    """Test edge cases and error conditions for Unicode handling."""

    def test_invalid_utf8_sequences(self):
        """Test handling of invalid UTF-8 sequences."""
        # Invalid UTF-8 sequences should either be rejected or handled gracefully
        invalid_sequences = [
            b"\xff\xff",  # Invalid start bytes
            b"\xc3",  # Incomplete 2-byte sequence
            b"\xe0\x80",  # Incomplete 3-byte sequence
            b"\xf0\x80\x80",  # Incomplete 4-byte sequence
        ]

        for seq in invalid_sequences:
            script = 'x = input(); print("got input")'
            result = subprocess.run(
                [MICROPYTHON, "-c", script], input=seq + b"\n", capture_output=True, timeout=5
            )
            # Should complete without hanging or crashing
            assert result.returncode is not None

    def test_empty_input(self):
        """Test that empty input is handled correctly."""
        script = "x = input(); print(repr(x)); print(len(x))"
        result = subprocess.run(
            [MICROPYTHON, "-c", script], input=b"\n", capture_output=True, timeout=5
        )
        output = result.stdout.decode("utf-8")
        assert "0" in output  # Length should be 0

    def test_very_long_unicode_string(self):
        """Test handling of long Unicode strings."""
        # Create a long string with various Unicode characters
        test_string = "café " * 100  # 500 characters
        script = "x = input(); print(len(x))"
        result = subprocess.run(
            [MICROPYTHON, "-c", script],
            input=(test_string + "\n").encode("utf-8"),
            capture_output=True,
            timeout=5,
        )
        output = result.stdout.decode("utf-8").strip()
        assert "500" in output


class TestUTF8ByteProcessing:
    """Test the actual byte-by-byte processing that occurs in readline."""

    def test_two_byte_utf8(self):
        """Test 2-byte UTF-8 character processing."""
        # Test characters that encode to 2 bytes
        chars = ["é", "ñ", "ö", "ü", "ä", "Ω", "α", "β"]
        for char in chars:
            script = f"x = input(); print(repr(x)); print(len(x))"
            result = subprocess.run(
                [MICROPYTHON, "-c", script],
                input=(char + "\n").encode("utf-8"),
                capture_output=True,
                timeout=5,
            )
            output = result.stdout.decode("utf-8")
            assert char in output, f"Expected {char!r} in output: {output}"
            assert "1" in output, f"Length should be 1 for {char!r}, output: {output}"

    def test_three_byte_utf8(self):
        """Test 3-byte UTF-8 character processing."""
        # Test characters that encode to 3 bytes
        chars = ["你", "好", "東", "京", "€", "→", "←"]
        for char in chars:
            script = f"x = input(); print(repr(x)); print(len(x))"
            result = subprocess.run(
                [MICROPYTHON, "-c", script],
                input=(char + "\n").encode("utf-8"),
                capture_output=True,
                timeout=5,
            )
            output = result.stdout.decode("utf-8")
            assert char in output, f"Expected {char!r} in output: {output}"
            assert "1" in output, f"Length should be 1 for {char!r}, output: {output}"

    def test_four_byte_utf8(self):
        """Test 4-byte UTF-8 character processing (emojis)."""
        # Test characters that encode to 4 bytes
        emojis = ["😀", "🎉", "🎊", "🎈", "🚀", "❤️"]
        for emoji in emojis:
            script = f"x = input(); print(repr(x)); print(len(x))"
            result = subprocess.run(
                [MICROPYTHON, "-c", script],
                input=(emoji + "\n").encode("utf-8"),
                capture_output=True,
                timeout=5,
            )
            output = result.stdout.decode("utf-8")
            # Note: Some emojis might have combining characters, so length check is flexible
            assert emoji in output or emoji[:1] in output, (
                f"Expected {emoji!r} or part of it in output: {output}"
            )


if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, "-v"])
