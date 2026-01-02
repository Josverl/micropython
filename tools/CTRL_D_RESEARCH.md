# Research Findings: Ctrl-D Handling in RFC2217 and MicroPython

## Investigation Summary

### 1. RFC2217 Protocol Handling of Ctrl-D

**Finding**: Ctrl-D (0x04 / EOT) passes through RFC2217 **unchanged**.

**Evidence**:
- RFC2217 filter only intercepts Telnet IAC sequences (0xFF)
- Tested with direct filter test - Ctrl-D passes through as-is
- `SET_CONTROL_REQ_BREAK_STATE` happens to be 0x04, but it's in a different context (COM_PORT_OPTION subnegotiation)

```python
# Direct test results:
Input: b'\x04' (Ctrl-D)
Filtered: b'\x04' (unchanged) ✓
```

### 2. MicroPython Unix Port Behavior

**Critical Finding**: MicroPython unix port **EXITS** when it receives standalone Ctrl-D in raw REPL!

**Evidence from testing**:
```
Process started in raw REPL
Send standalone Ctrl-D (0x04)
Response: b'OK\r\r\n'
Process status: TERMINATED (exit code: 0) ✗✗✗
```

**Root cause** (from source code analysis):
- `shared/runtime/pyexec.c`: When raw REPL receives Ctrl-D with empty command buffer, it returns `PYEXEC_FORCED_EXIT`
- `ports/unix/main.c`: `PYEXEC_FORCED_EXIT` causes the process to exit (by design - Unix EOF handling)

### 3. Why Soft Reboot Emulation Failed

The soft reboot emulation attempts were failing because:

1. **State tracking was unreliable**: `_in_raw_repl` flag wasn't being checked correctly
2. **Timing issue**: By the time we detect Ctrl-D, it's already written to stdin
3. **Process dies**: Unix port exits immediately on Ctrl-D, before we can restart

### 4. Solution Requirements

To make mpremote work without `resume`, we must:

1. **Intercept Ctrl-D BEFORE** it reaches MicroPython's stdin
2. **Do NOT write** standalone Ctrl-D to the process
3. **Restart the process** and inject expected output:
   - `OK` (acknowledgment)
   - `soft reboot\r\n` (what mpremote expects)
   - Re-enter raw REPL automatically
   - Send the new raw REPL prompt

### 5. Current Code Status

The infrastructure exists in `mp_rfc2217_bridge.py`:
- Redirector.writer() has interception logic (line 428-436)
- VirtualSerialPort has restart_callback support  
- `_perform_soft_reboot()` method exists

**Issues**:
- State tracking of `_in_raw_repl` is unreliable
- Needs simpler detection: just check if filtered_data == b'\x04' in writer()
- Must NOT write Ctrl-D to process - current code writes it on line 440

## Recommended Fix

```python
# In Redirector.writer():
if filtered_data == b'\x04':
    # ALWAYS intercept standalone Ctrl-D to prevent process exit
    self.log.info('Intercepted Ctrl-D - performing soft reboot emulation')
    if hasattr(self.serial, '_perform_soft_reboot'):
        self.serial._perform_soft_reboot()
    # DO NOT write to serial - this would kill the process!
    continue  # Skip the write
```

This simpler approach:
- Doesn't rely on state tracking
- Intercepts ALL standalone Ctrl-D bytes
- Prevents process termination
- Triggers restart and output injection

## Test Results

| Test | RFC2217 Pass-through | Unix Port Behavior |
|------|---------------------|-------------------|
| Regular text | ✓ Unchanged | ✓ Processes normally |
| Ctrl-D standalone | ✓ Unchanged (0x04) | ✗ Process EXITS |
| Code + Ctrl-D | ✓ Unchanged | ✓ Executes code |
| IAC (0xFF) | ✓ Escaped properly | N/A |

## Conclusion

The user's suggestion was correct - we needed to investigate how RFC2217 and the unix port handle Ctrl-D separately. The findings show:

1. RFC2217 is not transforming Ctrl-D
2. The problem is MicroPython unix port's exit-on-EOF behavior
3. Solution requires interception BEFORE the byte reaches MicroPython
4. Current code is close but needs refinement to work reliably
