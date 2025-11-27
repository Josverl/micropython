# Async Reports & Test Matrix

Centralized notes on refactoring work, coverage, performance findings, and how we validate the async stack.

## 1. Refactoring Highlights
- **Pytest migration:** All async tests now live under `tools/mpremote/tests` with shared fixtures (`event_loop`, `async_modules`, `hardware_target_info`, `require_target_platform`). The pytest hook enforces platform skips for Windows-only and hardware-required suites.
- **Command coverage:** `test_async_commands.py` reproduces the legacy shell scripts (`test_eval_exec_run.sh`, `test_filesystem.sh`, etc.) via fixtures for temp files, packages, and mocked state/args, reaching 100 % coverage for `commands_async.py`.
- **REPL + console tests:** `test_repl_async.py`, `test_repl_async_mount.py`, and `test_repl_async_unix.py` validate Ctrl-* flows, capture files, and mixed sync/async transports. Windows-only console tests retain explicit markers.
- **ESP8266 + manual chunk suites:** Hardware tests now rely on fixture-provided devices and auto-skipping. `test_manual_chunk_comparison.py`, `test_esp8266_fragmented.py`, `test_esp8266_memory.py`, and `test_esp8266_stress.py` consume `hardware_device` and `require_target_platform` so they never hardcode ports.

## 2. Test Suites at a Glance
| Suite | File(s) | Purpose | Hardware |
| --- | --- | --- | --- |
| Core unit tests | `test_async_modules.py`, `test_async_transport.py`, `test_async_comprehensive.py`, `test_async_coverage.py` | Structure, API contracts, encoding/decoding | No |
| Command + filesystem | `test_async_commands.py` (28 tests, down from 35) | Exec/eval/run, cp/mkdir/rm/tree—no sync fallback tests | Optional |
| REPL/Console | `test_repl_async*.py`, `test_main_async_mode.py` | Interactive flows, mounting, Unix backend | No |
| Integration | `test_integration.py`, `test_integration.py` (async workflow) | end-to-end w/out hardware | No |
| Hardware | `test_async_hardware.py`, ESP8266 suites, manual chunk comparison | Real board behavior, chunk detection, fragmentation | Yes |
| Benchmarks | `test_benchmark_async.py` | Upload/download throughput | Yes |

## 3. Dual Test Harness
- **Pytest (primary):** `pytest -v` from `tools/mpremote/tests` is the gate. Latest run (2025-11-22): `112 passed, 3 skipped` for async suites after code simplification. All PytestReturnNotNone warnings were fixed (see `test_integration.py`).
- **Bash scripts (legacy confidence):** `./run-mpremote-tests.sh` executes the historical shell tests (`test_errno.sh`, `test_filesystem.sh`, etc.). Run them whenever you touch filesystem, mip, or mounting behavior; they remain the quickest regression detector for CLI users.

## 4. Coverage Snapshot
(Last updated 2025-01-21)
| Module | Statements | Missing | Coverage |
| --- | --- | --- | --- |
| `protocol.py` | 40 | 0 | **100 %** |
| `repl_async.py` | 150 | 42 | **72 %** |
| `transport_serial_async.py` | 231 | 84 | **64 %** |
| `transport_async.py` | 45 | 27 | **40 %** |
| `console_async.py` | 106 | 70 | **34 %** |
| `commands_async.py` | 76 | 0 | **100 %** |
| **Total** | 648 | 289 | **55 %** |
_Priority gap_: add platform-mocked console tests and broaden transport base coverage to push totals upward.

## 5. Performance Findings (Windows Uploads)
Benchmark data shows async uploads lagging behind sync on Windows by up to 130 % for 10 KB files, while downloads achieve the expected 2× speedup. Root causes:
- `pyserial-asyncio` uses a polling backend on Windows; each `write()` + `drain()` introduces latency.
- `fs_writefile_async()` writes 256-byte chunks by default, triggering frequent drains.

**Mitigation plan:**
1. **Buffered drains (Option 1):** batch writes and call `drain()` periodically instead of per chunk.
2. **Adaptive chunk sizing (Option 2/3):** raise chunk size on Windows or when free memory allows; keep small chunks for constrained boards.
3. **Write coalescing (Option 5):** combine multiple small writes before hitting the transport.
4. **Fallback plan:** consider a Windows-specific backend using threads/pyserial if async buffering is insufficient (higher risk).
Progress on these experiments should be logged here with benchmark output from `pytest test_benchmark_async.py -v -s`.

## 6. Recent Fixes & Findings
- **Code simplification (2025-11-22):** Removed all `hasattr()` checks and sync fallback branches from async command handlers (`commands_async.py`). Core assumptions: asyncio/pyserial-asyncio always available in async mode, and async commands only run over AsyncSerialTransport. Eliminated ~220 lines of dead code and 7 fallback tests.
- **Exception handling cleanup (2025-11-22):** Replaced all `sys.exit()` calls in command handlers with `CommandFailure` exception. This eliminates "Task exception was never retrieved" asyncio warnings and provides clean error handling without exposing library internals.
- **Integration warnings resolved:** `test_integration.py` now asserts instead of returning booleans, eliminating PytestReturnNotNone warnings.
- **Hardware metadata fixture:** `hardware_target_info` probes `sys.platform`, `sys.implementation`, and `_machine` once per session; tests consume `require_target_platform()` to skip mismatched hardware (e.g. ESP8266 suites on RP2040 hardware now skip cleanly).
- **Manual chunk test gating:** `test_manual_chunk_comparison.py` pulls its device from CLI/env and is marked as `hardware_required + serial_required`.

## 7. Next Verification Steps
1. **Windows write-buffer prototype:** capture before/after benchmark tables (1 KB, 5 KB, 10 KB uploads) and attach to this document.
2. **Console coverage:** add pytest cases that mock stdin/stdout for POSIX + Windows paths, improving `console_async.py` coverage beyond 34 %.
3. **Docs + CI:** once coverage stabilizes, wire these suites into CI (Linux) and document how to run Windows hardware tests.

Update this report whenever you land refactors, change test structure, or gather new performance data.
