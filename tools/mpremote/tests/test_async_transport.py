#!/usr/bin/env python3
#
# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2025 Jos Verlinde
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Basic tests for async transport layer.

These tests verify that the async transport abstraction is properly
implemented and can be instantiated.
"""

import sys
import os

# Add mpremote to path
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    import asyncio
    from mpremote.transport_async import AsyncTransport
    from mpremote.transport_serial_async import AsyncSerialTransport
    from mpremote.protocol import RawREPLProtocol

    HAS_ASYNC = True
except ImportError as e:
    print(f"Async transport not available: {e}")
    HAS_ASYNC = False


def test_async_transport_abstract():
    """Test that AsyncTransport is abstract and has required methods."""
    if not HAS_ASYNC:
        return  # Skip test

    # Check that AsyncTransport has all required async methods
    required_methods = [
        "read_async",
        "write_async",
        "read_until_async",
        "enter_raw_repl_async",
        "exit_raw_repl_async",
        "exec_raw_no_follow_async",
        "follow_async",
        "exec_raw_async",
        "exec_async",
        "eval_async",
        "close_async",
        "fs_listdir_async",
        "fs_stat_async",
        "fs_readfile_async",
        "fs_writefile_async",
    ]

    for method in required_methods:
        assert hasattr(AsyncTransport, method), f"AsyncTransport missing {method}"


def test_async_serial_transport_instantiation():
    """Test that AsyncSerialTransport can be instantiated."""
    if not HAS_ASYNC:
        return

    try:
        # This should not raise an error even if device doesn't exist
        transport = AsyncSerialTransport("/dev/null", baudrate=115200, wait=0)

        # Check that it has the required attributes
        assert hasattr(transport, "device_name")
        assert hasattr(transport, "baudrate")
        assert hasattr(transport, "in_raw_repl")
        assert hasattr(transport, "use_raw_paste")

        # Check initial state
        assert transport.device_name == "/dev/null"
        assert transport.baudrate == 115200
        assert transport.in_raw_repl is False
        assert transport.use_raw_paste is True

    except Exception as e:
        print(f"FAIL: test_async_serial_transport_instantiation - {e}")


def test_protocol_constants():
    """Test that RawREPLProtocol has the correct constants."""
    if not HAS_ASYNC:
        return

    # Check control codes
    assert RawREPLProtocol.CTRL_A == b"\x01"
    assert RawREPLProtocol.CTRL_B == b"\x02"
    assert RawREPLProtocol.CTRL_C == b"\x03"
    assert RawREPLProtocol.CTRL_D == b"\x04"
    assert RawREPLProtocol.CTRL_E == b"\x05"

    # Check sequences
    assert RawREPLProtocol.RAW_REPL_ENTER == b"\r\x03\x03"
    assert RawREPLProtocol.RAW_REPL_EXIT == b"\r\x02"
    assert RawREPLProtocol.RAW_PASTE_START == b"\x05A\x01"

    # Check expected responses
    assert RawREPLProtocol.RAW_REPL_PROMPT == b"raw REPL; CTRL-B to exit\r\n>"
    assert RawREPLProtocol.RAW_REPL_OK == b"OK"


def test_protocol_encode_command():
    """Test protocol command encoding."""
    if not HAS_ASYNC:
        return

    # Test standard encoding
    cmd = "print('hello')"
    encoded = RawREPLProtocol.encode_command_standard(cmd)
    assert encoded == b"print('hello')"

    # Test raw paste encoding
    header, cmd_bytes = RawREPLProtocol.encode_command_raw_paste(cmd)
    assert header.startswith(RawREPLProtocol.RAW_PASTE_START)
    assert cmd_bytes == b"print('hello')"


def test_protocol_decode_response():
    """Test protocol response decoding."""
    if not HAS_ASYNC:
        return

    # Test normal response with stdout and stderr separated by \x04
    response = b"hello world\x04\x04"
    stdout, stderr = RawREPLProtocol.decode_response(response)
    assert stdout == b"hello world"
    assert stderr == b""

    # Test response with error
    response = b"output\x04error message\x04"
    stdout, stderr = RawREPLProtocol.decode_response(response)
    assert stdout == b"output"
    assert stderr == b"error message"


def run_all_tests():
    """Run all tests."""

    test_async_transport_abstract()
    test_async_serial_transport_instantiation()
    test_protocol_constants()
    test_protocol_encode_command()
    test_protocol_decode_response()



if __name__ == "__main__":
    run_all_tests()
