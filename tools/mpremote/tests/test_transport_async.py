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

"""Pytest-based tests for AsyncTransport base class and filesystem operations.

These tests provide comprehensive coverage of the transport_async module,
focusing on filesystem operations (fs_listdir_async, fs_stat_async, 
fs_readfile_async, fs_writefile_async) and abstract method verification.
"""

import asyncio
import pytest

pytestmark = [pytest.mark.async_required, pytest.mark.hardware_required, pytest.mark.serial_required]


# Tests for NotImplementedError on abstract methods


def test_async_transport_read_async_not_implemented(async_modules, event_loop):
    """Test that read_async raises NotImplementedError."""
    from mpremote.transport_async import AsyncTransport
    
    async def _test():
        transport = AsyncTransport()
        with pytest.raises(NotImplementedError):
            await transport.read_async(256)
    
    event_loop.run_until_complete(_test())


def test_async_transport_write_async_not_implemented(async_modules, event_loop):
    """Test that write_async raises NotImplementedError."""
    from mpremote.transport_async import AsyncTransport
    
    async def _test():
        transport = AsyncTransport()
        with pytest.raises(NotImplementedError):
            await transport.write_async(b"test")
    
    event_loop.run_until_complete(_test())


def test_async_transport_read_until_async_not_implemented(async_modules, event_loop):
    """Test that read_until_async raises NotImplementedError."""
    from mpremote.transport_async import AsyncTransport
    
    async def _test():
        transport = AsyncTransport()
        with pytest.raises(NotImplementedError):
            await transport.read_until_async(1, b"\r\n", timeout=1.0)
    
    event_loop.run_until_complete(_test())


def test_async_transport_enter_raw_repl_async_not_implemented(async_modules, event_loop):
    """Test that enter_raw_repl_async raises NotImplementedError."""
    from mpremote.transport_async import AsyncTransport
    
    async def _test():
        transport = AsyncTransport()
        with pytest.raises(NotImplementedError):
            await transport.enter_raw_repl_async()
    
    event_loop.run_until_complete(_test())


def test_async_transport_exit_raw_repl_async_not_implemented(async_modules, event_loop):
    """Test that exit_raw_repl_async raises NotImplementedError."""
    from mpremote.transport_async import AsyncTransport
    
    async def _test():
        transport = AsyncTransport()
        with pytest.raises(NotImplementedError):
            await transport.exit_raw_repl_async()
    
    event_loop.run_until_complete(_test())


def test_async_transport_exec_raw_no_follow_async_not_implemented(async_modules, event_loop):
    """Test that exec_raw_no_follow_async raises NotImplementedError."""
    from mpremote.transport_async import AsyncTransport
    
    async def _test():
        transport = AsyncTransport()
        with pytest.raises(NotImplementedError):
            await transport.exec_raw_no_follow_async("print(1)")
    
    event_loop.run_until_complete(_test())


def test_async_transport_follow_async_not_implemented(async_modules, event_loop):
    """Test that follow_async raises NotImplementedError."""
    from mpremote.transport_async import AsyncTransport
    
    async def _test():
        transport = AsyncTransport()
        with pytest.raises(NotImplementedError):
            await transport.follow_async(timeout=1.0)
    
    event_loop.run_until_complete(_test())


def test_async_transport_exec_raw_async_not_implemented(async_modules, event_loop):
    """Test that exec_raw_async raises NotImplementedError."""
    from mpremote.transport_async import AsyncTransport
    
    async def _test():
        transport = AsyncTransport()
        with pytest.raises(NotImplementedError):
            await transport.exec_raw_async("print(1)")
    
    event_loop.run_until_complete(_test())


def test_async_transport_exec_async_not_implemented(async_modules, event_loop):
    """Test that exec_async raises NotImplementedError."""
    from mpremote.transport_async import AsyncTransport
    
    async def _test():
        transport = AsyncTransport()
        with pytest.raises(NotImplementedError):
            await transport.exec_async("print(1)")
    
    event_loop.run_until_complete(_test())


def test_async_transport_eval_async_not_implemented(async_modules, event_loop):
    """Test that eval_async raises NotImplementedError."""
    from mpremote.transport_async import AsyncTransport
    
    async def _test():
        transport = AsyncTransport()
        with pytest.raises(NotImplementedError):
            await transport.eval_async("1+1")
    
    event_loop.run_until_complete(_test())


def test_async_transport_close_async_not_implemented(async_modules, event_loop):
    """Test that close_async raises NotImplementedError."""
    from mpremote.transport_async import AsyncTransport
    
    async def _test():
        transport = AsyncTransport()
        with pytest.raises(NotImplementedError):
            await transport.close_async()
    
    event_loop.run_until_complete(_test())


# Tests for filesystem operations


