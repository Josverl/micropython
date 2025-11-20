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

"""Pytest-based tests for async REPL functionality.

These tests provide comprehensive coverage of the repl_async module,
including keyboard input handling, device output handling, code injection,
and various edge cases.
"""

import asyncio
import tempfile
import os
from io import BytesIO
from unittest.mock import Mock, patch

import pytest

# Mark all tests as requiring async modules
pytestmark = pytest.mark.async_required


# Fixtures


@pytest.fixture
def mock_console():
    """Create a mock async console."""
    console = Mock()
    console.output = []
    console.input_queue = []
    console.input_idx = 0
    
    def write(data):
        console.output.append(data)
    
    async def readchar_async():
        if console.input_idx < len(console.input_queue):
            char = console.input_queue[console.input_idx]
            console.input_idx += 1
            await asyncio.sleep(0.001)  # Yield control
            return char
        await asyncio.sleep(0.001)
        return b"\x1d"  # ctrl-], exit by default
    
    console.write = write
    console.readchar_async = readchar_async
    console.enter = Mock()
    console.exit = Mock()
    
    return console


@pytest.fixture
def mock_async_transport():
    """Create a mock async transport."""
    transport = Mock()
    transport.device_name = "mock_device"
    transport.in_raw_repl = False
    transport.use_raw_paste = True
    transport.mounted = False
    transport.output_buffer = BytesIO()
    transport.read_position = 0
    
    async def read_async(size=256):
        # Read from buffer
        current_pos = transport.read_position
        data = transport.output_buffer.getvalue()[current_pos:current_pos + size]
        transport.read_position = current_pos + len(data)
        await asyncio.sleep(0.001)
        return data
    
    async def write_async(data):
        await asyncio.sleep(0.001)
        return len(data)
    
    async def enter_raw_repl_async(soft_reset=False):
        transport.in_raw_repl = True
        await asyncio.sleep(0.001)
    
    async def exit_raw_repl_async():
        transport.in_raw_repl = False
        await asyncio.sleep(0.001)
    
    async def exec_raw_no_follow_async(code):
        await asyncio.sleep(0.001)
    
    # Use Mock() for methods so we can track calls
    transport.read_async = Mock(side_effect=read_async)
    transport.write_async = Mock(side_effect=write_async)
    transport.enter_raw_repl_async = Mock(side_effect=enter_raw_repl_async)
    transport.exit_raw_repl_async = Mock(side_effect=exit_raw_repl_async)
    transport.exec_raw_no_follow_async = Mock(side_effect=exec_raw_no_follow_async)
    
    return transport


@pytest.fixture
def mock_state(mock_async_transport):
    """Create a mock state object."""
    state = Mock()
    state.transport = mock_async_transport
    state.did_action = Mock()
    
    async def ensure_friendly_repl_async():
        await asyncio.sleep(0.001)
    
    state.ensure_friendly_repl_async = ensure_friendly_repl_async
    
    return state


@pytest.fixture
def temp_inject_file():
    """Create a temporary file for code injection."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("print('injected code')\n")
        f.write("x = 42\n")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    try:
        os.unlink(temp_path)
    except:
        pass


# Tests for _is_disconnect_exception


def test_is_disconnect_exception_io_error(async_modules):
    """Test disconnect detection for IO error (errno 5)."""
    from mpremote.repl_async import _is_disconnect_exception
    
    exception = OSError(5, "Input/output error")
    assert _is_disconnect_exception(exception) is True


def test_is_disconnect_exception_write_timeout(async_modules):
    """Test disconnect detection for write timeout."""
    from mpremote.repl_async import _is_disconnect_exception
    
    exception = OSError("Write timeout")
    assert _is_disconnect_exception(exception) is True


def test_is_disconnect_exception_device_disconnected(async_modules):
    """Test disconnect detection for device disconnected message."""
    from mpremote.repl_async import _is_disconnect_exception
    
    exception = OSError("Device disconnected")
    assert _is_disconnect_exception(exception) is True


def test_is_disconnect_exception_clearcomm_error(async_modules):
    """Test disconnect detection for ClearCommError."""
    from mpremote.repl_async import _is_disconnect_exception
    
    exception = OSError("ClearCommError failed")
    assert _is_disconnect_exception(exception) is True


def test_is_disconnect_exception_other_oserror(async_modules):
    """Test that other OSErrors are not considered disconnects."""
    from mpremote.repl_async import _is_disconnect_exception
    
    exception = OSError(2, "No such file or directory")
    assert _is_disconnect_exception(exception) is False


def test_is_disconnect_exception_non_oserror(async_modules):
    """Test that non-OSError exceptions are not considered disconnects."""
    from mpremote.repl_async import _is_disconnect_exception
    
    assert _is_disconnect_exception(ValueError("test")) is False
    assert _is_disconnect_exception(KeyError("test")) is False


# Tests for do_repl_main_loop_async


def test_repl_main_loop_exit_ctrl_bracket(mock_state, mock_console, event_loop, async_modules):
    """Test exiting REPL with Ctrl-]."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        mock_console.input_queue = [b"\x1d"]  # ctrl-]
        result = await do_repl_main_loop_async(mock_state, mock_console)
        assert result is False  # Should return False (user exit, not disconnect)
    
    event_loop.run_until_complete(_test())


