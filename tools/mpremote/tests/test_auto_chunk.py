#!/usr/bin/env python3
"""Test automatic chunk size detection based on device memory."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from mpremote.transport_serial_async import AsyncSerialTransport


async def test_auto_detection():
    device = "COM7"

    print(f"\nTesting automatic chunk size detection on {device}\n")

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

    import time

    start = time.perf_counter()
    await transport.fs_writefile_async("/test_auto.bin", test_data)  # chunk_size=None (auto)
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


if __name__ == "__main__":
    asyncio.run(test_auto_detection())
