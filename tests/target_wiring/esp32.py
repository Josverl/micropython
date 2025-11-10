# Target wiring for general esp32 board.
#
# Connect:
# - GPIO4 to GPIO5 (UART loopback)
# - GPIO2 to GPIO15 (sleep wake test, optional)

uart_loopback_args = (1,)
uart_loopback_kwargs = {"tx": 4, "rx": 5}

# Sleep wake test configuration (optional)
# Connect sleep_trigger_pin to sleep_wake_pin for GPIO wake tests
sleep_wake_pin = 2      # Pin configured to wake from sleep
sleep_trigger_pin = 15  # Pin used to generate wake signal
