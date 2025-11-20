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

"""Hardware integration tests for async transport.

This test suite validates the async transport implementation against real
MicroPython devices connected via serial or USB-CDC.

Usage:
    # Test with first available device
    python test_async_hardware.py

    # Test with specific port
    python test_async_hardware.py COM20
    python test_async_hardware.py /dev/ttyUSB0

    # Run specific test
    python test_async_hardware.py COM20 TestAsyncHardware.test_basic_connection

Requirements:
    - A MicroPython device connected via serial/USB-CDC
    - pyserial-asyncio installed
"""

import sys
import os
import unittest
import asyncio
import tempfile
from pathlib import Path

# Add mpremote to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from mpremote.transport_serial_async import AsyncSerialTransport
    from mpremote.transport import TransportError
    import serial.tools.list_ports

    HAS_ASYNC = True
except ImportError as e:
    HAS_ASYNC = False
    IMPORT_ERROR = str(e)

# Global test port - can be set via command line
TEST_PORT = None


def find_micropython_device():
    """Find the first available MicroPython device."""
    try:
        ports = serial.tools.list_ports.comports()
        if not ports:
            return None

        # Look for common MicroPython device identifiers
        micropython_keywords = [
            "USB Serial",
            "USB-SERIAL",
            "CH340",
            "CH343",
            "CP210",
            "FT232",
            "Arduino",
            "Pico",
            "ESP32",
            "STM32",
        ]

        for port in ports:
            description = port.description.upper()
            for keyword in micropython_keywords:
                if keyword.upper() in description:
                    return port.device

        # If no specific match, return first available
        return ports[0].device
    except Exception:
        return None


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestAsyncHardware(unittest.TestCase):
    """Hardware integration tests for async transport."""

    @classmethod
    def setUpClass(cls):
        """Set up test class - verify device is available."""
        global TEST_PORT

        if TEST_PORT is None:
            TEST_PORT = find_micropython_device()

        if TEST_PORT is None:
            raise unittest.SkipTest("No MicroPython device found")

        print(f"\nUsing device: {TEST_PORT}")

    def setUp(self):
        """Set up each test."""
        self.transport = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Clean up after each test."""
        if self.transport:
            try:
                self.loop.run_until_complete(self.transport.close_async())
            except:
                pass
        self.loop.close()

    async def _connect_transport(self, timeout=5.0):
        """Helper to connect transport with timeout."""
        self.transport = AsyncSerialTransport(TEST_PORT, baudrate=115200)
        await asyncio.wait_for(self.transport.connect(), timeout=timeout)
        return self.transport

    def test_basic_connection(self):
        """Test basic connection and disconnection."""

        async def _test():
            transport = await self._connect_transport()
            self.assertIsNotNone(transport.reader)
            self.assertIsNotNone(transport.writer)
            self.assertEqual(transport.device_name, TEST_PORT)

        self.loop.run_until_complete(_test())

    def test_enter_raw_repl(self):
        """Test entering raw REPL mode."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)
            self.assertTrue(transport.in_raw_repl)

        self.loop.run_until_complete(_test())

    def test_exec_raw_async(self):
        """Test executing raw commands."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            # Simple print command
            stdout, stderr = await transport.exec_raw_async("print('hello')")
            self.assertEqual(stdout.strip(), b"hello")
            self.assertEqual(stderr, b"")

            # Command with result
            stdout, stderr = await transport.exec_raw_async("print(2 + 2)")
            self.assertEqual(stdout.strip(), b"4")
            self.assertEqual(stderr, b"")

        self.loop.run_until_complete(_test())

    def test_exec_with_error(self):
        """Test executing command that raises an error."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            # Command that raises NameError
            stdout, stderr = await transport.exec_raw_async("print(undefined_var)")
            self.assertEqual(stdout, b"")
            self.assertIn(b"NameError", stderr)

        self.loop.run_until_complete(_test())

    def test_eval_async(self):
        """Test evaluating expressions."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            # Arithmetic
            result = await transport.eval_async("2 + 2")
            self.assertEqual(result, 4)

            # String
            result = await transport.eval_async("'hello world'")
            self.assertEqual(result, "hello world")

            # List
            result = await transport.eval_async("[1, 2, 3]")
            self.assertEqual(result, [1, 2, 3])

            # Dictionary
            result = await transport.eval_async("{'a': 1, 'b': 2}")
            self.assertEqual(result, {"a": 1, "b": 2})

        self.loop.run_until_complete(_test())

    def test_exec_async(self):
        """Test executing multi-line code."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            code = """
