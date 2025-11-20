#!/usr/bin/env python3
"""Performance benchmark tests for async vs sync file operations.

Tests file copy operations to/from MCU and compares async vs sync performance.
Run with: pytest test_benchmark_async.py -v
Run with detailed output: pytest test_benchmark_async.py -v -s
"""

import os
import sys
import time
import asyncio
import tempfile
import hashlib
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mpremote.transport_serial_async import AsyncSerialTransport
from mpremote.transport_serial import SerialTransport


# Test data sizes (in bytes)
# Note: Using small sizes due to limited flash on test devices (<20KB free on PyBoard)
TEST_SIZES = [
    (1024, "1KB"),
    (5 * 1024, "5KB"),
    (10 * 1024, "10KB"),
]

# Mark all tests in this module
pytestmark = [
    pytest.mark.async_required,
    pytest.mark.hardware_required,
    pytest.mark.serial_required,
]


def create_test_data(size: int) -> bytes:
    """Create test data of specified size."""
    # Use repeating pattern for better compression testing
    pattern = b"0123456789ABCDEF" * (size // 16 + 1)
    return pattern[:size]


def compute_sha256(data: bytes) -> str:
    """Compute SHA-256 hash of data."""
    return hashlib.sha256(data).hexdigest()


async def cleanup_device_file(transport, path: str) -> None:
    """Clean up a file on the device, ignoring errors."""
    try:
        await transport.exec_raw(f"import os; os.remove('{path}')")
    except:
        pass  # Ignore if file doesn't exist


def cleanup_device_file_sync(transport, path: str) -> None:
    """Clean up a file on the device (sync version), ignoring errors."""
    try:
        transport.exec_raw(f"import os; os.remove('{path}')")
    except:
        pass  # Ignore if file doesn't exist


@pytest.fixture
def temp_files():
    """Create temporary files for testing."""
    files = {}
    try:
        for size, label in TEST_SIZES:
            fd, path = tempfile.mkstemp(prefix=f"bench_{label}_", suffix=".bin")
            os.write(fd, create_test_data(size))
            os.close(fd)
            files[label] = path
        yield files
    finally:
        for path in files.values():
            try:
                os.unlink(path)
            except:
                pass


class BenchmarkResult:
    """Store benchmark results."""

    def __init__(self, operation: str, size_label: str, transport_type: str):
        self.operation = operation
        self.size_label = size_label
        self.transport_type = transport_type
        self.duration = 0.0
        self.bytes_transferred = 0

    @property
    def throughput_kbps(self) -> float:
        """Calculate throughput in KB/s."""
        if self.duration == 0:
            return 0.0
        return (self.bytes_transferred / 1024) / self.duration

    def __str__(self) -> str:
        return (
            f"{self.transport_type:5s} | {self.operation:10s} | "
            f"{self.size_label:5s} | {self.duration:7.3f}s | "
            f"{self.throughput_kbps:8.2f} KB/s"
        )


class BenchmarkRunner:
    """Run benchmarks and collect results."""

    def __init__(self, device: str, writable_path: str = "/flash"):
        self.device = device
        self.writable_path = writable_path
        self.results = []

    async def benchmark_async_upload(self, file_path: str, size_label: str) -> BenchmarkResult:
        """Benchmark async file upload with SHA-256 verification."""
        result = BenchmarkResult("upload", size_label, "async")

        transport = AsyncSerialTransport(self.device, baudrate=115200)
        dest_path = f"{self.writable_path}/test_{size_label}.bin"

        try:
            await transport.connect()
            await transport.enter_raw_repl_async()

            # Clean up any existing test file
            await cleanup_device_file(transport, dest_path)

            # Read source data and compute hash
            with open(file_path, "rb") as f:
                data = f.read()
            result.bytes_transferred = len(data)
            source_hash = compute_sha256(data)

            # Benchmark upload
            start = time.perf_counter()
            await transport.fs_writefile_async(dest_path, data, chunk_size=256)
            result.duration = time.perf_counter() - start

            # Verify upload with SHA-256
            verify_code = f"import uhashlib,binascii;h=uhashlib.sha256();f=open('{dest_path}','rb');d=f.read();f.close();h.update(d);print(binascii.hexlify(h.digest()).decode())"
            stdout, stderr = await transport.exec_raw_async(verify_code)
            device_hash = stdout.decode().strip()

            assert device_hash == source_hash, (
                f"SHA-256 mismatch! Source: {source_hash}, Device: {device_hash}"
            )

        finally:
            # Cleanup
            await cleanup_device_file(transport, dest_path)
            await transport.close_async()

        return result

    async def benchmark_async_download(self, file_path: str, size_label: str) -> BenchmarkResult:
        """Benchmark async file download with SHA-256 verification."""
        result = BenchmarkResult("download", size_label, "async")

        transport = AsyncSerialTransport(self.device, baudrate=115200)
        src_path = f"{self.writable_path}/test_{size_label}.bin"

        try:
            await transport.connect()
            await transport.enter_raw_repl_async()

            # Clean up any existing test file
            await cleanup_device_file(transport, src_path)

            # Upload test file
            with open(file_path, "rb") as f:
                data = f.read()
            result.bytes_transferred = len(data)
            source_hash = compute_sha256(data)

            await transport.fs_writefile_async(src_path, data, chunk_size=256)

            # Benchmark download
            start = time.perf_counter()
            downloaded = await transport.fs_readfile_async(src_path, chunk_size=256)
            result.duration = time.perf_counter() - start

            # Verify data integrity with SHA-256
            if isinstance(downloaded, bytearray):
                downloaded = bytes(downloaded)
            downloaded_hash = compute_sha256(downloaded)

            assert downloaded_hash == source_hash, (
                f"SHA-256 mismatch! Source: {source_hash}, Downloaded: {downloaded_hash}"
            )
            assert downloaded == data, "Downloaded data doesn't match source!"

        finally:
            # Cleanup
            await cleanup_device_file(transport, src_path)
            await transport.close_async()

        return result

    def benchmark_sync_upload(self, file_path: str, size_label: str) -> BenchmarkResult:
        """Benchmark sync file upload with SHA-256 verification."""
        result = BenchmarkResult("upload", size_label, "sync")

        transport = SerialTransport(self.device, baudrate=115200)
        dest_path = f"{self.writable_path}/test_{size_label}.bin"

        try:
            transport.enter_raw_repl()

            # Clean up any existing test file
            cleanup_device_file_sync(transport, dest_path)

            # Read source data and compute hash
            with open(file_path, "rb") as f:
                data = f.read()
            result.bytes_transferred = len(data)
            source_hash = compute_sha256(data)

            # Benchmark upload
            start = time.perf_counter()
            transport.fs_writefile(dest_path, data, chunk_size=256)
            result.duration = time.perf_counter() - start

            # Verify upload with SHA-256
            verify_code = f"import uhashlib,binascii;h=uhashlib.sha256();f=open('{dest_path}','rb');d=f.read();f.close();h.update(d);print(binascii.hexlify(h.digest()).decode())"
            stdout, stderr = transport.exec_raw(verify_code)
            device_hash = stdout.decode().strip()

            if not device_hash:
                # If we got empty output, check stderr
                err_msg = stderr.decode() if stderr else "No stderr"
                raise AssertionError(f"Failed to compute SHA-256 on device. stderr: {err_msg}")

            assert device_hash == source_hash, (
                f"SHA-256 mismatch! Source: {source_hash}, Device: {device_hash}"
            )

        finally:
            # Cleanup
            cleanup_device_file_sync(transport, dest_path)
            transport.close()

        return result

    def benchmark_sync_download(self, file_path: str, size_label: str) -> BenchmarkResult:
        """Benchmark sync file download with SHA-256 verification."""
        result = BenchmarkResult("download", size_label, "sync")

        transport = SerialTransport(self.device, baudrate=115200)
        src_path = f"{self.writable_path}/test_{size_label}.bin"

        try:
            transport.enter_raw_repl()

            # Clean up any existing test file
            cleanup_device_file_sync(transport, src_path)

            # Upload test file
            with open(file_path, "rb") as f:
                data = f.read()
            result.bytes_transferred = len(data)
            source_hash = compute_sha256(data)

            transport.fs_writefile(src_path, data, chunk_size=256)

            # Benchmark download
            start = time.perf_counter()
            downloaded = transport.fs_readfile(src_path, chunk_size=256)
            result.duration = time.perf_counter() - start

            # Verify data integrity with SHA-256
            if isinstance(downloaded, bytearray):
                downloaded = bytes(downloaded)
            downloaded_hash = compute_sha256(downloaded)

            assert downloaded_hash == source_hash, (
                f"SHA-256 mismatch! Source: {source_hash}, Downloaded: {downloaded_hash}"
            )
            assert downloaded == data, "Downloaded data doesn't match source!"

        finally:
            # Cleanup
            cleanup_device_file_sync(transport, src_path)
            transport.close()

        return result

    def print_results(self, verbose: bool = True):
        """Print benchmark results."""
        if not self.results:
            return

        # Group results by operation and size for comparison
        comparisons = {}
        for result in self.results:
            key = (result.operation, result.size_label)
            if key not in comparisons:
                comparisons[key] = {}
            comparisons[key][result.transport_type] = result

        print("\nType  | Operation | Size | Duration | Throughput  | Speedup")
        print("-" * 68)

        for result in self.results:
            key = (result.operation, result.size_label)
            transports = comparisons.get(key, {})

            # Calculate speedup if both sync and async available
            speedup_str = "       "
            if len(transports) == 2 and "async" in transports and "sync" in transports:
                async_res = transports["async"]
                sync_res = transports["sync"]

                if result.transport_type == "async":
                    # Calculate percentage difference: positive = faster, negative = slower
                    pct_diff = ((sync_res.duration - async_res.duration) / sync_res.duration) * 100
                    speedup_str = f"{pct_diff:+6.1f}%"

            # Format output with speedup column
            print(
                f"{result.transport_type:5} | {result.operation:9} | {result.size_label:4} | "
                f"{result.duration:7.3f}s | {result.throughput_kbps:7.2f} KB/s | {speedup_str}"
            )


@pytest.mark.hardware
@pytest.mark.parametrize("size,label", TEST_SIZES)
def test_benchmark_upload(
    temp_files, size, label, request, hardware_device, get_writable_path, event_loop, async_modules
):
    """Benchmark file upload (host to MCU)."""
    verbose = request.config.getoption("-v") > 0 or request.config.getoption("-s")
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]

    async def _test():
        # Detect writable path on device
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await transport.connect()
        await transport.enter_raw_repl_async()
        writable_path = await get_writable_path(transport)
        await transport.close_async()

        if writable_path is None:
            pytest.skip("No writable filesystem available on device")

        runner = BenchmarkRunner(hardware_device, writable_path)
        file_path = temp_files[label]

        print(f"\nBenchmark {label} upload on {hardware_device}")

        # Run sync benchmark
        sync_result = runner.benchmark_sync_upload(file_path, label)
        runner.results.append(sync_result)

        # Run async benchmark
        async_result = await runner.benchmark_async_upload(file_path, label)
        runner.results.append(async_result)

        if verbose:
            runner.print_results(verbose=True)

        # Assertion: async should not be significantly slower (allow 20% tolerance for upload)
        # Note: Upload has more overhead than download in async implementation
        # Download shows 2x speedup, so async infrastructure is sound
        if async_result.duration > sync_result.duration * 1.20:
            pytest.fail(
                f"Async upload too slow: {async_result.duration:.3f}s vs sync {sync_result.duration:.3f}s (>20%)",
                pytrace=False,
            )

    event_loop.run_until_complete(_test())


