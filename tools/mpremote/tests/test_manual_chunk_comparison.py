#!/usr/bin/env python3
"""Manual test to compare performance of different chunk sizes.

This test manually specifies chunk sizes (256, 512, 1024, 2048) to measure
their relative performance. Used for benchmarking and validation.

Run standalone: python test_manual_chunk_comparison.py
"""

import asyncio
import os
import sys
import tempfile
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from mpremote.transport_serial_async import AsyncSerialTransport

pytestmark = [pytest.mark.hardware_required, pytest.mark.serial_required]


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def test_chunk_sizes(event_loop, hardware_device):
    async def _test():
        device = hardware_device

        # Create test data
        data = b"0123456789ABCDEF" * 640  # 10KB

        # Detect writable path
        transport = AsyncSerialTransport(device, baudrate=115200)
        await transport.connect()
        await transport.enter_raw_repl_async()

        # Try different common paths
        for test_path in ["/", "/flash", ""]:
            try:
                await transport.exec_raw_async(f"f=open('{test_path}/test_chunk.tmp','wb'); f.close()")
                await transport.exec_raw_async(f"import os; os.remove('{test_path}/test_chunk.tmp')")
                writable_path = test_path
                break
            except:
                continue
        else:
            writable_path = ""

        await transport.close_async()
        print(
            f"\nTesting 10KB upload with different chunk sizes on {device} (path: {writable_path or 'root'})\n"
        )
        print("Chunk Size | Duration | Throughput | Improvement")
        print("-" * 60)

        baseline_duration = None

        for chunk_size in [256, 512, 1024, 2048]:
            transport = AsyncSerialTransport(device, baudrate=115200)
            await transport.connect()
            await transport.enter_raw_repl_async()

            # Upload test
            dest_file = f"{writable_path}/test.bin" if writable_path else "test.bin"
            start = time.perf_counter()
            await transport.fs_writefile_async(dest_file, data, chunk_size=chunk_size)
            duration = time.perf_counter() - start
            throughput = len(data) / 1024 / duration

            if baseline_duration is None:
                baseline_duration = duration
                improvement = ""
            else:
                pct = ((baseline_duration - duration) / baseline_duration) * 100
                improvement = f"{pct:+6.1f}%"

            print(
                f"     {chunk_size:4d}  |  {duration:.3f}s  | {throughput:7.2f} KB/s | {improvement}"
            )

            # Cleanup
            try:
                await transport.exec_raw_async(f'import os; os.remove("{dest_file}")')
            except:
                pass
            await transport.close_async()
            await asyncio.sleep(0.5)  # Brief pause between tests

    event_loop.run_until_complete(_test())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # Import manually to avoid pytest requirement
        class MockEventLoop:
            def run_until_complete(self, coro):
                return asyncio.run(coro)
        test_chunk_sizes(MockEventLoop())
    finally:
        loop.close()