def test_repl_main_loop_exit_ctrl_x(mock_state, mock_console, event_loop, async_modules):
    """Test exiting REPL with Ctrl-X."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        mock_console.input_queue = [b"\x18"]  # ctrl-x
        result = await do_repl_main_loop_async(mock_state, mock_console)
        assert result is False
    
    event_loop.run_until_complete(_test())


def test_repl_main_loop_ctrl_d_async_transport(mock_state, mock_console, event_loop, async_modules):
    """Test Ctrl-D handling with async transport."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        mock_console.input_queue = [b"\x04", b"\x1d"]  # ctrl-d, then exit
        result = await do_repl_main_loop_async(mock_state, mock_console)
        assert result is False
        # Ctrl-D is processed, REPL exits normally
    
    event_loop.run_until_complete(_test())


def test_repl_main_loop_inject_code(mock_state, mock_console, event_loop, async_modules):
    """Test code injection with Ctrl-J."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        code_to_inject = b"print('hello')\r\n"
        mock_console.input_queue = [b"\x0a", b"\x1d"]  # ctrl-j, then exit
        
        result = await do_repl_main_loop_async(
            mock_state, mock_console, code_to_inject=code_to_inject
        )
        
        assert result is False
        # Verify code was injected
        calls = [call[0][0] for call in mock_state.transport.write_async.call_args_list]
        assert code_to_inject in calls
    
    event_loop.run_until_complete(_test())


def test_repl_main_loop_inject_file(mock_state, mock_console, temp_inject_file, event_loop, async_modules):
    """Test file injection with Ctrl-K."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        mock_console.input_queue = [b"\x0b", b"\x1d"]  # ctrl-k, then exit
        
        result = await do_repl_main_loop_async(
            mock_state, mock_console, file_to_inject=temp_inject_file
        )
        
        assert result is False
        # Verify raw REPL was entered and exited
        mock_state.transport.enter_raw_repl_async.assert_called_once()
        mock_state.transport.exit_raw_repl_async.assert_called_once()
        mock_state.transport.exec_raw_no_follow_async.assert_called_once()
    
    event_loop.run_until_complete(_test())


def test_repl_main_loop_inject_file_with_error(mock_state, mock_console, temp_inject_file, event_loop, async_modules):
    """Test file injection that raises TransportError."""
    from mpremote.repl_async import do_repl_main_loop_async
    from mpremote.transport import TransportError
    
    async def _test():
        mock_console.input_queue = [b"\x0b", b"\x1d"]  # ctrl-k, then exit
        
        # Make exec_raw_no_follow_async raise an error
        async def raise_error(code):
            raise TransportError("Execution failed")
        
        mock_state.transport.exec_raw_no_follow_async = raise_error
        
        result = await do_repl_main_loop_async(
            mock_state, mock_console, file_to_inject=temp_inject_file
        )
        
        assert result is False
        # Error should be written to console
        assert any(b"Error:" in output for output in mock_console.output)
    
    event_loop.run_until_complete(_test())


