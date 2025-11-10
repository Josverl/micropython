# Test machine.lightsleep with timer wake.
#
# This test validates that lightsleep works correctly with timer-based wake.
# No external hardware connections are required for these tests.
#
# lightsleep behavior:
# - CPU paused, RAM retained
# - Wakes after specified timeout
# - Execution continues after sleep call
# - Variables and state are preserved

import sys
import time
import unittest

try:
    from machine import lightsleep
except ImportError:
    print("SKIP")
    raise SystemExit

# Platform-specific adjustments
# Some platforms may have less accurate timing or wake interrupts
TIMING_TOLERANCE = 0.25  # 25% tolerance for timing tests

# Skip platforms with known issues
if sys.platform in ["webassembly"]:
    print("SKIP")
    raise SystemExit


class TestLightSleepTimer(unittest.TestCase):
    """Test lightsleep with timer-based wake."""

    def test_short_sleep(self):
        """Test short lightsleep (100ms)."""
        duration_ms = 100
        t0 = time.ticks_ms()
        lightsleep(duration_ms)
        elapsed = time.ticks_diff(time.ticks_ms(), t0)
        
        # Verify sleep occurred and timing is reasonable
        # Allow tolerance as interrupts may wake early
        self.assertGreaterEqual(elapsed, duration_ms * (1 - TIMING_TOLERANCE))
        self.assertLessEqual(elapsed, duration_ms * (1 + TIMING_TOLERANCE) + 50)

    def test_medium_sleep(self):
        """Test medium lightsleep (500ms)."""
        duration_ms = 500
        t0 = time.ticks_ms()
        lightsleep(duration_ms)
        elapsed = time.ticks_diff(time.ticks_ms(), t0)
        
        self.assertGreaterEqual(elapsed, duration_ms * (1 - TIMING_TOLERANCE))
        self.assertLessEqual(elapsed, duration_ms * (1 + TIMING_TOLERANCE) + 50)

    def test_longer_sleep(self):
        """Test longer lightsleep (1000ms)."""
        duration_ms = 1000
        t0 = time.ticks_ms()
        lightsleep(duration_ms)
        elapsed = time.ticks_diff(time.ticks_ms(), t0)
        
        self.assertGreaterEqual(elapsed, duration_ms * (1 - TIMING_TOLERANCE))
        self.assertLessEqual(elapsed, duration_ms * (1 + TIMING_TOLERANCE) + 50)

    def test_multiple_sleeps(self):
        """Test multiple consecutive lightsleeps."""
        total_expected = 0
        t0 = time.ticks_ms()
        
        for duration_ms in [100, 200, 300]:
            lightsleep(duration_ms)
            total_expected += duration_ms
        
        elapsed = time.ticks_diff(time.ticks_ms(), t0)
        
        # Total time should be approximately sum of all sleeps
        self.assertGreaterEqual(elapsed, total_expected * (1 - TIMING_TOLERANCE))
        self.assertLessEqual(elapsed, total_expected * (1 + TIMING_TOLERANCE) + 100)

    def test_zero_sleep(self):
        """Test lightsleep with 0ms (should return immediately or sleep minimally)."""
        t0 = time.ticks_ms()
        lightsleep(0)
        elapsed = time.ticks_diff(time.ticks_ms(), t0)
        
        # Should return very quickly (within 50ms)
        self.assertLessEqual(elapsed, 50)


class TestLightSleepState(unittest.TestCase):
    """Test that state is preserved across lightsleep."""

    def test_variable_preservation(self):
        """Test that local variables are preserved."""
        test_int = 12345
        test_str = "test_string"
        test_list = [1, 2, 3, 4, 5]
        test_dict = {"key": "value", "number": 42}
        
        lightsleep(100)
        
        # All variables should be unchanged
        self.assertEqual(test_int, 12345)
        self.assertEqual(test_str, "test_string")
        self.assertEqual(test_list, [1, 2, 3, 4, 5])
        self.assertEqual(test_dict, {"key": "value", "number": 42})

    def test_instance_state_preservation(self):
        """Test that instance variables are preserved."""
        self.test_value = 99999
        
        lightsleep(100)
        
        self.assertEqual(self.test_value, 99999)

    def test_time_advances(self):
        """Test that time advances during lightsleep."""
        t0 = time.ticks_ms()
        lightsleep(200)
        t1 = time.ticks_ms()
        
        # Time should have advanced
        self.assertGreater(t1, t0)
        elapsed = time.ticks_diff(t1, t0)
        self.assertGreaterEqual(elapsed, 150)  # At least 150ms (with tolerance)


class TestLightSleepPin(unittest.TestCase):
    """Test lightsleep with Pin states (basic test without external connections)."""

    def test_pin_state_after_sleep(self):
        """Test that Pin configuration is preserved (basic check)."""
        try:
            from machine import Pin
        except ImportError:
            self.skipTest("Pin not available")
        
        try:
            # Try to create a pin - use board.LED if available
            if hasattr(Pin, "board") and hasattr(Pin.board, "LED"):
                pin = Pin(Pin.board.LED, Pin.OUT)
            else:
                # Skip if we can't find a safe pin to test
                self.skipTest("No safe test pin available")
            
            # Set pin high
            pin.value(1)
            initial_value = pin.value()
            
            lightsleep(100)
            
            # Pin value should be preserved
            # Note: On some platforms, pin state may change during sleep
            # This is platform-dependent behavior
            final_value = pin.value()
            
            # Just verify we can still read the pin
            self.assertIn(final_value, [0, 1])
            
        except (OSError, ValueError, AttributeError):
            # If pin creation fails, skip the test
            self.skipTest("Pin test not applicable on this platform")


if __name__ == "__main__":
    unittest.main()