def test_fs_listdir_async_root(hardware_device, async_modules, event_loop):
    """Test fs_listdir_async on root directory."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)
        
        # Test fs_listdir_async
        entries = await transport.fs_listdir_async("")
        
        assert isinstance(entries, list)
        assert len(entries) > 0
        
        # Verify entry structure - entries have st_mode not type
        for entry in entries:
            assert hasattr(entry, 'name')
            assert hasattr(entry, 'st_mode')
            assert isinstance(entry.name, str)
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_fs_listdir_async_error_handling(hardware_device, async_modules, event_loop):
    """Test fs_listdir_async error handling for nonexistent directory."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)
        
        # Test error handling - fs operations raise OSError not TransportError
        with pytest.raises(OSError):
            await transport.fs_listdir_async("/nonexistent_xyz123")
        
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_fs_stat_async(hardware_device, async_modules, event_loop, get_writable_path):
    """Test fs_stat_async gets file statistics."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)
        
        # Find writable path
        writable_path = await get_writable_path(transport)
        if writable_path is None:
            pytest.skip("No writable filesystem available on device")
            return
        
        # Create test file (must close to flush)
        await transport.exec_async(f"f=open('{writable_path}/tmp_stat.txt','w'); f.write('test content'); f.close()")
        
        # Test fs_stat_async
        stats = await transport.fs_stat_async(f"{writable_path}/tmp_stat.txt")
        
        assert isinstance(stats, tuple)
        assert len(stats) >= 6
        # Check size
        assert stats[6] == 12  # "test content" is 12 bytes
        
        # Cleanup
        await transport.exec_async(f"import os; os.remove('{writable_path}/tmp_stat.txt')")
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_fs_readfile_async(hardware_device, async_modules, event_loop, get_writable_path):
    """Test fs_readfile_async reads file content."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)
        
        # Find writable path
        writable_path = await get_writable_path(transport)
        if writable_path is None:
            pytest.skip("No writable filesystem available on device")
            return
        
        # Create test file (must close to flush)
        test_content = "Hello async file!"
        await transport.exec_async(f"f=open('{writable_path}/tmp_read.txt','w'); f.write({test_content!r}); f.close()")
        
        # Test fs_readfile_async
        content = await transport.fs_readfile_async(f"{writable_path}/tmp_read.txt")
        
        assert isinstance(content, bytes)
        assert content.decode() == test_content
        
        # Cleanup
        await transport.exec_async(f"import os; os.remove('{writable_path}/tmp_read.txt')")
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_fs_writefile_async(hardware_device, async_modules, event_loop, get_writable_path):
    """Test fs_writefile_async writes file content."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)
        
        # Find writable path
        writable_path = await get_writable_path(transport)
        if writable_path is None:
            pytest.skip("No writable filesystem available on device")
            return
        
        # Test fs_writefile_async
        test_content = b"Async write test!"
        await transport.fs_writefile_async(f"{writable_path}/tmp_write.txt", test_content)
        
        # Verify file was written (use repr to get proper bytes representation)
        result = await transport.exec_async(f"print(repr(open('{writable_path}/tmp_write.txt', 'rb').read()))")
        import ast
        parsed_result = ast.literal_eval(result.decode().strip())
        assert parsed_result == test_content
        
        # Cleanup
        await transport.exec_async(f"import os; os.remove('{writable_path}/tmp_write.txt')")
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_fs_listdir_with_files(hardware_device, async_modules, event_loop, get_writable_path):
    """Test fs_listdir_async lists files in directory."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)
        
        # Find writable path
        writable_path = await get_writable_path(transport)
        if writable_path is None:
            pytest.skip("No writable filesystem available on device")
            return
        
        # Setup: create test directory with files (close to flush)
        await transport.exec_async(f"""
import os
try:
    os.mkdir('{writable_path}/tmp_ls_test')
except:
    pass
f=open('{writable_path}/tmp_ls_test/file1.txt','w'); f.write('a'); f.close()
f=open('{writable_path}/tmp_ls_test/file2.txt','w'); f.write('b'); f.close()
""")
        
        # Test: list directory
        entries = await transport.fs_listdir_async(f"{writable_path}/tmp_ls_test")
        names = [e.name for e in entries]
        
        assert 'file1.txt' in names
        assert 'file2.txt' in names
        
        # Cleanup
        await transport.exec_async(f"""
import os
os.remove('{writable_path}/tmp_ls_test/file1.txt')
os.remove('{writable_path}/tmp_ls_test/file2.txt')
os.rmdir('{writable_path}/tmp_ls_test')
""")
        await transport.close_async()
    
    event_loop.run_until_complete(_test())


def test_fs_operations_workflow(hardware_device, async_modules, event_loop, get_writable_path):
    """Test complete filesystem workflow: write, stat, read, listdir."""
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]
    
    async def _test():
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await asyncio.wait_for(transport.connect(), timeout=5.0)
        await transport.enter_raw_repl_async(soft_reset=True)
        
        # Find writable path
        writable_path = await get_writable_path(transport)
        if writable_path is None:
            pytest.skip("No writable filesystem available on device")
            return
        
        # Create directory
        await transport.exec_async(f"import os; os.mkdir('{writable_path}/tmp_wf') if 'tmp_wf' not in os.listdir('{writable_path}') else None")
        
        # Write file
        content = b"workflow test data"
        await transport.fs_writefile_async(f"{writable_path}/tmp_wf/data.txt", content)
        
        # Stat file
        stats = await transport.fs_stat_async(f"{writable_path}/tmp_wf/data.txt")
        assert stats[6] == len(content)
        
        # Read file
        read_content = await transport.fs_readfile_async(f"{writable_path}/tmp_wf/data.txt")
        assert read_content == content
        
        # List directory
        entries = await transport.fs_listdir_async(f"{writable_path}/tmp_wf")
        names = [e.name for e in entries]
        assert 'data.txt' in names
        
        # Cleanup
        await transport.exec_async(f"import os; os.remove('{writable_path}/tmp_wf/data.txt'); os.rmdir('{writable_path}/tmp_wf')")
        await transport.close_async()
    
    event_loop.run_until_complete(_test())
