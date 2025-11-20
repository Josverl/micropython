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

import asyncio
import pytest


pytestmark = pytest.mark.async_required


def test_async_transport_has_required_methods(async_modules):
    """Test that AsyncTransport is abstract and has required methods."""
    AsyncTransport = async_modules["AsyncTransport"]

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


def test_async_transport_methods_are_async(async_modules):
    """Test that async methods are coroutine functions."""
    AsyncTransport = async_modules["AsyncTransport"]

    async_methods = [
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
    ]

    for method_name in async_methods:
        method = getattr(AsyncTransport, method_name)
        assert asyncio.iscoroutinefunction(method), f"{method_name} should be a coroutine"


@pytest.mark.serial_required
def test_async_serial_transport_instantiation(async_modules):
    """Test that AsyncSerialTransport can be instantiated."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]

    transport = AsyncSerialTransport("/dev/null", baudrate=115200, wait=0)

    assert transport.device_name == "/dev/null"
    assert transport.baudrate == 115200
    assert transport.wait == 0
    assert transport.in_raw_repl is False
    assert transport.use_raw_paste is True
    assert transport.mounted is False


def test_async_serial_transport_inherits(async_modules):
    """Test that AsyncSerialTransport inherits from AsyncTransport."""
    AsyncTransport = async_modules["AsyncTransport"]
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]

    assert issubclass(AsyncSerialTransport, AsyncTransport)


def test_protocol_control_codes(async_modules):
    """Test that RawREPLProtocol has the correct control codes."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    assert RawREPLProtocol.CTRL_A == b"\x01"
    assert RawREPLProtocol.CTRL_B == b"\x02"
    assert RawREPLProtocol.CTRL_C == b"\x03"
    assert RawREPLProtocol.CTRL_D == b"\x04"
    assert RawREPLProtocol.CTRL_E == b"\x05"


def test_protocol_sequences(async_modules):
    """Test protocol sequences are correct."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    assert RawREPLProtocol.RAW_REPL_ENTER == b"\r\x03\x03"
    assert RawREPLProtocol.RAW_REPL_EXIT == b"\r\x02"
    assert RawREPLProtocol.RAW_PASTE_START == b"\x05A\x01"


def test_protocol_expected_responses(async_modules):
    """Test expected protocol responses."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    assert RawREPLProtocol.RAW_REPL_PROMPT == b"raw REPL; CTRL-B to exit\r\n>"
    assert RawREPLProtocol.RAW_REPL_OK == b"OK"
    assert RawREPLProtocol.SOFT_REBOOT_MSG == b"soft reboot\r\n"


def test_protocol_is_raw_paste_supported(async_modules):
    """Test raw paste support detection."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    assert RawREPLProtocol.is_raw_paste_supported(b"OK") is True
    assert RawREPLProtocol.is_raw_paste_supported(b"raw REPL") is True
    assert RawREPLProtocol.is_raw_paste_supported(b"error") is False


def test_protocol_encode_command_standard(async_modules):
    """Test standard command encoding."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    cmd = "print('hello')"
    encoded = RawREPLProtocol.encode_command_standard(cmd)

    assert encoded == b"print('hello')"
    assert isinstance(encoded, bytes)


def test_protocol_encode_command_raw_paste(async_modules):
    """Test raw paste command encoding."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    cmd = "print('hello')"
    header, cmd_bytes = RawREPLProtocol.encode_command_raw_paste(cmd)

    assert header.startswith(RawREPLProtocol.RAW_PASTE_START)
    assert cmd_bytes == b"print('hello')"
    assert len(header) == 7


def test_protocol_decode_response_normal(async_modules):
    """Test decoding normal response."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    response = b"hello world\x04\x04"
    stdout, stderr = RawREPLProtocol.decode_response(response)

    assert stdout == b"hello world"
    assert stderr == b""


def test_protocol_decode_response_with_error(async_modules):
    """Test decoding response with error."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    response = b"output\x04error message\x04"
    stdout, stderr = RawREPLProtocol.decode_response(response)

    assert stdout == b"output"
    assert stderr == b"error message"


def test_protocol_decode_response_empty(async_modules):
    """Test decoding empty response."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    stdout, stderr = RawREPLProtocol.decode_response(b"")

    assert stdout == b""
    assert stderr == b""


def test_protocol_decode_response_no_separator(async_modules):
    """Test decoding response without separator."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    stdout, stderr = RawREPLProtocol.decode_response(b"no separator")

    assert stdout == b"no separator"
    assert stderr == b""


def test_protocol_check_error_with_error(async_modules):
    """Test error checking with error present."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    error = RawREPLProtocol.check_error(b"error message")
    assert error == "error message"


def test_protocol_check_error_empty(async_modules):
    """Test error checking with empty stderr."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    error = RawREPLProtocol.check_error(b"")
    assert error is None


def test_protocol_check_error_whitespace_only(async_modules):
    """Test error checking with whitespace only."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    error = RawREPLProtocol.check_error(b"   \n  ")
    assert error is None


def test_protocol_check_error_strips_whitespace(async_modules):
    """Test error checking strips whitespace."""
    RawREPLProtocol = async_modules["RawREPLProtocol"]

    error = RawREPLProtocol.check_error(b"  error  \n")
    assert error == "error"