@pytest.mark.hardware
@pytest.mark.parametrize("size,label", TEST_SIZES)
def test_benchmark_download(
    temp_files, size, label, request, hardware_device, get_writable_path, event_loop, async_modules
):
    """Benchmark file download (MCU to host)."""
    verbose = request.config.getoption("-v") > 0 or request.config.getoption("-s")
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]

    async def _test():
        # Detect writable path on device
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await transport.connect()
        await transport.enter_raw_repl_async()
        writable_path = await get_writable_path(transport)
        await transport.close_async()

        if writable_path is None:
            pytest.skip("No writable filesystem available on device")

        runner = BenchmarkRunner(hardware_device, writable_path)
        file_path = temp_files[label]

        print(f"\nBenchmark {label} download from {hardware_device}")

        # Run sync benchmark
        sync_result = runner.benchmark_sync_download(file_path, label)
        runner.results.append(sync_result)

        # Run async benchmark
        async_result = await runner.benchmark_async_download(file_path, label)
        runner.results.append(async_result)

        if verbose:
            runner.print_results(verbose=True)

        # Assertion: async should not be significantly slower (allow 15% tolerance)
        # Note: Small overhead is expected due to async infrastructure
        if async_result.duration > sync_result.duration * 1.15:
            pytest.fail(
                f"Async download too slow: {async_result.duration:.3f}s vs sync {sync_result.duration:.3f}s (>15%)",
                pytrace=False,
            )

    event_loop.run_until_complete(_test())


