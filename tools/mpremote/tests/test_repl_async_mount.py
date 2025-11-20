#!/usr/bin/env python3
#
# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2025 Jos Verlinde
#

"""Tests for mount functionality and ctrl-D handling in repl_async.

These tests cover the special handling needed when filesystem is mounted,
including the write_ctrl_d method branching logic.
"""

import asyncio
from unittest.mock import Mock, AsyncMock, call

import pytest

pytestmark = pytest.mark.async_required


@pytest.fixture
def mock_state_with_async_transport():
    """Create mock state with async transport methods."""
    mock_state = Mock()
    mock_transport = Mock(spec=[])
    
    # Add async methods explicitly
    mock_transport.write_async = AsyncMock(return_value=None)
    
    # Mock read_async to return empty bytes (no device output) to avoid hanging
    async def mock_read_async(n):
        await asyncio.sleep(0.001)  # Small delay to yield control
        return b""
    
    mock_transport.read_async = mock_read_async
    mock_transport.in_raw_repl = False
    
    mock_state.transport = mock_transport
    mock_state.did_action = Mock()
    
    return mock_state


@pytest.fixture
def mock_console_with_queue():
    """Create mock console with input queue."""
    from mpremote.repl_async import AsyncConsole
    
    mock_console = Mock(spec=AsyncConsole)
    mock_console.output = []
    mock_console.input_queue = []
    mock_console.input_idx = 0
    
    async def readchar():
        if mock_console.input_idx < len(mock_console.input_queue):
            char = mock_console.input_queue[mock_console.input_idx]
            mock_console.input_idx += 1
            return char
        await asyncio.sleep(0.001)
        return b"\x1d"  # ctrl-]
    
    mock_console.readchar_async = readchar
    mock_console.write = Mock()
    mock_console.enter = Mock()
    mock_console.exit = Mock()
    
    return mock_console


def test_ctrl_d_with_write_ctrl_d_method(mock_state_with_async_transport, mock_console_with_queue, event_loop, async_modules):
    """Test ctrl-D handling when transport has write_ctrl_d method (mounted filesystem)."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Add write_ctrl_d method (used when filesystem is mounted)
        mock_state_with_async_transport.transport.write_ctrl_d = Mock()
        mock_state_with_async_transport.transport.mounted = True
        
        # Simulate ctrl-D followed by exit
        mock_console_with_queue.input_queue = [b"\x04", b"\x1d"]
        
        result = await do_repl_main_loop_async(
            mock_state_with_async_transport,
            mock_console_with_queue,
            escape_non_printable=False
        )
        
        # Verify write_ctrl_d was called instead of write_async
        mock_state_with_async_transport.transport.write_ctrl_d.assert_called_once()
        assert mock_state_with_async_transport.transport.write_ctrl_d.call_args[0][0] == mock_console_with_queue.write
        
        # Verify write_async was NOT called for ctrl-D
        calls = mock_state_with_async_transport.transport.write_async.call_args_list
        assert all(call[0][0] != b"\x04" for call in calls)
        
        assert result is False
    
    event_loop.run_until_complete(_test())


def test_ctrl_d_without_write_ctrl_d_uses_write_async(mock_state_with_async_transport, mock_console_with_queue, event_loop, async_modules):
    """Test ctrl-D handling when transport doesn't have write_ctrl_d (normal async)."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Ensure write_ctrl_d method doesn't exist
        if hasattr(mock_state_with_async_transport.transport, 'write_ctrl_d'):
            delattr(mock_state_with_async_transport.transport, 'write_ctrl_d')
        
        # Simulate ctrl-D followed by exit
        mock_console_with_queue.input_queue = [b"\x04", b"\x1d"]
        
        result = await do_repl_main_loop_async(
            mock_state_with_async_transport,
            mock_console_with_queue,
            escape_non_printable=False
        )
        
        # Verify write_async was called with ctrl-D
        calls = mock_state_with_async_transport.transport.write_async.call_args_list
        assert any(call[0][0] == b"\x04" for call in calls)
        
        assert result is False
    
    event_loop.run_until_complete(_test())


