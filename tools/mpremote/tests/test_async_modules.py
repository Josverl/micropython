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

"""Unit tests for async transport modules using unittest framework.

These tests provide proper coverage tracking and follow unittest conventions.
"""

import sys
import os
import unittest
import asyncio

# Add mpremote to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from mpremote.transport_async import AsyncTransport
    from mpremote.transport_serial_async import AsyncSerialTransport
    from mpremote.protocol import RawREPLProtocol
    from mpremote.console_async import AsyncConsole
    from mpremote.commands_async import do_exec_async, do_eval_async
    from mpremote.main import State
    HAS_ASYNC = True
except ImportError as e:
    HAS_ASYNC = False
    IMPORT_ERROR = str(e)


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestProtocol(unittest.TestCase):
    """Test RawREPLProtocol class."""
    
    def test_control_codes(self):
        """Test protocol control codes are correct."""
        self.assertEqual(RawREPLProtocol.CTRL_A, b'\x01')
        self.assertEqual(RawREPLProtocol.CTRL_B, b'\x02')
        self.assertEqual(RawREPLProtocol.CTRL_C, b'\x03')
        self.assertEqual(RawREPLProtocol.CTRL_D, b'\x04')
        self.assertEqual(RawREPLProtocol.CTRL_E, b'\x05')
    
    def test_sequences(self):
        """Test protocol sequences."""
        self.assertEqual(RawREPLProtocol.RAW_REPL_ENTER, b'\r\x03\x03')
        self.assertEqual(RawREPLProtocol.RAW_REPL_EXIT, b'\r\x02')
        self.assertEqual(RawREPLProtocol.RAW_PASTE_START, b'\x05A\x01')
    
    def test_expected_responses(self):
        """Test expected protocol responses."""
        self.assertEqual(RawREPLProtocol.RAW_REPL_PROMPT, b'raw REPL; CTRL-B to exit\r\n>')
        self.assertEqual(RawREPLProtocol.RAW_REPL_OK, b'OK')
        self.assertEqual(RawREPLProtocol.SOFT_REBOOT_MSG, b'soft reboot\r\n')
    
    def test_is_raw_paste_supported(self):
        """Test raw paste support detection."""
        self.assertTrue(RawREPLProtocol.is_raw_paste_supported(b'OK'))
        self.assertTrue(RawREPLProtocol.is_raw_paste_supported(b'raw REPL'))
        self.assertFalse(RawREPLProtocol.is_raw_paste_supported(b'error'))
    
    def test_encode_command_standard(self):
        """Test standard command encoding."""
        cmd = "print('hello')"
        encoded = RawREPLProtocol.encode_command_standard(cmd)
        self.assertEqual(encoded, b"print('hello')")
        self.assertIsInstance(encoded, bytes)
    
    def test_encode_command_raw_paste(self):
        """Test raw paste command encoding."""
        cmd = "print('hello')"
        header, cmd_bytes = RawREPLProtocol.encode_command_raw_paste(cmd)
        self.assertTrue(header.startswith(RawREPLProtocol.RAW_PASTE_START))
        self.assertEqual(cmd_bytes, b"print('hello')")
        self.assertEqual(len(header), 7)  # Ctrl-E A \x01 + 4 bytes length
    
    def test_decode_response_normal(self):
        """Test decoding normal response."""
        response = b"hello world\x04\x04"
        stdout, stderr = RawREPLProtocol.decode_response(response)
        self.assertEqual(stdout, b"hello world")
        self.assertEqual(stderr, b"")
    
    def test_decode_response_with_error(self):
        """Test decoding response with error."""
        response = b"output\x04error message\x04"
        stdout, stderr = RawREPLProtocol.decode_response(response)
        self.assertEqual(stdout, b"output")
        self.assertEqual(stderr, b"error message")
    
    def test_decode_response_empty(self):
        """Test decoding empty response."""
        stdout, stderr = RawREPLProtocol.decode_response(b"")
        self.assertEqual(stdout, b"")
        self.assertEqual(stderr, b"")
    
    def test_decode_response_no_separator(self):
        """Test decoding response without separator."""
        stdout, stderr = RawREPLProtocol.decode_response(b"no separator")
        self.assertEqual(stdout, b"no separator")
        self.assertEqual(stderr, b"")
    
    def test_check_error_with_error(self):
        """Test error checking with error present."""
        error = RawREPLProtocol.check_error(b"error message")
        self.assertEqual(error, "error message")
    
    def test_check_error_empty(self):
        """Test error checking with empty stderr."""
        error = RawREPLProtocol.check_error(b"")
        self.assertIsNone(error)
    
    def test_check_error_whitespace(self):
        """Test error checking with whitespace only."""
        error = RawREPLProtocol.check_error(b"   \n  ")
        self.assertIsNone(error)
    
    def test_check_error_with_whitespace(self):
        """Test error checking strips whitespace."""
        error = RawREPLProtocol.check_error(b"  error  \n")
        self.assertEqual(error, "error")


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestAsyncTransport(unittest.TestCase):
    """Test AsyncTransport base class."""
    
    def test_has_required_methods(self):
        """Test that AsyncTransport has all required async methods."""
        required_methods = [
            'read_async', 'write_async', 'read_until_async',
            'enter_raw_repl_async', 'exit_raw_repl_async',
            'exec_raw_no_follow_async', 'follow_async',
            'exec_raw_async', 'exec_async', 'eval_async',
            'close_async', 'fs_listdir_async', 'fs_stat_async',
            'fs_readfile_async', 'fs_writefile_async',
        ]
        for method in required_methods:
            self.assertTrue(hasattr(AsyncTransport, method),
                          f"AsyncTransport missing {method}")
    
    def test_methods_are_async(self):
        """Test that async methods are coroutines."""
        async_methods = [
            'read_async', 'write_async', 'read_until_async',
            'enter_raw_repl_async', 'exit_raw_repl_async',
            'exec_raw_no_follow_async', 'follow_async',
            'exec_raw_async', 'exec_async', 'eval_async',
            'close_async',
        ]
        for method_name in async_methods:
            method = getattr(AsyncTransport, method_name)
            self.assertTrue(asyncio.iscoroutinefunction(method),
                          f"{method_name} should be a coroutine")


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestAsyncSerialTransport(unittest.TestCase):
    """Test AsyncSerialTransport class."""
    
    def test_instantiation(self):
        """Test that AsyncSerialTransport can be instantiated."""
        try:
            transport = AsyncSerialTransport("/dev/null", baudrate=115200, wait=0)
            self.assertEqual(transport.device_name, "/dev/null")
            self.assertEqual(transport.baudrate, 115200)
            self.assertEqual(transport.wait, 0)
            self.assertFalse(transport.in_raw_repl)
            self.assertTrue(transport.use_raw_paste)
            self.assertFalse(transport.mounted)
        except ImportError:
            self.skipTest("pyserial-asyncio not installed")
    
    def test_inherits_from_async_transport(self):
        """Test that AsyncSerialTransport inherits from AsyncTransport."""
        self.assertTrue(issubclass(AsyncSerialTransport, AsyncTransport))
    
    def test_has_async_methods(self):
        """Test that AsyncSerialTransport implements async methods."""
        async_methods = [
            'connect', 'read_async', 'write_async', 'read_until_async',
            'enter_raw_repl_async', 'exit_raw_repl_async',
            'exec_raw_no_follow_async', 'follow_async',
            'exec_raw_async', 'exec_async', 'eval_async',
            'close_async',
        ]
        for method_name in async_methods:
            self.assertTrue(hasattr(AsyncSerialTransport, method_name),
                          f"AsyncSerialTransport missing {method_name}")


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestAsyncConsole(unittest.TestCase):
    """Test AsyncConsole factory and classes."""
    
    def test_console_factory(self):
        """Test that AsyncConsole factory returns correct type."""
        console = AsyncConsole()
        self.assertIsNotNone(console)
        # Check it has required methods
        self.assertTrue(hasattr(console, 'enter'))
        self.assertTrue(hasattr(console, 'exit'))
        self.assertTrue(hasattr(console, 'readchar_async'))
        self.assertTrue(hasattr(console, 'write'))
    
    def test_readchar_async_is_async(self):
        """Test that readchar_async is a coroutine."""
        console = AsyncConsole()
        self.assertTrue(asyncio.iscoroutinefunction(console.readchar_async))


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestAsyncCommands(unittest.TestCase):
    """Test async command handlers."""
    
    def test_async_commands_exist(self):
        """Test that async command functions exist."""
        self.assertTrue(callable(do_exec_async))
        self.assertTrue(callable(do_eval_async))
    
    def test_async_commands_are_async(self):
        """Test that async commands are coroutines."""
        self.assertTrue(asyncio.iscoroutinefunction(do_exec_async))
        self.assertTrue(asyncio.iscoroutinefunction(do_eval_async))


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestStateAsync(unittest.TestCase):
    """Test State class async methods."""
    
    def test_state_has_async_methods(self):
        """Test that State class has async methods."""
        state = State()
        self.assertTrue(hasattr(state, 'ensure_connected_async'))
        self.assertTrue(hasattr(state, 'ensure_raw_repl_async'))
        self.assertTrue(hasattr(state, 'ensure_friendly_repl_async'))
    
    def test_state_async_methods_are_async(self):
        """Test that State async methods are coroutines."""
        state = State()
        self.assertTrue(asyncio.iscoroutinefunction(state.ensure_connected_async))
        self.assertTrue(asyncio.iscoroutinefunction(state.ensure_raw_repl_async))
        self.assertTrue(asyncio.iscoroutinefunction(state.ensure_friendly_repl_async))
    
    def test_state_has_sync_methods(self):
        """Test that State still has sync methods (backward compat)."""
        state = State()
        self.assertTrue(hasattr(state, 'ensure_connected'))
        self.assertTrue(hasattr(state, 'ensure_raw_repl'))
        self.assertTrue(hasattr(state, 'ensure_friendly_repl'))
    
    def test_state_sync_methods_are_not_async(self):
        """Test that State sync methods are not coroutines."""
        state = State()
        self.assertFalse(asyncio.iscoroutinefunction(state.ensure_connected))
        self.assertFalse(asyncio.iscoroutinefunction(state.ensure_raw_repl))
        self.assertFalse(asyncio.iscoroutinefunction(state.ensure_friendly_repl))


if __name__ == "__main__":
    # Run with unittest
    unittest.main(verbosity=2)