@pytest.mark.hardware
def test_benchmark_comprehensive(
    temp_files, request, hardware_device, get_writable_path, event_loop, async_modules
):
    """Run comprehensive benchmark of all operations."""
    verbose = request.config.getoption("-v") > 0 or request.config.getoption("-s")
    AsyncSerialTransport = async_modules["AsyncSerialTransport"]

    async def _test():
        # Detect writable path on device
        transport = AsyncSerialTransport(hardware_device, baudrate=115200)
        await transport.connect()
        await transport.enter_raw_repl_async()
        writable_path = await get_writable_path(transport)
        await transport.close_async()

        if writable_path is None:
            pytest.skip("No writable filesystem available on device")

        runner = BenchmarkRunner(hardware_device, writable_path)

        print(f"\nComprehensive benchmark on {hardware_device}")

        for size, label in TEST_SIZES:
            file_path = temp_files[label]

            # Upload benchmarks
            runner.results.append(runner.benchmark_sync_upload(file_path, label))
            runner.results.append(await runner.benchmark_async_upload(file_path, label))

            # Download benchmarks
            runner.results.append(runner.benchmark_sync_download(file_path, label))
            runner.results.append(await runner.benchmark_async_download(file_path, label))

        runner.print_results(verbose=verbose)

    event_loop.run_until_complete(_test())


