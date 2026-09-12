import codecs
import io
import os
import sys
import unittest
from unittest import mock


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mpremote.console import ConsoleWindows
import mpremote.transport as transport


class ConsoleWindowsOutputTest(unittest.TestCase):
    def test_legacy_console_buffers_split_utf8(self):
        console = ConsoleWindows.__new__(ConsoleWindows)
        console._use_raw_output = False
        console._decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        output = io.StringIO()

        with mock.patch.object(sys, "stdout", output):
            console.write(b"\xe4")
            console.write(b"\xb8")
            self.assertEqual(output.getvalue(), "")
            console.write(b"\xad")

        self.assertEqual(output.getvalue(), "中")

    def test_modern_console_writes_utf8_bytes(self):
        console = ConsoleWindows.__new__(ConsoleWindows)
        console._use_raw_output = True
        console.outfile = io.BytesIO()

        console.write("你好")

        self.assertEqual(console.outfile.getvalue(), "你好".encode("utf-8"))


class StdoutWriteBytesTest(unittest.TestCase):
    def setUp(self):
        transport._stdout_buffer = b""

    def tearDown(self):
        transport._stdout_buffer = b""

    def test_split_utf8_is_buffered_until_complete(self):
        class Output:
            def __init__(self):
                self.buffer = io.BytesIO()

            def flush(self):
                pass

        output = Output()
        with mock.patch.object(sys, "stdout", output):
            transport.stdout_write_bytes(b"A\xe4")
            self.assertEqual(output.buffer.getvalue(), b"A")
            self.assertEqual(transport._stdout_buffer, b"\xe4")
            transport.stdout_write_bytes(b"\xb8\xad")

        self.assertEqual(output.buffer.getvalue(), b"A\xe4\xb8\xad")
        self.assertEqual(transport._stdout_buffer, b"")


if __name__ == "__main__":
    unittest.main()