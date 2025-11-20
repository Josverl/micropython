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

"""Tests for repl_async using MicroPython unix port as backend.

This test uses the MicroPython unix port via pty/subprocess to test
the async REPL functionality without requiring hardware.
"""

import sys
import os
import unittest
import asyncio
import pty
import subprocess
from pathlib import Path

# Add mpremote to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from mpremote.repl_async import do_repl_main_loop_async
    from mpremote.console_async import AsyncConsole
    from mpremote.transport_async import AsyncTransport

    HAS_ASYNC = True
except ImportError as e:
    HAS_ASYNC = False
    IMPORT_ERROR = str(e)

# Find MicroPython unix port binary
MICROPYTHON_BIN = None
for possible_path in [
    Path(__file__).parent.parent.parent.parent
    / "ports"
    / "unix"
    / "build-standard"
    / "micropython",
    Path(__file__).parent.parent.parent.parent / "ports" / "unix" / "build" / "micropython",
    Path("/usr/local/bin/micropython"),
    Path("/usr/bin/micropython"),
]:
    if possible_path.exists() and possible_path.is_file():
        MICROPYTHON_BIN = str(possible_path)
        break


class MockAsyncTransportUnix(AsyncTransport):
    """Mock async transport that uses unix port via pty."""

    def __init__(self, process, master_fd):
        self.process = process
        self.master_fd = master_fd
        self.device_name = "unix-pty"
        self.in_raw_repl = False
        self.use_raw_paste = True
        self.mounted = False

    async def read_async(self, size=1):
        """Read bytes from the pty."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, os.read, self.master_fd, size)

    async def write_async(self, data):
        """Write bytes to the pty."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, os.write, self.master_fd, data)

    async def read_until_async(self, ending, timeout=10):
        """Read until a specific byte sequence is found."""
        data = b""
        start_time = asyncio.get_event_loop().time()
        while True:
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError(f"Timeout waiting for {ending}")
            try:
                chunk = await asyncio.wait_for(self.read_async(1), timeout=0.1)
                data += chunk
                if data.endswith(ending):
                    return data
            except asyncio.TimeoutError:
                continue

    async def close_async(self):
        """Close the transport."""
        try:
            self.process.terminate()
            await asyncio.sleep(0.1)
            if self.process.poll() is None:
                self.process.kill()
            os.close(self.master_fd)
        except:
            pass


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
@unittest.skipUnless(MICROPYTHON_BIN, "MicroPython unix port not found")
class TestREPLAsyncUnixBackend(unittest.TestCase):
    """Test async REPL using unix backend."""

    def setUp(self):
        """Set up test - start MicroPython process."""
        # Create pty pair
        master_fd, slave_fd = pty.openpty()

        # Start MicroPython on the slave pty
        self.process = subprocess.Popen(
            [MICROPYTHON_BIN], stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, close_fds=True
        )

        # Close slave fd in parent - child has it
        os.close(slave_fd)

        self.master_fd = master_fd
        self.transport = MockAsyncTransportUnix(self.process, master_fd)

    def tearDown(self):
        """Clean up - terminate MicroPython process."""
        try:
            self.process.terminate()
            self.process.wait(timeout=1)
        except:
            self.process.kill()
        try:
            os.close(self.master_fd)
        except:
            pass

    def test_unix_backend_starts(self):
        """Test that MicroPython unix backend starts correctly."""
        # Wait a bit for process to start
        import time

        time.sleep(0.2)

        self.assertIsNotNone(self.process)
        self.assertIsNone(self.process.poll(), "Process should be running")

    def test_basic_repl_interaction(self):
        """Test basic REPL interaction via pty."""
        import time

        time.sleep(0.2)  # Wait for REPL to start

        # Send a command
        os.write(self.master_fd, b"print('hello')\r")
        time.sleep(0.1)

        # Read response
        try:
            output = os.read(self.master_fd, 1024)
            self.assertIn(b"hello", output)
        except OSError:
            self.skipTest("Could not read from pty")

    async def _test_async_transport_read_write(self):
        """Test async read/write to transport."""
        import time

        time.sleep(0.2)  # Wait for REPL to start

        # Clear initial output
        try:
            while True:
                chunk = await asyncio.wait_for(self.transport.read_async(1024), timeout=0.1)
                if not chunk:
                    break
        except asyncio.TimeoutError:
            pass

        # Send command
        await self.transport.write_async(b"1+1\r")
        await asyncio.sleep(0.1)

        # Read response
        output = b""
        for _ in range(10):
            try:
                chunk = await asyncio.wait_for(self.transport.read_async(1024), timeout=0.1)
                output += chunk
                if b"2" in output:
                    break
            except asyncio.TimeoutError:
                break

        self.assertIn(b"2", output, "Should see result of 1+1")

    def test_async_transport_read_write(self):
        """Wrapper to run async test."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_async_transport_read_write())

    def test_transport_attributes(self):
        """Test that mock transport has required attributes."""
        self.assertEqual(self.transport.device_name, "unix-pty")
        self.assertFalse(self.transport.in_raw_repl)
        self.assertTrue(self.transport.use_raw_paste)
        self.assertFalse(self.transport.mounted)
        self.assertTrue(hasattr(self.transport, "read_async"))
        self.assertTrue(hasattr(self.transport, "write_async"))


@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
class TestREPLAsyncFunctions(unittest.TestCase):
    """Test REPL async functions without actual backend."""

    def test_repl_main_loop_async_exists(self):
        """Test that do_repl_main_loop_async function exists."""
        self.assertTrue(callable(do_repl_main_loop_async))
        self.assertTrue(asyncio.iscoroutinefunction(do_repl_main_loop_async))

    def test_repl_function_signature(self):
        """Test that REPL function has correct signature."""
        import inspect

        sig = inspect.signature(do_repl_main_loop_async)
        params = list(sig.parameters.keys())

        # Check required parameters
        self.assertIn("state", params)
        self.assertIn("console", params)

        # Check keyword-only parameters
        self.assertIn("escape_non_printable", params)
        self.assertIn("code_to_inject", params)
        self.assertIn("file_to_inject", params)


if __name__ == "__main__":
    # Print diagnostic info
    print("=" * 72)
    print("REPL Async Unix Backend Tests")
    print("=" * 72)
    print(f"MicroPython binary: {MICROPYTHON_BIN or 'NOT FOUND'}")
    print(f"Async modules available: {HAS_ASYNC}")
    if not HAS_ASYNC:
        print(f"Import error: {IMPORT_ERROR}")
    print("=" * 72)
    print()

    unittest.main(verbosity=2)