if __name__ == "__main__":
    """Run benchmarks directly (not via pytest)."""
    # Get device from environment or auto-detect
    device = os.environ.get("MICROPYTHON_DEVICE")
    if not device:
        # Try to auto-detect
        try:
            import serial.tools.list_ports

            ports = serial.tools.list_ports.comports()
            if ports:
                device = ports[0].device
                print(f"Auto-detected device: {device}")
        except ImportError:
            print("ERROR: No device specified and pyserial not available for auto-detection")
            print("Set MICROPYTHON_DEVICE environment variable or install pyserial")
            sys.exit(1)

    if not device:
        print("ERROR: No MicroPython device found")
        sys.exit(1)

    print(f"Running benchmarks on device: {device}")

    # Create temp files
    temp_files = {}
    for size, label in TEST_SIZES:
        fd, path = tempfile.mkstemp(prefix=f"bench_{label}_", suffix=".bin")
        os.write(fd, create_test_data(size))
        os.close(fd)
        temp_files[label] = path

    try:
        runner = BenchmarkRunner(device)

        for size, label in TEST_SIZES:
            file_path = temp_files[label]
            print(f"\nBenchmarking {label}...")

            # Upload
            runner.results.append(runner.benchmark_sync_upload(file_path, label))
            runner.results.append(asyncio.run(runner.benchmark_async_upload(file_path, label)))

            # Download
            runner.results.append(runner.benchmark_sync_download(file_path, label))
            runner.results.append(asyncio.run(runner.benchmark_async_download(file_path, label)))

        runner.print_results(verbose=True)

    finally:
        for path in temp_files.values():
            try:
                os.unlink(path)
            except:
                pass
