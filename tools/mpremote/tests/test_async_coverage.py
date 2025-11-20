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

import sys
import os
import unittest
import asyncio
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from io import BytesIO

# Add mpremote to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from mpremote.transport_async import AsyncTransport
    from mpremote.transport_serial_async import AsyncSerialTransport
    from mpremote.protocol import RawREPLProtocol
    from mpremote.console_async import AsyncConsole, AsyncConsolePosix, AsyncConsoleWindows
    from mpremote.commands_async import (
        do_exec_async,
        do_eval_async,
        do_run_async,
        do_filesystem_cp_async,
    )
    from mpremote.transport import TransportError, TransportExecError

    HAS_ASYNC = True
except ImportError as e:
    HAS_ASYNC = False
    IMPORT_ERROR = str(e)


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestAsyncTransportMethods(unittest.TestCase):
    """Test AsyncTransport methods with mocking."""

    def test_fs_listdir_async(self):
        """Test fs_listdir_async method."""
        transport = AsyncTransport()

        # Test that the method exists and is async
        self.assertTrue(hasattr(transport, "fs_listdir_async"))
        self.assertTrue(asyncio.iscoroutinefunction(transport.fs_listdir_async))

    def test_fs_stat_async(self):
        """Test fs_stat_async method."""
        transport = AsyncTransport()

        # Test that the method exists and is async
        self.assertTrue(hasattr(transport, "fs_stat_async"))
        self.assertTrue(asyncio.iscoroutinefunction(transport.fs_stat_async))

    def test_fs_readfile_async(self):
        """Test fs_readfile_async method."""
        transport = AsyncTransport()

        # Test that the method exists and is async
        self.assertTrue(hasattr(transport, "fs_readfile_async"))
        # Note: This uses sync implementation as placeholder, so might not be async

    def test_fs_writefile_async(self):
        """Test fs_writefile_async method."""
        transport = AsyncTransport()

        # Test that the method exists
        self.assertTrue(hasattr(transport, "fs_writefile_async"))


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestConsoleAsyncPosix(unittest.TestCase):
    """Test AsyncConsolePosix class."""

    @unittest.skipIf(sys.platform == "win32", "POSIX only test")
    def test_posix_console_instantiation(self):
        """Test POSIX console can be created."""
        try:
            import termios

            console = AsyncConsolePosix()
            self.assertIsNotNone(console)
            self.assertTrue(hasattr(console, "infd"))
            self.assertTrue(hasattr(console, "infile"))
            self.assertTrue(hasattr(console, "outfile"))
            self.assertTrue(hasattr(console, "orig_attr"))
        except ImportError:
            self.skipTest("termios not available")

    @unittest.skipIf(sys.platform == "win32", "POSIX only test")
    def test_posix_console_methods(self):
        """Test POSIX console methods."""
        try:
            import termios

            console = AsyncConsolePosix()

            # Test methods exist
            self.assertTrue(hasattr(console, "enter"))
            self.assertTrue(hasattr(console, "exit"))
            self.assertTrue(hasattr(console, "readchar"))
            self.assertTrue(hasattr(console, "readchar_async"))
            self.assertTrue(hasattr(console, "write"))
            self.assertTrue(hasattr(console, "waitchar"))

            # Test readchar_async is async
            self.assertTrue(asyncio.iscoroutinefunction(console.readchar_async))
        except ImportError:
            self.skipTest("termios not available")


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestConsoleAsyncWindows(unittest.TestCase):
    """Test AsyncConsoleWindows class."""

    @unittest.skipUnless(sys.platform == "win32", "Windows only test")
    def test_windows_console_instantiation(self):
        """Test Windows console can be created."""
        console = AsyncConsoleWindows()
        self.assertIsNotNone(console)
        self.assertEqual(console.ctrl_c, 0)
        self.assertTrue(hasattr(console, "_msvcrt"))
        self.assertTrue(hasattr(console, "_signal"))

    @unittest.skipUnless(sys.platform == "win32", "Windows only test")
    def test_windows_console_methods(self):
        """Test Windows console methods."""
        console = AsyncConsoleWindows()

        # Test methods exist
        self.assertTrue(hasattr(console, "enter"))
        self.assertTrue(hasattr(console, "exit"))
        self.assertTrue(hasattr(console, "readchar"))
        self.assertTrue(hasattr(console, "readchar_async"))
        self.assertTrue(hasattr(console, "write"))
        self.assertTrue(hasattr(console, "inWaiting"))

        # Test readchar_async is async
        self.assertTrue(asyncio.iscoroutinefunction(console.readchar_async))

    @unittest.skipUnless(sys.platform == "win32", "Windows only test")
    def test_windows_in_waiting(self):
        """Test inWaiting method."""
        console = AsyncConsoleWindows()
        result = console.inWaiting()
        self.assertIsInstance(result, int)


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestAsyncSerialTransportMethods(unittest.TestCase):
    """Test AsyncSerialTransport methods."""

    def test_close_sync_wrapper(self):
        """Test synchronous close wrapper."""
        try:
            transport = AsyncSerialTransport("/dev/null", baudrate=115200, wait=0)
            # Test that close exists
            self.assertTrue(hasattr(transport, "close"))
            self.assertTrue(callable(transport.close))
        except ImportError:
            self.skipTest("pyserial-asyncio not installed")

    def test_fs_hook_mount_attribute(self):
        """Test fs_hook_mount attribute exists."""
        self.assertTrue(hasattr(AsyncSerialTransport, "fs_hook_mount"))
        self.assertEqual(AsyncSerialTransport.fs_hook_mount, "/remote")


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestProtocolEncoding(unittest.TestCase):
    """Test protocol encoding with various inputs."""

    def test_encode_unicode_characters(self):
        """Test encoding unicode characters."""
        cmd = "print('ñ')"
        encoded = RawREPLProtocol.encode_command_standard(cmd)
        self.assertIsInstance(encoded, bytes)
        self.assertIn(b"print", encoded)

    def test_encode_empty_command(self):
        """Test encoding empty command."""
        cmd = ""
        encoded = RawREPLProtocol.encode_command_standard(cmd)
        self.assertEqual(encoded, b"")

    def test_encode_multiline_command(self):
        """Test encoding multiline command."""
        cmd = "x = 1\ny = 2\nprint(x + y)"
        encoded = RawREPLProtocol.encode_command_standard(cmd)
        self.assertIn(b"x = 1", encoded)
        self.assertIn(b"y = 2", encoded)

    def test_raw_paste_length_encoding(self):
        """Test raw paste encodes length correctly."""
        cmd = "x" * 100
        header, cmd_bytes = RawREPLProtocol.encode_command_raw_paste(cmd)
        # Length should be encoded in bytes 3-6 (little-endian)
        length_bytes = header[3:7]
        length = int.from_bytes(length_bytes, "little")
        self.assertEqual(length, 100)

    def test_decode_response_multiple_separators(self):
        """Test decoding response with multiple separators."""
        response = b"out1\x04err1\x04extra\x04"
        stdout, stderr = RawREPLProtocol.decode_response(response)
        self.assertEqual(stdout, b"out1")
        self.assertEqual(stderr, b"err1")


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestCommandsAsyncWithMocks(unittest.TestCase):
    """Test async commands with mocking."""

    async def test_do_exec_async_with_mock_state(self):
        """Test do_exec_async with mocked state."""
        # Create mock state and transport
        state = Mock()
        state.transport = Mock()
        state.transport.exec_raw_no_follow_async = AsyncMock()
        state.transport.follow_async = AsyncMock(return_value=(b"output", b""))
        state.ensure_raw_repl_async = AsyncMock()
        state.did_action = Mock()

        # Create mock args
        args = Mock()
        args.command = "-"
        args.follow = False

        # Mock stdin
        with patch("sys.stdin.buffer.read", return_value=b"print('test')"):
            await do_exec_async(state, args)

        # Verify calls
        state.ensure_raw_repl_async.assert_called_once()
        state.did_action.assert_called_once()

    async def test_do_eval_async_with_mock_state(self):
        """Test do_eval_async with mocked state."""
        state = Mock()
        state.transport = Mock()
        state.transport.eval_async = AsyncMock(return_value=42)
        state.ensure_raw_repl_async = AsyncMock()
        state.did_action = Mock()

        args = Mock()
        args.expression = "2 + 2"

        with patch("builtins.print") as mock_print:
            await do_eval_async(state, args)

        state.ensure_raw_repl_async.assert_called_once()
        state.did_action.assert_called_once()
        state.transport.eval_async.assert_called_once_with("2 + 2")

    async def test_do_run_async_with_mock_state(self):
        """Test do_run_async with mocked state."""
        state = Mock()
        state.transport = Mock()
        state.transport.exec_raw_async = AsyncMock(return_value=(b"output", b""))
        state.ensure_raw_repl_async = AsyncMock()
        state.did_action = Mock()

        args = Mock()
        args.script = "/tmp/test.py"

        # Create temp file
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("print('test')")
            temp_path = f.name

        try:
            args.script = temp_path
            await do_run_async(state, args)

            state.ensure_raw_repl_async.assert_called_once()
            state.did_action.assert_called_once()
        finally:
            os.unlink(temp_path)

    def test_async_command_tests(self):
        """Run async command tests."""
        # Run the async tests
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.test_do_exec_async_with_mock_state())
        loop.run_until_complete(self.test_do_eval_async_with_mock_state())
        loop.run_until_complete(self.test_do_run_async_with_mock_state())


if __name__ == "__main__":
    unittest.main(verbosity=2)