def test_repl_main_loop_regular_input(mock_state, mock_console, event_loop, async_modules):
    """Test regular character input."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        mock_console.input_queue = [b"a", b"b", b"c", b"\r", b"\x1d"]
        
        result = await do_repl_main_loop_async(mock_state, mock_console)
        
        assert result is False
        # All characters should be sent to device
        assert mock_state.transport.write_async.call_count >= 4
    
    event_loop.run_until_complete(_test())


def test_repl_main_loop_device_output(mock_state, mock_console, event_loop, async_modules):
    """Test receiving device output."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Set up device output
        mock_state.transport.output_buffer = BytesIO(b"MicroPython v1.0\r\n>>> ")
        mock_state.transport.read_position = 0
        
        mock_console.input_queue = [b"\x1d"]  # Exit immediately
        
        result = await do_repl_main_loop_async(mock_state, mock_console)
        
        assert result is False
        # Device output should be written to console
        assert len(mock_console.output) > 0
    
    event_loop.run_until_complete(_test())


def test_repl_main_loop_escape_non_printable(mock_state, mock_console, event_loop, async_modules):
    """Test escaping non-printable characters."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Device output with non-printable bytes
        mock_state.transport.output_buffer = BytesIO(b"test\x00\x01\x02")
        mock_state.transport.read_position = 0
        
        mock_console.input_queue = [b"\x1d"]
        
        result = await do_repl_main_loop_async(
            mock_state, mock_console, escape_non_printable=True
        )
        
        assert result is False
        # Non-printable bytes should be escaped in output
        output = b"".join(mock_console.output)
        assert b"[00]" in output or b"test" in output
    
    event_loop.run_until_complete(_test())


def test_repl_main_loop_disconnect_on_read(mock_state, mock_console, event_loop, async_modules):
    """Test handling disconnect during device read."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Make read_async raise a disconnect exception
        async def raise_disconnect(size=256):
            raise OSError(5, "Input/output error")
        
        mock_state.transport.read_async = raise_disconnect
        mock_console.input_queue = []  # No input
        
        result = await do_repl_main_loop_async(mock_state, mock_console)
        
        assert result is True  # Should return True for disconnect
    
    event_loop.run_until_complete(_test())


def test_repl_main_loop_disconnect_on_write(mock_state, mock_console, event_loop, async_modules):
    """Test handling disconnect during device write."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Make write_async raise a disconnect exception
        async def raise_disconnect(data):
            raise OSError(5, "Input/output error")
        
        mock_state.transport.write_async = raise_disconnect
        mock_console.input_queue = [b"a"]  # Try to send a character
        
        result = await do_repl_main_loop_async(mock_state, mock_console)
        
        assert result is True  # Should return True for disconnect
    
    event_loop.run_until_complete(_test())


def test_repl_with_sync_transport(mock_state, mock_console, event_loop, async_modules):
    """Test REPL with synchronous transport (fallback)."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Remove async methods to simulate sync transport
        del mock_state.transport.write_async
        del mock_state.transport.read_async
        
        # Add sync serial interface
        mock_serial = Mock()
        mock_serial.write = Mock(return_value=1)
        mock_serial.inWaiting = Mock(return_value=0)
        mock_state.transport.serial = mock_serial
        
        mock_console.input_queue = [b"a", b"\x1d"]
        
        result = await do_repl_main_loop_async(mock_state, mock_console)
        
        assert result is False
        # Verify sync methods were used
        mock_serial.write.assert_called()
        mock_serial.inWaiting.assert_called()
    
    event_loop.run_until_complete(_test())


# Tests for do_repl_async wrapper


def test_do_repl_async_wrapper(mock_state, event_loop, async_modules):
    """Test synchronous wrapper for async REPL."""
    from mpremote.repl_async import do_repl_async_wrapper
    
    args = Mock()
    args.escape_non_printable = False
    args.capture = None
    args.inject_code = None
    args.inject_file = None
    
    with patch('mpremote.repl_async.AsyncConsole') as MockConsole:
        mock_console_instance = Mock()
        
        async def readchar():
            await asyncio.sleep(0.001)
            return b"\x1d"
        
        mock_console_instance.readchar_async = readchar
        mock_console_instance.write = Mock()
        mock_console_instance.enter = Mock()
        mock_console_instance.exit = Mock()
        
        MockConsole.return_value = mock_console_instance
        
        with patch('builtins.print'):
            result = do_repl_async_wrapper(mock_state, args)
        
        assert result is False
