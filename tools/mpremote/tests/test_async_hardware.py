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
    pytest test_async_hardware.py

    # Test with specific port
    pytest --device=COM20 test_async_hardware.py
    pytest --device=/dev/ttyUSB0 test_async_hardware.py

    # Run specific test
    pytest --device=COM20 test_async_hardware.py::test_basic_connection

Requirements:
    - A MicroPython device connected via serial/USB-CDC
    - pyserial-asyncio installed
"""

import asyncio
import pytest


pytestmark = [pytest.mark.async_required, pytest.mark.hardware_required, pytest.mark.serial_required]


def test_basic_connection(hardware_device, async_modules, event_loop):
    """Test basic connection and disconnection."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        
        assert transport.reader is not None
        assert transport.writer is not None
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_enter_raw_repl(hardware_device, async_modules, event_loop):
    """Test entering raw REPL mode."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        
        await transport.enter_raw_repl_async(soft_reset=True)
        assert transport.in_raw_repl is True
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_exec_raw_async(hardware_device, async_modules, event_loop):
    """Test executing raw commands."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        # Simple print command
        stdout, stderr = await transport.exec_raw_async("print('hello')")
        assert stdout.strip() == b"hello"
        assert stderr == b""

        # Command with result
        stdout, stderr = await transport.exec_raw_async("print(2 + 2)")
        assert stdout.strip() == b"4"
        assert stderr == b""
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_exec_with_error(hardware_device, async_modules, event_loop):
    """Test executing command that raises an error."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        # Command that raises NameError
        stdout, stderr = await transport.exec_raw_async("print(undefined_var)")
        assert stdout == b""
        assert b"NameError" in stderr
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_eval_async(hardware_device, async_modules, event_loop):
    """Test evaluating expressions."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        # Arithmetic
        result = await transport.eval_async("2 + 2")
        assert result == 4

        # String
        result = await transport.eval_async("'hello world'")
        assert result == "hello world"

        # List
        result = await transport.eval_async("[1, 2, 3]")
        assert result == [1, 2, 3]

        # Dictionary
        result = await transport.eval_async("{'a': 1, 'b': 2}")
        assert result == {"a": 1, "b": 2}
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_exec_async(hardware_device, async_modules, event_loop):
    """Test executing multi-line code."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        code = """
x = 10
y = 20
print(x + y)
"""
        stdout = await transport.exec_async(code)
        assert stdout.strip() == b"30"
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_multiple_commands(hardware_device, async_modules, event_loop):
    """Test executing multiple commands in sequence."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        # Set a variable
        stdout, stderr = await transport.exec_raw_async("x = 42")
        assert stderr == b""

        # Read it back
        result = await transport.eval_async("x")
        assert result == 42

        # Modify it
        stdout, stderr = await transport.exec_raw_async("x = x * 2")
        assert stderr == b""

        # Read modified value
        result = await transport.eval_async("x")
        assert result == 84
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_concurrent_operations(hardware_device, async_modules, event_loop):
    """Test that operations are properly serialized."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        # These will execute sequentially due to device limitations
        results = []
        for expr in ["1 + 1", "2 + 2", "3 + 3"]:
            result = await transport.eval_async(expr)
            results.append(result)

        assert results == [2, 4, 6]
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


@pytest.mark.slow
def test_raw_paste_mode(hardware_device, async_modules, event_loop):
    """Test raw paste mode if supported."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        if transport.use_raw_paste:
            # Test with larger code block that benefits from raw paste
            code = "\n".join(["print('line1')" for _ in range(50)])
            stdout, stderr = await transport.exec_raw_async(code)
            assert stderr == b""
            # Should have 50 lines of output
            lines = stdout.strip().split(b"\r\n")
            assert len(lines) == 50
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_soft_reset(hardware_device, async_modules, event_loop):
    """Test soft reset functionality."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        # Set a variable
        stdout, stderr = await transport.exec_raw_async("test_var = 'before reset'")
        assert stderr == b""

        # Soft reset
        await transport.enter_raw_repl_async(soft_reset=True)

        # Variable should be gone
        stdout, stderr = await transport.exec_raw_async("print(test_var)")
        assert b"NameError" in stderr
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_exit_and_reenter_raw_repl(hardware_device, async_modules, event_loop):
    """Test exiting and re-entering raw REPL."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        
        # Enter raw REPL
        await transport.enter_raw_repl_async(soft_reset=True)
        assert transport.in_raw_repl is True

        # Exit raw REPL
        await transport.exit_raw_repl_async()
        assert transport.in_raw_repl is False

        # Re-enter raw REPL
        await transport.enter_raw_repl_async(soft_reset=False)
        assert transport.in_raw_repl is True

        # Should still be able to execute commands
        result = await transport.eval_async("1 + 1")
        assert result == 2
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


