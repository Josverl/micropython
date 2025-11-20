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

"""Additional coverage tests for async modules.

These tests focus on increasing code coverage for async modules.
"""

import asyncio
import os
import tempfile
import pytest
from unittest.mock import Mock, AsyncMock, patch


pytestmark = pytest.mark.async_required


class TestAsyncTransportMethods:
    """Test AsyncTransport methods with mocking."""

    def test_fs_listdir_async(self, async_modules):
        """Test fs_listdir_async method."""
        AsyncTransport = async_modules["AsyncTransport"]
        transport = AsyncTransport()

        assert hasattr(transport, "fs_listdir_async")
        assert asyncio.iscoroutinefunction(transport.fs_listdir_async)

    def test_fs_stat_async(self, async_modules):
        """Test fs_stat_async method."""
        AsyncTransport = async_modules["AsyncTransport"]
        transport = AsyncTransport()

        assert hasattr(transport, "fs_stat_async")
        assert asyncio.iscoroutinefunction(transport.fs_stat_async)

    def test_fs_readfile_async(self, async_modules):
        """Test fs_readfile_async method."""
        AsyncTransport = async_modules["AsyncTransport"]
        transport = AsyncTransport()

        assert hasattr(transport, "fs_readfile_async")

    def test_fs_writefile_async(self, async_modules):
        """Test fs_writefile_async method."""
        AsyncTransport = async_modules["AsyncTransport"]
        transport = AsyncTransport()

        assert hasattr(transport, "fs_writefile_async")


@pytest.mark.posix_only
class TestConsoleAsyncPosix:
    """Test AsyncConsolePosix class."""

    def test_posix_console_instantiation(self, async_modules):
        """Test POSIX console can be created."""
        from mpremote.console_async import AsyncConsolePosix

        console = AsyncConsolePosix()
        assert console is not None
        assert hasattr(console, "infd")
        assert hasattr(console, "infile")
        assert hasattr(console, "outfile")
        assert hasattr(console, "orig_attr")

    def test_posix_console_methods(self, async_modules):
        """Test POSIX console methods."""
        from mpremote.console_async import AsyncConsolePosix

        console = AsyncConsolePosix()

        assert hasattr(console, "enter")
        assert hasattr(console, "exit")
        assert hasattr(console, "readchar")
        assert hasattr(console, "readchar_async")
        assert hasattr(console, "write")
        assert hasattr(console, "waitchar")

        assert asyncio.iscoroutinefunction(console.readchar_async)


@pytest.mark.windows_only
class TestConsoleAsyncWindows:
    """Test AsyncConsoleWindows class."""

    def test_windows_console_instantiation(self, async_modules):
        """Test Windows console can be created."""
        from mpremote.console_async import AsyncConsoleWindows

        console = AsyncConsoleWindows()
        assert console is not None
        assert console.ctrl_c == 0
        assert hasattr(console, "_msvcrt")
        assert hasattr(console, "_signal")

    def test_windows_console_methods(self, async_modules):
        """Test Windows console methods."""
        from mpremote.console_async import AsyncConsoleWindows

        console = AsyncConsoleWindows()

        assert hasattr(console, "enter")
        assert hasattr(console, "exit")
        assert hasattr(console, "readchar")
        assert hasattr(console, "readchar_async")
        assert hasattr(console, "write")
        assert hasattr(console, "inWaiting")

        assert asyncio.iscoroutinefunction(console.readchar_async)

    def test_windows_in_waiting(self, async_modules):
        """Test inWaiting method."""
        from mpremote.console_async import AsyncConsoleWindows

        console = AsyncConsoleWindows()
        result = console.inWaiting()
        assert isinstance(result, int)


@pytest.mark.serial_required
class TestAsyncSerialTransportMethods:
    """Test AsyncSerialTransport methods."""

    def test_close_sync_wrapper(self, async_modules):
        """Test synchronous close wrapper."""
        AsyncSerialTransport = async_modules["AsyncSerialTransport"]
        transport = AsyncSerialTransport("/dev/null", baudrate=115200, wait=0)

        assert hasattr(transport, "close")
        assert callable(transport.close)

    def test_fs_hook_mount_attribute(self, async_modules):
        """Test fs_hook_mount attribute exists."""
        AsyncSerialTransport = async_modules["AsyncSerialTransport"]
        assert hasattr(AsyncSerialTransport, "fs_hook_mount")
        assert AsyncSerialTransport.fs_hook_mount == "/remote"


class TestProtocolEncoding:
    """Test protocol encoding with various inputs."""

    def test_encode_unicode_characters(self, async_modules):
        """Test encoding unicode characters."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        cmd = "print('ñ')"
        encoded = RawREPLProtocol.encode_command_standard(cmd)
        assert isinstance(encoded, bytes)
        assert b"print" in encoded

    def test_encode_empty_command(self, async_modules):
        """Test encoding empty command."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        cmd = ""
        encoded = RawREPLProtocol.encode_command_standard(cmd)
        assert encoded == b""

    def test_encode_multiline_command(self, async_modules):
        """Test encoding multiline command."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        cmd = "x = 1\ny = 2\nprint(x + y)"
        encoded = RawREPLProtocol.encode_command_standard(cmd)
        assert b"x = 1" in encoded
        assert b"y = 2" in encoded

    def test_raw_paste_length_encoding(self, async_modules):
        """Test raw paste encodes length correctly."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        cmd = "x" * 100
        header, cmd_bytes = RawREPLProtocol.encode_command_raw_paste(cmd)
        # Length should be encoded in bytes 3-6 (little-endian)
        length_bytes = header[3:7]
        length = int.from_bytes(length_bytes, "little")
        assert length == 100

    def test_decode_response_multiple_separators(self, async_modules):
        """Test decoding response with multiple separators."""
        RawREPLProtocol = async_modules["RawREPLProtocol"]
        response = b"out1\x04err1\x04extra\x04"
        stdout, stderr = RawREPLProtocol.decode_response(response)
        assert stdout == b"out1"
        assert stderr == b"err1"
