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

"""Unit tests for async transport modules using pytest framework.

These tests provide proper coverage tracking and follow pytest conventions.
"""

import asyncio
import pytest


pytestmark = pytest.mark.async_required


class TestProtocol:
    """Test RawREPLProtocol class."""

    def test_control_codes(self, async_modules):
        """Test protocol control codes are correct."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        assert RawREPLProtocol.CTRL_A == b"\x01"
        assert RawREPLProtocol.CTRL_B == b"\x02"
        assert RawREPLProtocol.CTRL_C == b"\x03"
        assert RawREPLProtocol.CTRL_D == b"\x04"
        assert RawREPLProtocol.CTRL_E == b"\x05"

    def test_sequences(self, async_modules):
        """Test protocol sequences."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        assert RawREPLProtocol.RAW_REPL_ENTER == b"\r\x03\x03"
        assert RawREPLProtocol.RAW_REPL_EXIT == b"\r\x02"
        assert RawREPLProtocol.RAW_PASTE_START == b"\x05A\x01"

    def test_expected_responses(self, async_modules):
        """Test expected protocol responses."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        assert RawREPLProtocol.RAW_REPL_PROMPT == b"raw REPL; CTRL-B to exit\r\n>"
        assert RawREPLProtocol.RAW_REPL_OK == b"OK"
        assert RawREPLProtocol.SOFT_REBOOT_MSG == b"soft reboot\r\n"

    def test_is_raw_paste_supported(self, async_modules):
        """Test raw paste support detection."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        assert RawREPLProtocol.is_raw_paste_supported(b"OK") is True
        assert RawREPLProtocol.is_raw_paste_supported(b"raw REPL") is True
        assert RawREPLProtocol.is_raw_paste_supported(b"error") is False

    def test_encode_command_standard(self, async_modules):
        """Test standard command encoding."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        cmd = "print('hello')"
        encoded = RawREPLProtocol.encode_command_standard(cmd)
        assert encoded == b"print('hello')"
        assert isinstance(encoded, bytes)

    def test_encode_command_raw_paste(self, async_modules):
        """Test raw paste command encoding."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        cmd = "print('hello')"
        header, cmd_bytes = RawREPLProtocol.encode_command_raw_paste(cmd)
        assert header.startswith(RawREPLProtocol.RAW_PASTE_START)
        assert cmd_bytes == b"print('hello')"
        assert len(header) == 7

    def test_decode_response_normal(self, async_modules):
        """Test decoding normal response."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        response = b"hello world\x04\x04"
        stdout, stderr = RawREPLProtocol.decode_response(response)
        assert stdout == b"hello world"
        assert stderr == b""

    def test_decode_response_with_error(self, async_modules):
        """Test decoding response with error."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        response = b"output\x04error message\x04"
        stdout, stderr = RawREPLProtocol.decode_response(response)
        assert stdout == b"output"
        assert stderr == b"error message"

    def test_decode_response_empty(self, async_modules):
        """Test decoding empty response."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        stdout, stderr = RawREPLProtocol.decode_response(b"")
        assert stdout == b""
        assert stderr == b""

    def test_decode_response_no_separator(self, async_modules):
        """Test decoding response without separator."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        stdout, stderr = RawREPLProtocol.decode_response(b"no separator")
        assert stdout == b"no separator"
        assert stderr == b""

    def test_check_error_with_error(self, async_modules):
        """Test error checking with error present."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        error = RawREPLProtocol.check_error(b"error message")
        assert error == "error message"

    def test_check_error_empty(self, async_modules):
        """Test error checking with empty stderr."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        error = RawREPLProtocol.check_error(b"")
        assert error is None

    def test_check_error_whitespace(self, async_modules):
        """Test error checking with whitespace only."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        error = RawREPLProtocol.check_error(b"   \n  ")
        assert error is None

    def test_check_error_with_whitespace(self, async_modules):
        """Test error checking strips whitespace."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        error = RawREPLProtocol.check_error(b"  error  \n")
        assert error == "error"


class TestAsyncTransport:
    """Test AsyncTransport base class."""

    def test_has_required_methods(self, async_modules):
        """Test that AsyncTransport has all required async methods."""
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

    def test_methods_are_async(self, async_modules):
        """Test that async methods are coroutines."""
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


