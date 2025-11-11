# Research: Testing machine.lightsleep and machine.deepsleep

## Overview
This document outlines research findings and implementation plan for creating hardware tests for `machine.lightsleep()` and `machine.deepsleep()` functions in MicroPython.

## Test Framework Analysis

### Current Testing Patterns in MicroPython

1. **unittest-based tests** (located in `tests/extmod_hardware/`)
   - Used for hardware-specific functionality requiring special setup
   - Tests inherit from `unittest.TestCase`
   - Can use `@unittest.skipIf()` for platform-specific skips
   - Example: `machine_i2c_target.py`

2. **Expected output tests** (`.exp` files)
   - Used when output is predictable and platform-independent
   - Test output compared against `.exp` file
   - Example: `machine_uart_irq_rx.py`

3. **Multi-instance tests** (located in `tests/multi_*/`)
   - Used for tests requiring multiple connected devices
   - Example: `stress_deepsleep_reconnect.py` for Bluetooth

### Target Wiring Configuration

Files in `tests/target_wiring/` define platform-specific hardware connections:
- `esp32.py`: GPIO4 to GPIO5 for UART loopback
- `rp2.py`: GPIO0 to GPIO1 for UART loopback
- Other platforms: PYBx.py, nrf.py, samd.py, etc.

These files export variables that tests import to get correct pin configurations.

## Sleep Function Capabilities

### Common Features (all platforms)
- Timer-based wake (sleep for N milliseconds)
- Platform detection via `sys.platform` and `sys.implementation._machine`

### ESP32 Specific Features
- **Wake sources:**
  - Timer wake (all ESP32 variants)
  - EXT0 wake (single pin, high or low level)
  - EXT1 wake (multiple pins, any high or all low)
  - Touchpad wake (capacitive touch)
  - ULP wake (Ultra Low Power coprocessor)
  
- **Reset/Wake reason detection:**
  - `machine.reset_cause()`: Returns reason for last reset
  - `machine.wake_reason()`: Returns reason for wake from sleep
  - Constants: `DEEPSLEEP_RESET`, `PIN_WAKE`, `TIMER_WAKE`, etc.

### RP2 Specific Features
- Timer-based wake
- GPIO-based wake
- Thread-safe lightsleep (can be called from multiple threads)

### Behavioral Differences

**lightsleep:**
- CPU paused, RAM retained
- UART/serial typically remains connected
- Can be woken by interrupts
- Returns to next line of code after wake

**deepsleep:**
- Full system reset after wake
- RAM lost (except RTC memory on some platforms)
- UART/serial disconnected
- Execution starts from boot.py/main.py after wake
- Detectable via `machine.reset_cause() == machine.DEEPSLEEP_RESET`

## Implementation Plan

### Phase 1: Basic Timer-Based Sleep Tests

Create `tests/extmod_hardware/machine_sleep.py` with unittest-based tests:

1. **lightsleep tests:**
   - Test basic timer wake (various durations: 100ms, 500ms, 1000ms)
   - Verify timing accuracy (within tolerance)
   - Test state preservation (variables, pin states)
   - Test immediate wake (0ms sleep)

2. **deepsleep tests:**
   - Test timer-based deepsleep with state file
   - Verify reset cause after wake
   - Test RTC memory preservation (if available)
   - Use a marker file to track test state across reboots

### Phase 2: GPIO Wake Tests

Extend target_wiring configurations to support sleep tests:

1. **Add to target_wiring files:**
   ```python
   # tests/target_wiring/esp32.py
   # Add GPIO wake configuration
   sleep_wake_pin = 4  # Pin to trigger wake
   sleep_trigger_pin = 5  # Pin to generate wake signal
   ```

2. **Implement GPIO wake tests:**
   - Configure wake pin before sleep
   - Use second pin to generate wake signal (via Timer or IRQ)
   - Verify wake occurs and wake_reason is correct

### Phase 3: Platform-Specific Wake Sources

Test platform-specific features where available:

**ESP32:**
- EXT0 wake (single pin)
- EXT1 wake (multiple pins)
- Touchpad wake (if hardware supports)

**RP2:**
- Thread-based lightsleep tests (already exists)

### Test Structure Example

