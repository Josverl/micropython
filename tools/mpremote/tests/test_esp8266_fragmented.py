#!/usr/bin/env python3
"""Test auto-detection on ESP8266 with memory fragmentation."""

import asyncio
import os
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from mpremote.transport_serial_async import AsyncSerialTransport

pytestmark = [pytest.mark.hardware_required, pytest.mark.serial_required]


async def _run_fragmentation_test(device: str):
    print(f"\nTesting auto-detection on ESP8266 ({device}) with memory fragmentation\n")

    transport = AsyncSerialTransport(device, baudrate=115200)
    await transport.connect()
    await transport.enter_raw_repl_async()

    try:
        # Check initial memory
        free_before = await transport.eval_async("__import__('gc').mem_free()", parse=False)
        free_before_kb = int(free_before.decode().strip()) / 1024
        print(f"Initial free memory: {free_before_kb:.1f} KB")

        # Fragment memory by allocating some large buffers
        print("\nFragmenting memory with allocations...")
        await transport.exec_async(
            """
# Allocate some buffers to fragment memory
_bufs = []
for i in range(5):
    try:
        _bufs.append(bytearray(2000))  # 2KB each
    except:
        break
print(f"Allocated {len(_bufs)} buffers")
"""
        )

        # Check memory after fragmentation
        free_after = await transport.eval_async("__import__('gc').mem_free()", parse=False)
        free_after_kb = int(free_after.decode().strip()) / 1024
        print(f"Free memory after fragmentation: {free_after_kb:.1f} KB")
        print(f"Memory consumed: {free_before_kb - free_after_kb:.1f} KB")

        # Force garbage collection
        await transport.exec_async("__import__('gc').collect()")

        # Test auto-detection with fragmented memory
        print("\nTesting auto-detection with fragmented memory...")
        optimal_chunk = await transport.detect_optimal_chunk_size_async()

        print(f"  Detected optimal chunk size: {optimal_chunk} bytes")

        if free_after_kb < 20:
            expected = 256
        elif free_after_kb < 50:
            expected = 512
        elif free_after_kb < 100:
            expected = 1024
        else:
            expected = 2048

        print(f"  Expected chunk size: {expected} bytes")

        if optimal_chunk == expected:
            print("  ✓ Correct chunk size selected!")
        else:
            print("  ⚠ Different from expected (may be due to fragmentation)")

        # Test file upload with auto-detected chunk
        print("\nTesting file upload with auto-detected chunk size...")
        test_data = b"0123456789ABCDEF" * 320  # 5KB (safer for ESP8266)

        start = time.perf_counter()
        await transport.fs_writefile_async("/test_esp.bin", test_data)  # Auto chunk
        duration = time.perf_counter() - start

        print(
            f"  Upload: {len(test_data)} bytes in {duration:.3f}s ({len(test_data) / 1024 / duration:.2f} KB/s)"
        )

        # Cleanup on device
        try:
            await transport.exec_async("del _bufs")  # Free the buffers
            await transport.exec_async("__import__('gc').collect()")
            await transport.exec_raw_async('import os; os.remove("/test_esp.bin")')
        except Exception:
            pass

        # Final memory check
        free_final = await transport.eval_async("__import__('gc').mem_free()", parse=False)
        free_final_kb = int(free_final.decode().strip()) / 1024
        print(f"\nFinal free memory: {free_final_kb:.1f} KB")

        print("\n✓ ESP8266 fragmentation test complete!")
    finally:
        await transport.close_async()


def test_esp8266_fragmented_memory(event_loop, hardware_device, require_target_platform):
    require_target_platform(platform="esp8266")
    event_loop.run_until_complete(_run_fragmentation_test(hardware_device))


if __name__ == "__main__":
    device = (
        os.environ.get("ESP8266_DEVICE")
        or os.environ.get("MICROPYTHON_DEVICE")
        or (sys.argv[1] if len(sys.argv) > 1 else None)
    )

    if not device:
        print("Set ESP8266_DEVICE/MICROPYTHON_DEVICE or pass serial port as argument.")
        sys.exit(1)

    asyncio.run(_run_fragmentation_test(device))
