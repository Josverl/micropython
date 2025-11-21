#!/usr/bin/env python3
"""Comprehensive tests for async file upload optimizations.

Tests:
1. Small file optimization (<3KB single-shot writes)
2. Large file chunked writes with auto-detection
3. Chunk size selection based on device memory
4. Caching behavior
5. Boundary cases

Run unit tests: python test_upload_optimization.py
Run with hardware: pytest test_upload_optimization.py::test_auto_detection_with_device -v
"""

import asyncio
import sys
import time
from pathlib import Path
from unittest.mock import AsyncMock
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from mpremote.transport_serial_async import AsyncSerialTransport
from mpremote.transport_async import MIN_FILE_SIZE_FOR_AUTO_DETECTION


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def test_constant_value():
    """Verify MIN_FILE_SIZE_FOR_AUTO_DETECTION constant."""
    assert MIN_FILE_SIZE_FOR_AUTO_DETECTION == 3 * 1024
    print(f"✓ MIN_FILE_SIZE_FOR_AUTO_DETECTION = {MIN_FILE_SIZE_FOR_AUTO_DETECTION} bytes (3KB)")


def test_small_file_single_shot():
    """Test that files <3KB use single-shot write (unit test with mocks)."""
    async def _test():
        transport = AsyncSerialTransport("COM7", baudrate=115200)
        transport.exec_async = AsyncMock()
        transport.detect_optimal_chunk_size_async = AsyncMock(return_value=2048)
        
        # Test small file (2KB)
        small_data = b"x" * 2048
        await transport.fs_writefile_async("/test.bin", small_data)
        
        # Verify single exec_async call (no detection)
        assert transport.exec_async.call_count == 1
        assert not transport.detect_optimal_chunk_size_async.called
        
        # Verify it's the combined write command
        call_str = str(transport.exec_async.call_args_list[0])
        assert "open(" in call_str and ".write(" in call_str and ".close()" in call_str
        
        print(f"✓ Small file ({len(small_data)} bytes): Single-shot write")
    
    asyncio.run(_test())


def test_large_file_chunked():
    """Test that files ≥3KB use chunked writes with auto-detection (unit test with mocks)."""
    async def _test():
        transport = AsyncSerialTransport("COM7", baudrate=115200)
        transport.exec_async = AsyncMock()
        transport.detect_optimal_chunk_size_async = AsyncMock(return_value=2048)
        
        # Test large file (4KB)
        large_data = b"x" * 4096
        await transport.fs_writefile_async("/test.bin", large_data)
        
        # Verify detection was called
        transport.detect_optimal_chunk_size_async.assert_called_once()
        
        # Verify chunked approach (open + 2 writes + close = 4 calls)
        assert transport.exec_async.call_count == 4
        
        print(f"✓ Large file ({len(large_data)} bytes): Chunked write with auto-detection")
    
    asyncio.run(_test())


def test_boundary_cases():
    """Test files at the 3KB threshold boundary (unit test with mocks)."""
    async def _test():
        # Just below threshold - should use single-shot
        transport = AsyncSerialTransport("COM7", baudrate=115200)
        transport.exec_async = AsyncMock()
        transport.detect_optimal_chunk_size_async = AsyncMock(return_value=2048)
        
        data_below = b"x" * (MIN_FILE_SIZE_FOR_AUTO_DETECTION - 1)
        await transport.fs_writefile_async("/test.bin", data_below)
        
        assert not transport.detect_optimal_chunk_size_async.called
        assert transport.exec_async.call_count == 1
        print(f"✓ {len(data_below)} bytes (threshold-1): Single-shot write")
        
        # Exactly at threshold - should use chunked
        transport = AsyncSerialTransport("COM7", baudrate=115200)
        transport.exec_async = AsyncMock()
        transport.detect_optimal_chunk_size_async = AsyncMock(return_value=2048)
        
        data_at = b"x" * MIN_FILE_SIZE_FOR_AUTO_DETECTION
        await transport.fs_writefile_async("/test.bin", data_at)
        
        assert transport.detect_optimal_chunk_size_async.called
        assert transport.exec_async.call_count > 1
        print(f"✓ {len(data_at)} bytes (threshold): Chunked write with detection")
    
    asyncio.run(_test())


@pytest.mark.hardware
def test_auto_detection_with_device(event_loop, hardware_device):
    """Test automatic chunk size detection on real hardware."""
    async def _test():
        device = hardware_device
        print(f"\nTesting auto-detection on {device}\n")

        transport = AsyncSerialTransport(device, baudrate=115200)
        await transport.connect()
        await transport.enter_raw_repl_async()

        # Test auto-detection
        print("Detecting optimal chunk size...")
        optimal_chunk = await transport.detect_optimal_chunk_size_async()

        if transport._free_memory_kb:
            print(f"  Device free memory: {transport._free_memory_kb:.1f} KB")
        else:
            print(f"  Device free memory: Unable to detect")

        print(f"  Selected chunk size: {optimal_chunk} bytes")

        # Verify it's cached
        optimal_chunk2 = await transport.detect_optimal_chunk_size_async()
        assert optimal_chunk == optimal_chunk2, "Chunk size should be cached!"
        print(f"  ✓ Chunk size cached (no second query needed)")

        # Test file upload with auto chunk size
        print("\nTesting file upload with auto-detected chunk size...")
        test_data = b"0123456789ABCDEF" * 640  # 10KB

        start = time.perf_counter()
        await transport.fs_writefile_async("/test_auto.bin", test_data)
        duration = time.perf_counter() - start

        print(
            f"  Upload: {len(test_data)} bytes in {duration:.3f}s ({len(test_data) / 1024 / duration:.2f} KB/s)"
        )

        # Cleanup
        try:
            await transport.exec_raw_async('import os; os.remove("/test_auto.bin")')
        except:
            pass

        await transport.close_async()
        print("\n✓ Auto-detection test complete!")

    event_loop.run_until_complete(_test())


if __name__ == "__main__":
    print("Running async upload optimization tests...\n")
    print("=" * 60)
    
    # Run unit tests (no hardware required)
    print("\n1. Unit Tests (mocked, no hardware):\n")
    test_constant_value()
    test_small_file_single_shot()
    test_large_file_chunked()
    test_boundary_cases()
    
    print("\n" + "=" * 60)
    print("\n✓ All unit tests passed!")
    print("\nFor hardware tests, run:")
    print("  pytest test_upload_optimization.py::test_auto_detection_with_device -v")