def test_ctrl_d_fallback_to_sync_serial(mock_state_with_async_transport, mock_console_with_queue, event_loop, async_modules):
    """Test ctrl-D uses write_async when available (sync serial not used in async loop)."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Ensure no write_ctrl_d method
        if hasattr(mock_state_with_async_transport.transport, 'write_ctrl_d'):
            delattr(mock_state_with_async_transport.transport, 'write_ctrl_d')
        
        # Simulate ctrl-D followed by exit
        mock_console_with_queue.input_queue = [b"\x04", b"\x1d"]
        
        result = await do_repl_main_loop_async(
            mock_state_with_async_transport,
            mock_console_with_queue,
            escape_non_printable=False
        )
        
        # Verify write_async was called (async context uses async methods)
        calls = mock_state_with_async_transport.transport.write_async.call_args_list
        assert len(calls) > 0, "write_async should be called in async context"
        
        assert result is False
    
    event_loop.run_until_complete(_test())


def test_regular_input_with_mounted_filesystem(mock_state_with_async_transport, mock_console_with_queue, event_loop, async_modules):
    """Test regular character input when filesystem is mounted."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Add write_ctrl_d method (mounted filesystem)
        mock_state_with_async_transport.transport.write_ctrl_d = Mock()
        mock_state_with_async_transport.transport.mounted = True
        
        # Simulate regular input followed by exit
        mock_console_with_queue.input_queue = [b"a", b"b", b"c", b"\x1d"]
        
        result = await do_repl_main_loop_async(
            mock_state_with_async_transport,
            mock_console_with_queue,
            escape_non_printable=False
        )
        
        # Verify write_async was called for regular characters
        calls = mock_state_with_async_transport.transport.write_async.call_args_list
        assert any(call[0][0] == b"a" for call in calls)
        assert any(call[0][0] == b"b" for call in calls)
        assert any(call[0][0] == b"c" for call in calls)
        
        # Verify write_ctrl_d was NOT called for regular characters
        mock_state_with_async_transport.transport.write_ctrl_d.assert_not_called()
        
        assert result is False
    
    event_loop.run_until_complete(_test())


def test_ctrl_j_code_injection_with_write_async(mock_state_with_async_transport, mock_console_with_queue, event_loop, async_modules):
    """Test ctrl-J code injection uses write_async when available."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Simulate ctrl-J (code injection) followed by exit
        mock_console_with_queue.input_queue = [b"\x0a", b"\x1d"]
        code_to_inject = b"print('injected')\r\n"
        
        result = await do_repl_main_loop_async(
            mock_state_with_async_transport,
            mock_console_with_queue,
            escape_non_printable=False,
            code_to_inject=code_to_inject
        )
        
        # Verify write_async was called with injected code
        calls = mock_state_with_async_transport.transport.write_async.call_args_list
        assert any(call[0][0] == code_to_inject for call in calls)
        
        assert result is False
    
    event_loop.run_until_complete(_test())


def test_ctrl_j_code_injection_fallback_to_sync(mock_state_with_async_transport, mock_console_with_queue, event_loop, async_modules):
    """Test ctrl-J code injection fallback to sync serial.write."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Remove write_async to trigger sync fallback
        delattr(mock_state_with_async_transport.transport, 'write_async')
        
        # Add sync serial interface
        mock_serial = Mock()
        mock_serial.write = Mock(return_value=1)
        mock_serial.inWaiting = Mock(return_value=0)
        mock_state_with_async_transport.transport.serial = mock_serial
        
        # Simulate ctrl-J (code injection) followed by exit
        mock_console_with_queue.input_queue = [b"\x0a", b"\x1d"]
        code_to_inject = b"print('injected')\r\n"
        
        result = await do_repl_main_loop_async(
            mock_state_with_async_transport,
            mock_console_with_queue,
            escape_non_printable=False,
            code_to_inject=code_to_inject
        )
        
        # Verify serial.write was called with injected code
        calls = mock_serial.write.call_args_list
        assert any(call[0][0] == code_to_inject for call in calls)
        
        assert result is False
    
    event_loop.run_until_complete(_test())


