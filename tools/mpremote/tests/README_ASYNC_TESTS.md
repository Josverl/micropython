# Async Upload Optimization Tests

This directory contains tests for validating async file upload optimizations.

## Test Files

### Core Tests

**`test_upload_optimization.py`** - Comprehensive optimization tests
- Small file optimization (<3KB single-shot writes)
- Large file chunked writes with auto-detection
- Boundary cases at 3KB threshold
- Memory detection and caching
- Run: `python test_upload_optimization.py` (unit tests, no hardware)
- Run: `pytest test_upload_optimization.py -v` (includes hardware tests)

**`test_benchmark_async.py`** - Performance benchmarks
- Compare async vs sync performance
- Tests multiple file sizes (1KB, 2KB, 3KB, 5KB, 10KB)
- Upload and download benchmarks
- SHA-256 verification
- Run: `pytest test_benchmark_async.py -v -s`

### Specialized Tests

**`test_manual_chunk_comparison.py`** - Manual chunk size comparison
- Manually test different chunk sizes (256, 512, 1024, 2048 bytes)
- Measure performance impact of each size
- Useful for benchmarking and validation
- Run: `python test_manual_chunk_comparison.py`

**`test_esp8266_memory.py`** - ESP8266 memory stress tests
- Test on constrained devices (~35KB free RAM)
- Memory fragmentation scenarios
- Heavy memory pressure tests
- Verify correct chunk size selection
- Run: `python test_esp8266_memory.py` or `pytest test_esp8266_memory.py -v`

## Quick Start

```bash
# Run unit tests (no hardware required)
python test_upload_optimization.py

# Run all tests with hardware
pytest test_benchmark_async.py test_upload_optimization.py -v -s

# Run ESP8266 specific tests
python test_esp8266_memory.py
```

## Test Matrix

| Test File | Hardware Required | Purpose |
|-----------|------------------|---------|
| `test_upload_optimization.py` | Optional | Validate optimization logic |
| `test_benchmark_async.py` | Yes | Performance comparison |
| `test_manual_chunk_comparison.py` | Yes | Manual chunk benchmarking |
| `test_esp8266_memory.py` | Yes (ESP8266) | Constrained device validation |

## Optimization Summary

### Small Files (<3KB)
- **Strategy**: Single exec_async call
- **Performance**: ~6x fewer operations vs chunked
- **Example**: `f=open('file','wb');f.write(data);f.close()`

### Large Files (≥3KB)
- **Strategy**: Chunked writes with auto-detected size
- **Chunk Selection**:
  - >100KB free: 2048 bytes (best performance)
  - 50-100KB free: 1024 bytes
  - 20-50KB free: 512 bytes
  - <20KB free: 256 bytes (safe for ESP8266)
- **Caching**: Detection result cached per connection

## Expected Results

### Benchmark Targets
- Small files (1-2KB): Async ≥ sync (no slower)
- Medium files (3-5KB): Async ~20-30% faster than sync
- Large files (10KB+): Async ~30-50% faster than sync
- Downloads: Async ~40-50% faster than sync

### ESP8266 Expectations
- Normal conditions (~35KB free): 512-byte chunks
- Heavy fragmentation (<20KB free): 256-byte chunks
- All uploads should succeed with correct verification

## Troubleshooting

**Tests fail with "No device found"**: Set `MICROPYTHON_DEVICE` environment variable or ensure device is connected.

**ESP8266 tests fail**: Update device port in test files (default: COM29).

**Performance worse than expected**: Check for:
- Background processes consuming CPU
- Slow baud rate (should be 115200)
- Device busy with other operations
- Windows Defender or antivirus interference