x = 10
y = 20
print(x + y)
"""
            stdout = await transport.exec_async(code)
            self.assertEqual(stdout.strip(), b"30")

        self.loop.run_until_complete(_test())

    def test_multiple_commands(self):
        """Test executing multiple commands in sequence."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            # Set a variable
            stdout, stderr = await transport.exec_raw_async("x = 42")
            self.assertEqual(stderr, b"")

            # Read it back
            result = await transport.eval_async("x")
            self.assertEqual(result, 42)

            # Modify it
            stdout, stderr = await transport.exec_raw_async("x = x * 2")
            self.assertEqual(stderr, b"")

            # Read modified value
            result = await transport.eval_async("x")
            self.assertEqual(result, 84)

        self.loop.run_until_complete(_test())

    def test_concurrent_operations(self):
        """Test that operations are properly serialized (not truly concurrent on single device)."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            # These will execute sequentially due to device limitations
            # but the async API should handle them correctly
            tasks = [
                transport.eval_async("1 + 1"),
                transport.eval_async("2 + 2"),
                transport.eval_async("3 + 3"),
            ]

            results = []
            for task in tasks:
                results.append(await task)

            self.assertEqual(results, [2, 4, 6])

        self.loop.run_until_complete(_test())

    def test_raw_paste_mode(self):
        """Test raw paste mode if supported."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            if transport.use_raw_paste:
                # Test with larger code block that benefits from raw paste
                code = "\n".join(["print('line1')" for _ in range(50)])
                stdout, stderr = await transport.exec_raw_async(code)
                self.assertEqual(stderr, b"")
                # Should have 50 lines of output
                lines = stdout.strip().split(b"\r\n")
                self.assertEqual(len(lines), 50)

        self.loop.run_until_complete(_test())

    def test_soft_reset(self):
        """Test soft reset functionality."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            # Set a variable
            stdout, stderr = await transport.exec_raw_async("test_var = 'before reset'")
            self.assertEqual(stderr, b"")

            # Soft reset
            await transport.enter_raw_repl_async(soft_reset=True)

            # Variable should be gone
            stdout, stderr = await transport.exec_raw_async("print(test_var)")
            self.assertIn(b"NameError", stderr)

        self.loop.run_until_complete(_test())

    def test_exit_and_reenter_raw_repl(self):
        """Test exiting and re-entering raw REPL."""

        async def _test():
            transport = await self._connect_transport()

            # Enter raw REPL
            await transport.enter_raw_repl_async(soft_reset=True)
            self.assertTrue(transport.in_raw_repl)

            # Exit raw REPL
            await transport.exit_raw_repl_async()
            self.assertFalse(transport.in_raw_repl)

            # Re-enter raw REPL
            await transport.enter_raw_repl_async(soft_reset=False)
            self.assertTrue(transport.in_raw_repl)

            # Should still be able to execute commands
            result = await transport.eval_async("1 + 1")
            self.assertEqual(result, 2)

        self.loop.run_until_complete(_test())

    def test_large_output(self):
        """Test handling large output from device."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            # Generate large output
            code = "for i in range(100): print(f'Line {i:03d}: ' + 'x' * 50)"
            stdout, stderr = await transport.exec_raw_async(code)
            self.assertEqual(stderr, b"")

            lines = stdout.strip().split(b"\r\n")
            self.assertEqual(len(lines), 100)
            self.assertIn(b"Line 000:", lines[0])
            self.assertIn(b"Line 099:", lines[99])

        self.loop.run_until_complete(_test())

    def test_unicode_handling(self):
        """Test handling of Unicode characters."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            # Test various Unicode characters
            test_strings = [
                "Hello, 世界",
                "Привет, мир",
                "مرحبا بالعالم",
                "🐍 Python",
            ]

            for test_str in test_strings:
                result = await transport.eval_async(f"'{test_str}'")
                self.assertEqual(result, test_str)

        self.loop.run_until_complete(_test())

    def test_import_modules(self):
        """Test importing standard MicroPython modules."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            # Import and use sys module
            code = """
import sys
print(sys.platform)
"""
            stdout = await transport.exec_async(code)
            self.assertGreater(len(stdout), 0)

            # Import and use time module
            code = """
import time
t = time.time()
print(t > 0)
"""
            stdout = await transport.exec_async(code)
            self.assertIn(b"True", stdout)

        self.loop.run_until_complete(_test())


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestAsyncHardwareFilesystem(unittest.TestCase):
    """Filesystem operation tests on hardware."""

    @classmethod
    def setUpClass(cls):
        """Set up test class - verify device is available."""
        if TEST_PORT is None:
            raise unittest.SkipTest("No MicroPython device found")

    def setUp(self):
        """Set up each test."""
        self.transport = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Clean up after each test."""
        if self.transport:
            try:
                self.loop.run_until_complete(self.transport.close_async())
            except:
                pass
        self.loop.close()

    async def _connect_transport(self, timeout=5.0):
        """Helper to connect transport with timeout."""
        self.transport = AsyncSerialTransport(TEST_PORT, baudrate=115200)
        await asyncio.wait_for(self.transport.connect(), timeout=timeout)
        return self.transport

    def test_filesystem_operations(self):
        """Test basic filesystem operations."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            # Create a test file
            code = """
with open('/test_async.txt', 'w') as f:
    f.write('async test content')
print('created')
"""
            stdout = await transport.exec_async(code)
            self.assertIn(b"created", stdout)

            # Read the file back
            code = """
with open('/test_async.txt', 'r') as f:
    content = f.read()
print(content)
"""
            stdout = await transport.exec_async(code)
            self.assertIn(b"async test content", stdout)

            # Delete the file
            code = """
import os
os.remove('/test_async.txt')
print('deleted')
"""
            stdout = await transport.exec_async(code)
            self.assertIn(b"deleted", stdout)

        self.loop.run_until_complete(_test())

    def test_directory_operations(self):
        """Test directory operations."""

        async def _test():
            transport = await self._connect_transport()
            await transport.enter_raw_repl_async(soft_reset=True)

            # Create directory
            code = """
import os
try:
    os.mkdir('/test_async_dir')
    print('created')
except OSError:
    print('already exists')
"""
            stdout = await transport.exec_async(code)
            self.assertTrue(b"created" in stdout or b"already exists" in stdout)

            # List directory
            code = """
import os
items = os.listdir('/')
print('test_async_dir' in items)
"""
            stdout = await transport.exec_async(code)
            self.assertIn(b"True", stdout)

            # Remove directory
            code = """
import os
try:
    os.rmdir('/test_async_dir')
    print('removed')
except OSError as e:
    print(f'error: {e}')
"""
            stdout = await transport.exec_async(code)
            self.assertTrue(b"removed" in stdout or b"error" in stdout)

        self.loop.run_until_complete(_test())


