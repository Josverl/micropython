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

"""Integration tests for repl_async using MicroPython unix port.

This test exercises the actual async REPL loop with a real MicroPython
backend to achieve meaningful code coverage.
"""

import sys
import os
import unittest
import asyncio
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock

# POSIX-only imports
try:
    import pty
    HAS_PTY = True
except ImportError:
    HAS_PTY = False

# Add mpremote to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from mpremote.repl_async import do_repl_main_loop_async, do_repl_async, do_repl_async_wrapper
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
]:
    if possible_path.exists() and possible_path.is_file():
        MICROPYTHON_BIN = str(possible_path)
        break


class MockConsole:
    """Mock console for testing."""

    def __init__(self):
        self.output = []
        self.input_queue = []
        self.input_idx = 0

    def enter(self):
        pass

    def exit(self):
        pass

    def write(self, data):
        self.output.append(data)

    async def readchar_async(self):
        """Read a character from input queue."""
        if self.input_idx < len(self.input_queue):
            char = self.input_queue[self.input_idx]
            self.input_idx += 1
            return char
        # Return exit character when no more input
        await asyncio.sleep(0.01)
        return b"\x1d"  # ctrl-]


class MockTransportUnix(AsyncTransport):
    """Mock async transport for unix backend."""

    def __init__(self, process, master_fd):
        self.process = process
        self.master_fd = master_fd
        self.device_name = "unix-pty"
        self.in_raw_repl = False
        self.use_raw_paste = True
        self.mounted = False
        self.serial = Mock()  # Mock serial for compatibility

    async def read_async(self, size=1):
        """Read bytes from the pty."""
        loop = asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, os.read, self.master_fd, size)
            return data
        except OSError:
            return b""

    async def write_async(self, data):
        """Write bytes to the pty."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, os.write, self.master_fd, data)

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
@unittest.skipUnless(HAS_PTY, "PTY not available on this platform")
@unittest.skipUnless(HAS_ASYNC, "Async modules not available")
@unittest.skipUnless(MICROPYTHON_BIN, "MicroPython unix port not found")
class TestREPLAsyncIntegration(unittest.TestCase):
    """Integration tests for async REPL."""

    def setUp(self):
        """Set up test - start MicroPython process."""
        # Create pty pair
        master_fd, slave_fd = pty.openpty()

        # Start MicroPython on the slave pty
        self.process = subprocess.Popen(
            [MICROPYTHON_BIN], stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, close_fds=True
        )

        # Close slave fd in parent
        os.close(slave_fd)

        self.master_fd = master_fd
        self.transport = MockTransportUnix(self.process, master_fd)

        # Create mock state
        self.state = Mock()
        self.state.transport = self.transport
        self.state.did_action = Mock()

    def tearDown(self):
        """Clean up."""
        try:
            self.process.terminate()
            self.process.wait(timeout=1)
        except:
            self.process.kill()
        try:
            os.close(self.master_fd)
        except:
            pass

    async def _test_repl_main_loop_basic(self):
        """Test basic REPL main loop."""
        import time

        time.sleep(0.3)  # Wait for REPL to start

        # Create mock console with exit command
        console = MockConsole()
        console.input_queue = [b"\x1d"]  # ctrl-], exit immediately

        # Run REPL loop
        result = await asyncio.wait_for(
            do_repl_main_loop_async(
                self.state,
                console,
                escape_non_printable=False,
                code_to_inject=None,
                file_to_inject=None,
            ),
            timeout=2.0,
        )

        # Should have exited normally (not disconnected)
        self.assertFalse(result)

    def test_repl_main_loop_basic(self):
        """Wrapper to run async test."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._test_repl_main_loop_basic())
        finally:
            loop.close()

    async def _test_repl_with_code_injection(self):
        """Test REPL with code injection."""
        import time

        time.sleep(0.3)

        # Create mock console with code injection and exit
        console = MockConsole()
        # Send ctrl-j (inject code), then exit
        console.input_queue = [b"\x0a", b"\x1d"]

        # Run REPL loop with code to inject
        result = await asyncio.wait_for(
            do_repl_main_loop_async(
                self.state,
                console,
                escape_non_printable=False,
                code_to_inject=b"print('injected')\r",
                file_to_inject=None,
            ),
            timeout=2.0,
        )

        self.assertFalse(result)

    def test_repl_with_code_injection(self):
        """Wrapper to run async test."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._test_repl_with_code_injection())
        finally:
            loop.close()

    async def _test_repl_with_file_injection(self):
        """Test REPL with file injection."""
        import time

        time.sleep(0.3)

        # Create temporary Python file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("print('from file')\n")
            temp_file = f.name

        try:
            # Create mock console
            console = MockConsole()
            # Send ctrl-k (inject file), then exit
            console.input_queue = [b"\x0b", b"\x1d"]

            # Mock enter_raw_repl_async
            self.transport.enter_raw_repl_async = Mock(return_value=asyncio.Future())
            self.transport.enter_raw_repl_async.return_value.set_result(None)

            # Mock exec_raw_no_follow_async
            self.transport.exec_raw_no_follow_async = Mock(return_value=asyncio.Future())
            self.transport.exec_raw_no_follow_async.return_value.set_result(None)

            # Run REPL loop
            result = await asyncio.wait_for(
                do_repl_main_loop_async(
                    self.state,
                    console,
                    escape_non_printable=False,
                    code_to_inject=None,
                    file_to_inject=temp_file,
                ),
                timeout=2.0,
            )

            self.assertFalse(result)
        finally:
            os.unlink(temp_file)

    def test_repl_with_file_injection(self):
        """Wrapper to run async test."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._test_repl_with_file_injection())
        finally:
            loop.close()

    def test_do_repl_async_exists(self):
        """Test that do_repl_async function exists."""
        self.assertTrue(callable(do_repl_async))
        self.assertTrue(asyncio.iscoroutinefunction(do_repl_async))

    def test_do_repl_async_wrapper_exists(self):
        """Test that do_repl_async_wrapper function exists."""
        self.assertTrue(callable(do_repl_async_wrapper))
        # Wrapper should not be async
        self.assertFalse(asyncio.iscoroutinefunction(do_repl_async_wrapper))


if __name__ == "__main__":
    print("=" * 72)
    print("REPL Async Integration Tests")
    print("=" * 72)
    print(f"MicroPython binary: {MICROPYTHON_BIN or 'NOT FOUND'}")
    print(f"Async modules available: {HAS_ASYNC}")
    if not HAS_ASYNC:
        print(f"Import error: {IMPORT_ERROR}")
    print("=" * 72)
    print()

    unittest.main(verbosity=2)