@pytest.mark.slow
def test_large_output(hardware_device, async_modules, event_loop):
    """Test handling large output from device."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        # Generate large output
        code = "for i in range(100): print(f'Line {i:03d}: ' + 'x' * 50)"
        stdout, stderr = await transport.exec_raw_async(code)
        assert stderr == b""

        lines = stdout.strip().split(b"\r\n")
        assert len(lines) == 100
        assert b"Line 000:" in lines[0]
        assert b"Line 099:" in lines[99]
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_unicode_handling(hardware_device, async_modules, event_loop):
    """Test handling of Unicode characters."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
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
            assert result == test_str
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_import_modules(hardware_device, async_modules, event_loop):
    """Test importing standard MicroPython modules."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        # Import and use sys module
        code = """
import sys
print(sys.platform)
"""
        stdout = await transport.exec_async(code)
        assert len(stdout) > 0

        # Import and use time module
        code = """
import time
t = time.time()
print(t > 0)
"""
        stdout = await transport.exec_async(code)
        assert b"True" in stdout
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


# Filesystem Tests


def test_filesystem_operations(hardware_device, async_modules, event_loop):
    """Test basic filesystem operations."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        # Detect writable filesystem location (handles pyboard, esp32, rp2, etc.)
        code = """
import os
import sys
# Try to find a writable filesystem
writable_path = None
test_paths = ['/', '/flash', '/sd']
for path in test_paths:
    try:
        # Check if path exists and is writable
        items = os.listdir(path)
        # Try to create a test file
        test_file = path + '/.test_write'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        writable_path = path
        break
    except (OSError, AttributeError):
        continue
print(writable_path if writable_path else 'NONE')
"""
        stdout = await transport.exec_async(code)
        writable_path = stdout.strip().decode()
        
        if writable_path == 'NONE':
            # Skip test if no writable filesystem available
            pytest.skip("No writable filesystem available on device")
            return

        # Create a test file
        code = f"""
with open('{writable_path}/test_async.txt', 'w') as f:
    f.write('async test content')
print('created')
"""
        stdout = await transport.exec_async(code)
        assert b"created" in stdout

        # Read the file back
        code = f"""
with open('{writable_path}/test_async.txt', 'r') as f:
    content = f.read()
print(content)
"""
        stdout = await transport.exec_async(code)
        assert b"async test content" in stdout

        # Delete the file
        code = f"""
import os
os.remove('{writable_path}/test_async.txt')
print('deleted')
"""
        stdout = await transport.exec_async(code)
        assert b"deleted" in stdout
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_directory_operations(hardware_device, async_modules, event_loop):
    """Test directory operations."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)

        # Detect writable filesystem location
        code = """
import os
writable_path = None
test_paths = ['/', '/flash', '/sd']
for path in test_paths:
    try:
        items = os.listdir(path)
        test_file = path + '/.test_write'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        writable_path = path
        break
    except (OSError, AttributeError):
        continue
print(writable_path if writable_path else 'NONE')
"""
        stdout = await transport.exec_async(code)
        writable_path = stdout.strip().decode()
        
        if writable_path == 'NONE':
            pytest.skip("No writable filesystem available on device")
            return

        # Create directory
        code = f"""
import os
try:
    os.mkdir('{writable_path}/test_async_dir')
    print('created')
except OSError:
    print('already exists')
"""
        stdout = await transport.exec_async(code)
        assert b"created" in stdout or b"already exists" in stdout

        # List directory
        code = f"""
import os
items = os.listdir('{writable_path}')
print('test_async_dir' in items)
"""
        stdout = await transport.exec_async(code)
        assert b"True" in stdout

        # Remove directory
        code = f"""
import os
try:
    os.rmdir('{writable_path}/test_async_dir')
    print('removed')
except OSError as e:
    print(f'error: {{e}}')
"""
        stdout = await transport.exec_async(code)
        assert b"removed" in stdout or b"error" in stdout
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())

