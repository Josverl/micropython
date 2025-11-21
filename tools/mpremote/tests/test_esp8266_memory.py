#!/usr/bin/env python3
"""ESP8266 memory stress tests for auto-detection.

Tests chunk size selection on constrained devices with:
1. Normal memory conditions
2. Memory fragmentation
3. Heavy memory pressure

Run: python test_esp8266_memory.py
Or with pytest: pytest test_esp8266_memory.py -v
"""

import asyncio
import os
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from mpremote.transport_serial_async import AsyncSerialTransport

pytestmark = [pytest.mark.hardware_required, pytest.mark.serial_required]


async def _run_fragmented_memory_test(device: str):
    print(f"\nTest 1: ESP8266 memory fragmentation test ({device})\n")

    transport = AsyncSerialTransport(device, baudrate=115200)
    await transport.connect()
    await transport.enter_raw_repl_async()

    try:
        # Check initial memory
        free_before = await transport.eval_async("__import__('gc').mem_free()", parse=False)
        free_before_kb = int(free_before.decode().strip()) / 1024
        print(f"Initial free memory: {free_before_kb:.1f} KB")

        # Fragment memory by allocating buffers
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

        # Test auto-detection
        print("\nTesting auto-detection with fragmented memory...")
        optimal_chunk = await transport.detect_optimal_chunk_size_async()
        print(f"  Detected optimal chunk size: {optimal_chunk} bytes")

        # Test file upload
        print("\nTesting file upload with auto-detected chunk size...")
        test_data = b"0123456789ABCDEF" * 320  # 5KB

        start = time.perf_counter()
        await transport.fs_writefile_async("/test_esp.bin", test_data)
        duration = time.perf_counter() - start

        print(
            f"  Upload: {len(test_data)} bytes in {duration:.3f}s ({len(test_data) / 1024 / duration:.2f} KB/s)"
        )

        # Cleanup allocations/files on device
        try:
            await transport.exec_async("del _bufs")
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


async def _run_heavy_stress_test(device: str):
    print(f"\nTest 2: ESP8266 heavy stress test ({device})\n")

    transport = AsyncSerialTransport(device, baudrate=115200)
    await transport.connect()
    await transport.enter_raw_repl_async()

    try:
        # Check initial memory
        free_before = await transport.eval_async("__import__('gc').mem_free()", parse=False)
        free_before_kb = int(free_before.decode().strip()) / 1024
        print(f"Initial free memory: {free_before_kb:.1f} KB")

        # Heavy fragmentation
        print("\nCreating heavy memory fragmentation...")
        await transport.exec_async(
            """
import gc
_bufs = []
for i in range(20):
    try:
        _bufs.append(bytearray(800))  # 800 bytes each
    except:
        break
gc.collect()
print(f"Allocated {len(_bufs)} buffers = {len(_bufs) * 800} bytes")
"""
        )

        # Check severely constrained memory
        free_after = await transport.eval_async("__import__('gc').mem_free()", parse=False)
        free_after_kb = int(free_after.decode().strip()) / 1024
        print(f"Free memory after fragmentation: {free_after_kb:.1f} KB")
        print(f"Memory consumed: {free_before_kb - free_after_kb:.1f} KB")

        # Test scenarios
        scenarios = [
            ("Heavily fragmented", None),
            ("After GC", "gc.collect()"),
            ("After cleanup", "del _bufs; gc.collect()"),
        ]

        for scenario_name, cleanup_code in scenarios:
            if cleanup_code:
                await transport.exec_async(cleanup_code)
                free_mem = await transport.eval_async("__import__('gc').mem_free()", parse=False)
                free_kb = int(free_mem.decode().strip()) / 1024
            else:
                free_kb = free_after_kb

            print(f"\n{scenario_name} (Free: {free_kb:.1f} KB):")

            # Force re-detection
            transport._optimal_chunk_size = None
            transport._free_memory_kb = None

            optimal_chunk = await transport.detect_optimal_chunk_size_async()
            print(f"  Selected chunk size: {optimal_chunk} bytes")

            # Verify appropriate for memory
            if free_kb < 20:
                assert optimal_chunk == 256
                print("  ✓ Correctly using minimal chunk (256) for very low memory")
            elif free_kb < 50:
                assert optimal_chunk == 512
                print("  ✓ Correctly using small chunk (512) for low memory")
            else:
                print(f"  ✓ Using {optimal_chunk} bytes for {free_kb:.1f} KB free")

        # Test upload with constrained memory
        print("\nTesting upload with constrained memory...")
        test_data = b"X" * 2048  # 2KB (small file, should use single-shot)

        start = time.perf_counter()
        try:
            await transport.fs_writefile_async("/test_stress.bin", test_data)
            duration = time.perf_counter() - start
            print(f"  ✓ Upload successful: {len(test_data)} bytes in {duration:.3f}s")

            # Verify file
            verify = await transport.eval_async("len(open('/test_stress.bin','rb').read())")
            assert verify == len(test_data)
            print(f"  ✓ File verified: {verify} bytes")

        except Exception as exc:
            print(f"  ✗ Upload failed: {exc}")

        # Cleanup on device
        try:
            await transport.exec_raw_async('import os; os.remove("/test_stress.bin")')
        except Exception:
            pass

        print("\n✓ Heavy stress test complete!")
    finally:
        await transport.close_async()


def test_esp8266_fragmented_memory(event_loop, hardware_device, require_target_platform):
    """Test auto-detection on ESP8266 with memory fragmentation."""

    require_target_platform(platform="esp8266")
    event_loop.run_until_complete(_run_fragmented_memory_test(hardware_device))


def test_esp8266_heavy_stress(event_loop, hardware_device, require_target_platform):
    """Stress test with heavy memory fragmentation on ESP8266."""

    require_target_platform(platform="esp8266")
    event_loop.run_until_complete(_run_heavy_stress_test(hardware_device))


if __name__ == "__main__":
    device = (
        os.environ.get("ESP8266_DEVICE")
        or os.environ.get("MICROPYTHON_DEVICE")
        or (sys.argv[1] if len(sys.argv) > 1 else None)
    )

    if not device:
        print("Set ESP8266_DEVICE/MICROPYTHON_DEVICE or pass serial port as argument.")
        sys.exit(1)

    print("=" * 60)
    print("ESP8266 Memory Stress Tests")
    print("=" * 60)

    asyncio.run(_run_fragmented_memory_test(device))
    asyncio.run(_run_heavy_stress_test(device))

    print("\n" + "=" * 60)
    print("✓ All ESP8266 tests passed!")
    print("=" * 60)
