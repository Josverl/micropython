import codecs
import io
import os
import sys

import pytest


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mpremote.console import ConsoleWindows
import mpremote.transport as transport


@pytest.fixture
def reset_stdout_buffer():
    transport._stdout_buffer = b""
    yield
    transport._stdout_buffer = b""


def test_legacy_console_buffers_split_utf8(monkeypatch):
    console = ConsoleWindows.__new__(ConsoleWindows)
    console._use_raw_output = False
    console._decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
    output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", output)

    console.write(b"\xe4")
    console.write(b"\xb8")
    assert output.getvalue() == ""
    console.write(b"\xad")

    assert output.getvalue() == "中"


def test_modern_console_writes_utf8_bytes():
    console = ConsoleWindows.__new__(ConsoleWindows)
    console._use_raw_output = True
    console.outfile = io.BytesIO()

    console.write("你好")

    assert console.outfile.getvalue() == "你好".encode("utf-8")


def test_split_utf8_is_buffered_until_complete(monkeypatch, reset_stdout_buffer):
    class Output:
        def __init__(self):
            self.buffer = io.BytesIO()

        def flush(self):
            pass

    output = Output()
    monkeypatch.setattr(sys, "stdout", output)

    transport.stdout_write_bytes(b"A\xe4")
    assert output.buffer.getvalue() == b"A"
    assert transport._stdout_buffer == b"\xe4"
    transport.stdout_write_bytes(b"\xb8\xad")

    assert output.buffer.getvalue() == b"A\xe4\xb8\xad"
    assert transport._stdout_buffer == b""
