# Async mpremote User Guide

A concise how-to for working with the asyncio-enabled mpremote stack.

## 1. Prerequisites
- **Python environment:** Activate the project venv before doing anything: `source ~/micropython/.venv/bin/activate`.
- **Dependencies:** The venv already carries `pyserial` ≥ 3.3 and `pyserial-asyncio` ≥ 0.6. If you need to refresh, run `pip install -r tools/mpremote/tests/requirements.txt` inside the venv.
- **Hardware access:** Plug in your MicroPython board and note its serial port (`mpflash list --json`). You can pass the port explicitly with `--device=/dev/ttyACM0` or set `MICROPYTHON_DEVICE` / `MANUAL_CHUNK_DEVICE` / `ESP8266_DEVICE` env vars.

## 2. Quick Start (Python API)
```python
import asyncio
from mpremote.transport_serial_async import AsyncSerialTransport

async def main():
    transport = AsyncSerialTransport("/dev/ttyUSB0", baudrate=115200)
    await transport.connect()
    await transport.enter_raw_repl_async()

    stdout, _ = await transport.exec_raw_async("print('Hello async!')")
    print(stdout.decode())

    await transport.close_async()

asyncio.run(main())
```

## 3. State & Command Helpers
```python
import asyncio
from mpremote.main import State
from mpremote.commands_async import do_exec_async, do_eval_async

async def run_script(port: str):
    state = State()
    state.transport = AsyncSerialTransport(port, baudrate=115200)

    await state.transport.connect()
    await state.ensure_raw_repl_async()

    class Args:  # mimic argparse namespace
        follow = True
        command = ["print('ready')"]
        expr = "2 + 2"

    await do_exec_async(state, Args())
    await do_eval_async(state, Args())
    await state.transport.close_async()

asyncio.run(run_script("/dev/ttyUSB0"))
```
- All async helpers end with `_async`; sync wrappers (e.g. `do_exec_sync_wrapper`) remain available for legacy code but simply call the async version via `asyncio.run()`.

## 4. CLI Usage
The CLI still defaults to the sync transport, but the async stack is fully available to embedders or future flags. Recommended workflow while the feature flag is wired up:
1. Use mpremote normally for user-facing commands.
2. Use the async Python API (above) or custom scripts when you need concurrent operations.
3. Keep an eye on `ASYNC_MAIN_PLAN.md` for the status of the async CLI toggle.

## 5. Test & Benchmark Commands
- **Full pytest sweep:**
  ```bash
  cd tools/mpremote/tests
  pytest -v
  ```
- **Legacy bash harness:**
  ```bash
  cd tools/mpremote/tests
  ./run-mpremote-tests.sh
  ```
- **Upload/download benchmarks:**
  ```bash
  pytest test_benchmark_async.py -v -s
  ```
  (Requires a connected device; results are printed inline.)

## 6. Hardware-Aware Fixtures
Pytest fixtures automatically detect hardware details:
- `hardware_target_info` captures `sys.platform`, `sys.implementation`, `_machine`, `_build`, etc.
- `require_target_platform(platform="esp8266")` skips tests when the connected board does not match.
- `connected_transport` yields `(transport, writable_path)` and annotates `transport.target_info` for reuse.
Always request these fixtures instead of re-implementing device detection.

## 7. Troubleshooting
| Symptom | Resolution |
| --- | --- |
| `ImportError: pyserial-asyncio` | Activate the venv, then `pip install pyserial-asyncio`. |
| Tests hang waiting for hardware | Pass `--device` or set `MICROPYTHON_DEVICE`; unsupported boards will skip via `require_target_platform`. |
| Windows uploads slower than sync | Known issue; see the performance section in `ASYNC_REPORTS_AND_TESTS.md` for mitigation progress. |
| `TransportError: Not connected` | Ensure you call `await transport.connect()` before REPL or filesystem APIs. |

Keep this guide short—link to the main plan and reports for details.