def print_available_ports():
    """Print all available serial ports."""
    try:
        ports = serial.tools.list_ports.comports()
        if not ports:
            print("No serial ports found")
            return

        print("\\nAvailable serial ports:")
        for port in ports:
            print(f"  {port.device:12s} - {port.description}")
    except Exception as e:
        print(f"Error listing ports: {e}")


if __name__ == "__main__":
    print("=" * 72)
    print("MicroPython Async Transport - Hardware Integration Tests")
    print("=" * 72)

    # Parse command line arguments
    if len(sys.argv) > 1 and not sys.argv[1].startswith("Test"):
        TEST_PORT = sys.argv[1]
        # Remove port from argv so unittest doesn't see it
        sys.argv.pop(1)

    if not HAS_ASYNC:
        print(f"ERROR: Async modules not available")
        print(f"Import error: {IMPORT_ERROR}")
        sys.exit(1)

    print_available_ports()

    if TEST_PORT is None:
        TEST_PORT = find_micropython_device()

    if TEST_PORT:
        print(f"\\nTest device: {TEST_PORT}")
    else:
        print("\\nWARNING: No MicroPython device found - tests will be skipped")
        print("\\nTo specify a device manually:")
        print("  python test_async_hardware.py COM20")
        print("  python test_async_hardware.py /dev/ttyUSB0")

    print("=" * 72)
    print()

    # Run tests
    unittest.main(verbosity=2)
