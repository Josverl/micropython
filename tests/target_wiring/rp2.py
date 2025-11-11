# Target wiring for general rp2 board.
#
# Connect:
# - GPIO0 to GPIO1 (UART loopback)
# - GPIO2 to GPIO3 (sleep wake test, optional)

uart_loopback_args = (0,)
uart_loopback_kwargs = {"tx": "GPIO0", "rx": "GPIO1"}

# Sleep wake test configuration (optional)
# Connect sleep_trigger_pin to sleep_wake_pin for GPIO wake tests
sleep_wake_pin = 2      # Pin configured to wake from sleep
sleep_trigger_pin = 3   # Pin used to generate wake signal
