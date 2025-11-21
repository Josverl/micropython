# Async mpremote Main Plan

This is the single source of truth for the asyncio migration effort. Keep it concise, actionable, and up to date when work lands.

## Snapshot (2025-11-21)
- **Phases 1-3 complete:** async transport, commands, console/REPL, and State coexist cleanly with the legacy sync stack.
- **Full pytest suite:** `pytest -v` under `tools/mpremote/tests` currently delivers `207 passed, 8 skipped, 0 failed`; skips are Windows-only console tests plus hardware-gated ESP8266/manual chunk suites.
- **Dual harness:** legacy bash scripts in `tools/mpremote/tests/run-mpremote-tests.sh` remain the sanity check for regressions; always keep them passing after refactors.
- **Hardware gating:** fixtures now auto-detect `sys.platform`, `sys.implementation`, and serial ports; tests must skip (never fail) when required boards are missing.
- **Performance gap:** Windows async uploads trail sync by 20–130% for 1–10 KB transfers; the buffering plan below drives the next wave of work.

## Phase Overview
| Phase | Focus | Status | Notes |
| --- | --- | --- | --- |
| 1 | Build async transport layer + Raw REPL protocol | ✅ Done | `transport_async.py`, `transport_serial_async.py`, `protocol.py`
| 2 | Async command layer + filesystem/mip/mount | ✅ Done | `commands_async.py` + sync wrappers
| 3 | Async console + REPL loop | ✅ Done | `console_async.py`, `repl_async.py`, async State helpers
| 4 | Testing, docs, adoption | ⚙️ Active | Finish dual-harness reliability, shrink warnings, document workflows
| 5 | Optimization & polish | 📋 Next | Windows upload buffering, chunk tuning, error ergonomics
| 6 | Future transports & deprecation path | 🧭 Future | WebSocket/BLE transports, sync API sunset plan

## Phase 4 Goals (Active)
1. **Test Reliability**
   - Keep `pytest -v` green; expand coverage for `commands_async.py`, `console_async.py`.
   - Ensure hardware suites (`test_async_hardware.py`, ESP8266 stress tests, manual chunk benchmarking) skip gracefully without devices.
2. **Documentation & Guidance**
   - Maintain `ASYNC_USER_GUIDE.md` (see below) for quick starts.
   - Surface fixture usage (`hardware_target_info`, `require_target_platform`) inside tests when touching hardware logic.
3. **Adoption Hooks**
   - Confirm CLI plumbing (feature flags/env vars) before defaulting to async.
   - Capture migration friction in `ASYNC_REPORTS_AND_TESTS.md` so future agents know open issues.
   - Global `--async` flag and `MPREMOTE_ASYNC` env var now flip command dispatch + REPL; when transports lack async primitives we emit a warning and fall back to sync behavior.

## Phase 5 Preview (Performance & Polish)
- **Buffered writes on Windows:** defer `drain()` calls, coalesce small chunks (Option 1 + Option 5 from the retired performance doc).
- **Chunk sizing heuristics:** raise default upload chunk when memory allows; keep per-board detection logic.
- **Better telemetry:** add optional tracing for async write latency to reproduce perf issues.

## Active Workstreams & Priorities
1. **Maintain green test matrix.** Re-run `pytest -v` plus targeted suites after any change to transports, commands, or fixtures.
2. **Tackle Windows upload gap.** Prototype buffered writes and/or larger chunk heuristics; benchmark with `test_benchmark_async.py`.
3. **Document and instrument.** Keep user-facing instructions and agent guidance synchronized with code changes.

## Agent Instructions
- **Environment:** `source ~/micropython/.venv/bin/activate` before running scripts; dependencies (e.g. `pyserial-asyncio`) are already pinned in that venv.
- **Hardware discovery:** use `mpflash list --json` or rely on the fixtures (`--device` CLI flag, `MICROPYTHON_DEVICE`, `MANUAL_CHUNK_DEVICE`, `ESP8266_DEVICE`). Never hardcode `COM29` or similar inside tests.
- **Test cadence:**
  always run both test suites before submitting changes:
  - Fast check: `pytest -v` from `tools/mpremote/tests`.
  - Legacy harness: `./run-mpremote-tests.sh` (in the same folder).
  - Targeted hardware suites: run only when you have the required board; otherwise ensure skips are informative.
- **Before sending PR-quality changes:** 
   - ensure docs in this folder stay ≤3 files (plan, user guide, reports) and reflect the latest reality.
   - run ruff format and lint checks: `ruff check tools/mpremote`.

## Shell-to-Pytest Migration Guide (Example: `test_eval_exec_run`)
Use this playbook when converting legacy `.sh` harnesses (plus `.exp` golden files) into pytest suites that exercise both sync and async CLI paths.

1. **Create a helper-backed pytest module.** Mirror the shell script filename (e.g. `test_eval_exec_run.sh` → `test_eval_exec_run.py`). Use existing fixtures from `conftest.py` such as `mpremote_cmd`, `cli_mode`, and `temp_script` so tests automatically cover `mpremote` and `mpremote --async`.
2. **Port commands verbatim.** Each logical CLI snippet in the shell script becomes its own `@pytest.mark.cli` test (e.g. simple exec, eval, run with `--no-follow`). Call `helpers.run_mpremote()` to spawn the command and assert on `result.returncode`, `stdout`, and `stderr` instead of diffing against a `.exp` file.
3. **Replace heredocs with `write_script`.** Instead of `cat <<EOF` blocks, call `helpers.write_script(temp_script, code)`; the helper wraps `textwrap.dedent`, keeping fixtures tidy while matching the original script contents.
4. **Handle timing-sensitive cases explicitly.** The shell version relied on `sleep` to allow `--no-follow` commands to finish. The pytest port documents that we intentionally do not assert on output for those cases, keeping parity without introducing flaky waits.
5. **DO NOT delete the `.sh` and `.exp` files**—they must stay in the tree for the next two minor releases so the legacy harness keeps working while the async pytest suite matures.

Future migrations should follow the same pattern: enumerate each CLI action as its own test, reuse the shared helpers, and capture expectations directly in Python asserts instead of external goldens.

## Backlog (ordered)
1. **Async CLI adoption path**
   - ✅ 2025-11-21: CLI flag/env parsing plus REPL dispatch landed; `--async` and `MPREMOTE_ASYNC=1` select async handlers with sync fallback messaging.
   - ⏭ Detect and instantiate `AsyncSerialTransport` automatically when async mode is requested; ensure legacy-only commands degrade cleanly or error with actionable guidance.
   - ⏭ Document the flag/env usage workflow inside `ASYNC_USER_GUIDE.md` and `docs/reference/mpremote.rst` so users can opt-in without spelunking the plan docs.
2. Extend pytest coverage for `console_async.py` (platform mocks) and `commands_async.py` (remaining filesystem verbs).
3. Promote async documentation into `docs/reference/mpremote.rst` once behaviour stabilizes.
4. Define sync API deprecation timeline once async becomes default (Phase 6).

Keep this plan updated whenever scope, priorities, or status changes. Use short diffs so future agents immediately understand what to do next.
