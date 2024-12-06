#!/bin/bash
set -e

# Test script to verify the new functionality of waiting for a device connection

# Function to simulate device connection
simulate_device_connection() {
    sleep 2
    touch /tmp/test_device
}

# Function to simulate device disconnection
simulate_device_disconnection() {
    sleep 2
    rm /tmp/test_device
}

# Test case for waiting for device connection
test_wait_for_device_connection() {
    echo "Testing wait for device connection..."
    simulate_device_connection &
    $MPREMOTE connect --wait 5 /tmp/test_device
    if [ -e /tmp/test_device ]; then
        echo "Device connected successfully"
    else
        echo "Failed to connect to device"
        exit 1
    fi
}

# Test case for device disconnection and reconnection
test_device_reconnection() {
    echo "Testing device reconnection..."
    simulate_device_disconnection &
    $MPREMOTE connect --reconnect /tmp/test_device
    if [ ! -e /tmp/test_device ]; then
        echo "Device disconnected successfully"
    else
        echo "Failed to disconnect device"
        exit 1
    fi

    simulate_device_connection &
    $MPREMOTE connect --reconnect /tmp/test_device
    if [ -e /tmp/test_device ]; then
        echo "Device reconnected successfully"
    else
        echo "Failed to reconnect to device"
        exit 1
    fi
}

# Run the test cases
test_wait_for_device_connection
test_device_reconnection

echo "All tests passed"