def test_ctrl_k_file_injection_with_async_methods(mock_state_with_async_transport, mock_console_with_queue, event_loop, async_modules):
    """Test ctrl-K file injection uses async methods when available."""
    from mpremote.repl_async import do_repl_main_loop_async
    import tempfile
    import os
    
    async def _test():
        # Add async REPL methods
        mock_state_with_async_transport.transport.enter_raw_repl_async = AsyncMock()
        mock_state_with_async_transport.transport.exec_raw_no_follow_async = AsyncMock()
        mock_state_with_async_transport.transport.exit_raw_repl_async = AsyncMock()
        
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("print('from file')\n")
            temp_file = f.name
        
        try:
            # Simulate ctrl-K (file injection) followed by exit
            mock_console_with_queue.input_queue = [b"\x0b", b"\x1d"]
            
            result = await do_repl_main_loop_async(
                mock_state_with_async_transport,
                mock_console_with_queue,
                escape_non_printable=False,
                file_to_inject=temp_file
            )
            
            # Verify async methods were called
            mock_state_with_async_transport.transport.enter_raw_repl_async.assert_called_once()
            mock_state_with_async_transport.transport.exec_raw_no_follow_async.assert_called_once()
            mock_state_with_async_transport.transport.exit_raw_repl_async.assert_called_once()
            
            # Verify file content was passed
            call_args = mock_state_with_async_transport.transport.exec_raw_no_follow_async.call_args[0][0]
            assert b"print('from file')" in call_args
            
            assert result is False
        finally:
            os.unlink(temp_file)
    
    event_loop.run_until_complete(_test())


def test_ctrl_k_file_injection_checks_async_first(mock_state_with_async_transport, mock_console_with_queue, event_loop, async_modules):
    """Test ctrl-K file injection prioritizes async methods over sync."""
    from mpremote.repl_async import do_repl_main_loop_async
    import tempfile
    import os
    
    async def _test():
        # Add both sync and async REPL methods to test priority
        mock_state_with_async_transport.transport.enter_raw_repl_async = AsyncMock()
        mock_state_with_async_transport.transport.exec_raw_no_follow_async = AsyncMock()
        mock_state_with_async_transport.transport.exit_raw_repl_async = AsyncMock()
        mock_state_with_async_transport.transport.enter_raw_repl = Mock()
        mock_state_with_async_transport.transport.exec_raw_no_follow = Mock()
        mock_state_with_async_transport.transport.exit_raw_repl = Mock()
        
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("print('from file')\n")
            temp_file = f.name
        
        try:
            # Simulate ctrl-K (file injection) followed by exit
            mock_console_with_queue.input_queue = [b"\x0b", b"\x1d"]
            
            result = await do_repl_main_loop_async(
                mock_state_with_async_transport,
                mock_console_with_queue,
                escape_non_printable=False,
                file_to_inject=temp_file
            )
            
            # Verify async methods were called (not sync)
            mock_state_with_async_transport.transport.enter_raw_repl_async.assert_called_once()
            mock_state_with_async_transport.transport.exec_raw_no_follow_async.assert_called_once()
            mock_state_with_async_transport.transport.exit_raw_repl_async.assert_called_once()
            
            # Verify sync methods were NOT called
            mock_state_with_async_transport.transport.enter_raw_repl.assert_not_called()
            mock_state_with_async_transport.transport.exec_raw_no_follow.assert_not_called()
            mock_state_with_async_transport.transport.exit_raw_repl.assert_not_called()
            
            assert result is False
        finally:
            os.unlink(temp_file)
    
    event_loop.run_until_complete(_test())


def test_regular_input_fallback_to_sync_serial(mock_state_with_async_transport, mock_console_with_queue, event_loop, async_modules):
    """Test regular character input fallback to sync serial.write."""
    from mpremote.repl_async import do_repl_main_loop_async
    
    async def _test():
        # Remove write_async to trigger sync fallback
        delattr(mock_state_with_async_transport.transport, 'write_async')
        
        # Add sync serial interface
        mock_serial = Mock()
        mock_serial.write = Mock(return_value=1)
        mock_serial.inWaiting = Mock(return_value=0)
        mock_state_with_async_transport.transport.serial = mock_serial
        
        # Simulate regular input followed by exit
        mock_console_with_queue.input_queue = [b"x", b"y", b"z", b"\x1d"]
        
        result = await do_repl_main_loop_async(
            mock_state_with_async_transport,
            mock_console_with_queue,
            escape_non_printable=False
        )
        
        # Verify serial.write was called for regular characters
        calls = mock_serial.write.call_args_list
        assert any(call[0][0] == b"x" for call in calls)
        assert any(call[0][0] == b"y" for call in calls)
        assert any(call[0][0] == b"z" for call in calls)
        
        assert result is False
    
    event_loop.run_until_complete(_test())
