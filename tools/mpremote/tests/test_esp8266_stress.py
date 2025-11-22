#!/usr/bin/env python3
"""Stress test auto-detection with heavy memory fragmentation."""

import asyncio
import os
import sys

import pytest
from mpremote.transport_serial_async import AsyncSerialTransport

pytestmark = [pytest.mark.hardware_required, pytest.mark.serial_required]


async def _run_heavy_fragmentation(device: str):
    print(f"\nStress test: Heavy memory fragmentation on ESP8266 ({device})\n")

    transport = AsyncSerialTransport(device, baudrate=115200)
    await transport.connect()
    await transport.enter_raw_repl_async()

    try:
        # Check initial memory
        free_before = await transport.eval_async("__import__('gc').mem_free()", parse=False)
        free_before_kb = int(free_before.decode().strip()) / 1024
        print(f"Initial free memory: {free_before_kb:.1f} KB")

        # Heavy fragmentation - allocate many small buffers
        print("\nCreating heavy memory fragmentation...")
        await transport.exec_async(
            """
import gc
_bufs = []
# Allocate many small buffers to create fragmentation
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

            # Force re-detection by clearing cache
            transport._optimal_chunk_size = None
            transport._free_memory_kb = None

            optimal_chunk = await transport.detect_optimal_chunk_size_async()
            print(f"  Selected chunk size: {optimal_chunk} bytes")

            # Verify it's appropriate for available memory
            if free_kb < 20:
                assert optimal_chunk == 256, (
                    f"Should use 256 bytes for <20KB free, got {optimal_chunk}"
                )
                print("  ✓ Correctly using minimal chunk (256) for very low memory")
            elif free_kb < 50:
                assert optimal_chunk == 512, (
                    f"Should use 512 bytes for 20-50KB free, got {optimal_chunk}"
                )
                print("  ✓ Correctly using small chunk (512) for low memory")
            else:
                print(f"  ✓ Using {optimal_chunk} bytes for {free_kb:.1f} KB free")

        # Test actual upload with minimal memory
        print("\nTesting upload with constrained memory...")
        test_data = b"X" * 2048  # 2KB

        import time

        start = time.perf_counter()
        try:
            await transport.fs_writefile_async("/test_stress.bin", test_data)
            duration = time.perf_counter() - start
            print(f"  ✓ Upload successful: {len(test_data)} bytes in {duration:.3f}s")

            # Verify file
            verify = await transport.eval_async("len(open('/test_stress.bin','rb').read())")
            assert verify == len(test_data), f"File size mismatch: {verify} != {len(test_data)}"
            print(f"  ✓ File verified: {verify} bytes")

        except Exception as exc:
            print(f"  ✗ Upload failed: {exc}")

        # Cleanup on device
        try:
            await transport.exec_raw_async('import os; os.remove("/test_stress.bin")')
        except Exception:
            pass

        print("\n✓ Stress test complete!")
    finally:
        await transport.close_async()


def test_heavy_fragmentation(event_loop, hardware_device, require_dut):
    require_dut(platform="esp8266")
    event_loop.run_until_complete(_run_heavy_fragmentation(hardware_device))