```python
# tests/extmod_hardware/machine_sleep.py
import sys
import time
import unittest

try:
    from machine import lightsleep, deepsleep, reset_cause, wake_reason
except ImportError:
    print("SKIP")
    raise SystemExit

class TestLightSleep(unittest.TestCase):
    def test_timer_wake(self):
        """Test lightsleep with timer wake"""
        durations = [100, 250, 500]
        for duration_ms in durations:
            t0 = time.ticks_ms()
            lightsleep(duration_ms)
            elapsed = time.ticks_diff(time.ticks_ms(), t0)
            # Allow 20% tolerance for timing
            self.assertAlmostEqual(elapsed, duration_ms, delta=duration_ms * 0.2)
    
    def test_state_preservation(self):
        """Test that variables are preserved across lightsleep"""
        test_value = 12345
        lightsleep(100)
        self.assertEqual(test_value, 12345)

class TestDeepSleep(unittest.TestCase):
    # Note: deepsleep tests are more complex due to device reset
    # May need special handling or separate test files
    pass

if __name__ == "__main__":
    unittest.main()
```

## Challenges and Solutions

### Challenge 1: Testing deepsleep
**Problem:** Device resets after deepsleep, losing test state

**Solutions:**
1. Use filesystem to persist state between boots
2. Use RTC memory (platform-specific)
3. Create multi-stage test with boot script detection
4. Leverage `machine.reset_cause()` to detect wake

### Challenge 2: Timing accuracy
**Problem:** Sleep timing varies based on system load and interrupts

**Solutions:**
1. Use generous timing tolerances (±20%)
2. Multiple test runs and averaging
3. Disable interrupts where possible during test
4. Document expected timing variations per platform

### Challenge 3: Hardware requirements
**Problem:** Some wake sources require external connections

**Solutions:**
1. Start with timer-based tests (no hardware needed)
2. Document required connections in test file header
3. Use target_wiring configs for platform-specific pins
4. Make hardware-dependent tests optional/skippable

### Challenge 4: Serial disconnect on some platforms
**Problem:** USB serial may disconnect during sleep

**Solutions:**
1. Use explicit UART connections for testing
2. Test framework handles reconnection
3. Document platform-specific behavior
4. For deepsleep, rely on filesystem or next boot detection

## Testing Strategy

### Minimal Hardware Setup
- No external connections required for basic timer-based tests
- Tests can run on any MicroPython board with sleep support

### Full Hardware Setup
- GPIO loopback for wake pin testing
- Configuration defined in target_wiring files
- Format: `sleep_wake_pin` and `sleep_trigger_pin`

### Test Execution
```bash
# Run on connected hardware
./run-tests.py -t /dev/ttyACM0 tests/extmod_hardware/machine_sleep.py

# Run specific platform tests
./run-tests.py -t /dev/ttyACM0 tests/ports/esp32/esp32_deepsleep.py
```

## Recommended Test Files

1. `tests/extmod_hardware/machine_lightsleep.py`
   - Basic timer-based lightsleep tests
   - State preservation tests
   - Multi-platform compatible

2. `tests/extmod_hardware/machine_deepsleep.py`
   - Timer-based deepsleep with state persistence
   - Reset cause verification
   - Platform-agnostic where possible

3. `tests/extmod_hardware/machine_sleep_gpio.py`
   - GPIO wake tests requiring loopback
   - Uses target_wiring configurations
   - Platform-specific variations

4. `tests/ports/esp32/esp32_sleep_ext.py` (optional)
   - ESP32-specific wake sources (EXT0, EXT1, touchpad, ULP)
   - Advanced sleep features

5. Update `tests/target_wiring/*.py`
   - Add sleep test pin configurations
   - Document required connections

## Success Criteria

1. Tests run successfully on Unix port (where sleep is stubbed)
2. Tests pass on real hardware (ESP32, RP2, etc.)
3. Tests are maintainable and well-documented
4. Timing tests have appropriate tolerances
5. Hardware requirements are clearly documented
6. Tests can be skipped on unsupported platforms

## Next Steps

1. Implement Phase 1: Basic timer-based tests
2. Update target_wiring configurations
3. Test on multiple platforms (ESP32, RP2)
4. Iterate based on real hardware behavior
5. Add documentation to main test README
6. Consider GPIO wake tests (Phase 2)
7. Add platform-specific tests (Phase 3) as needed