class TestAsyncSerialTransport:
    """Test AsyncSerialTransport class."""

    @pytest.mark.serial_required
    def test_instantiation(self, async_modules):
        """Test that AsyncSerialTransport can be instantiated."""
        AsyncSerialTransport = async_modules["AsyncSerialTransport"]
        transport = AsyncSerialTransport("/dev/null", baudrate=115200, wait=0)
        assert transport.device_name == "/dev/null"
        assert transport.baudrate == 115200
        assert transport.wait == 0
        assert transport.in_raw_repl is False
        assert transport.use_raw_paste is True
        assert transport.mounted is False

    def test_inherits_from_async_transport(self, async_modules):
        """Test that AsyncSerialTransport inherits from AsyncTransport."""
        AsyncTransport = async_modules["AsyncTransport"]
        AsyncSerialTransport = async_modules["AsyncSerialTransport"]
        assert issubclass(AsyncSerialTransport, AsyncTransport)

    def test_has_async_methods(self, async_modules):
        """Test that AsyncSerialTransport implements async methods."""
        AsyncSerialTransport = async_modules["AsyncSerialTransport"]
        async_methods = [
            "connect",
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
            assert hasattr(AsyncSerialTransport, method_name), (
                f"AsyncSerialTransport missing {method_name}"
            )


class TestAsyncConsole:
    """Test AsyncConsole factory and classes."""

    def test_console_factory(self, async_modules):
        """Test that AsyncConsole factory returns correct type."""
        AsyncConsole = async_modules["AsyncConsole"]
        console = AsyncConsole()
        assert console is not None
        assert hasattr(console, "enter")
        assert hasattr(console, "exit")
        assert hasattr(console, "readchar_async")
        assert hasattr(console, "write")

    def test_readchar_async_is_async(self, async_modules):
        """Test that readchar_async is a coroutine."""
        AsyncConsole = async_modules["AsyncConsole"]
        console = AsyncConsole()
        assert asyncio.iscoroutinefunction(console.readchar_async)


class TestAsyncCommands:
    """Test async command handlers."""

    def test_async_commands_exist(self, async_modules):
        """Test that async command functions exist."""
        do_exec_async = async_modules["do_exec_async"]
        do_eval_async = async_modules["do_eval_async"]
        assert callable(do_exec_async)
        assert callable(do_eval_async)

    def test_async_commands_are_async(self, async_modules):
        """Test that async commands are coroutines."""
        do_exec_async = async_modules["do_exec_async"]
        do_eval_async = async_modules["do_eval_async"]
        assert asyncio.iscoroutinefunction(do_exec_async)
        assert asyncio.iscoroutinefunction(do_eval_async)


class TestStateAsync:
    """Test State class async methods."""

    def test_state_has_async_methods(self, async_modules):
        """Test that State class has async methods."""
        from mpremote.main import State

        state = State()
        assert hasattr(state, "ensure_connected_async")
        assert hasattr(state, "ensure_raw_repl_async")
        assert hasattr(state, "ensure_friendly_repl_async")

    def test_state_async_methods_are_async(self, async_modules):
        """Test that State async methods are coroutines."""
        from mpremote.main import State

        state = State()
        assert asyncio.iscoroutinefunction(state.ensure_connected_async)
        assert asyncio.iscoroutinefunction(state.ensure_raw_repl_async)
        assert asyncio.iscoroutinefunction(state.ensure_friendly_repl_async)

    def test_state_has_sync_methods(self, async_modules):
        """Test that State still has sync methods (backward compat)."""
        from mpremote.main import State

        state = State()
        assert hasattr(state, "ensure_connected")
        assert hasattr(state, "ensure_raw_repl")
        assert hasattr(state, "ensure_friendly_repl")

    def test_state_sync_methods_are_not_async(self, async_modules):
        """Test that State sync methods are not coroutines."""
        from mpremote.main import State

        state = State()
        assert not asyncio.iscoroutinefunction(state.ensure_connected)
        assert not asyncio.iscoroutinefunction(state.ensure_raw_repl)
        assert not asyncio.iscoroutinefunction(state.ensure_friendly_repl)
