# Test BLE PHY selection on an established connection.

from micropython import const
import time, machine, bluetooth

TIMEOUT_MS = 5000

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_PHY_UPDATE = const(32)

waiting_events = {}


def irq(event, data):
    if event == _IRQ_CENTRAL_CONNECT:
        print("_IRQ_CENTRAL_CONNECT")
        waiting_events[event] = data[0]
    elif event == _IRQ_CENTRAL_DISCONNECT:
        print("_IRQ_CENTRAL_DISCONNECT")
    elif event == _IRQ_PERIPHERAL_CONNECT:
        print("_IRQ_PERIPHERAL_CONNECT")
        waiting_events[event] = data[0]
    elif event == _IRQ_PERIPHERAL_DISCONNECT:
        print("_IRQ_PERIPHERAL_DISCONNECT")
    elif event == _IRQ_PHY_UPDATE:
        print("_IRQ_PHY_UPDATE")
        waiting_events[event] = (data[1], data[2])

    if event not in waiting_events:
        waiting_events[event] = None


def wait_for_event(event, timeout_ms):
    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
        if event in waiting_events:
            return waiting_events.pop(event)
        machine.idle()
    raise ValueError("Timeout waiting for {}".format(event))


ble = bluetooth.BLE()
ble.irq(irq)


def activate_or_skip():
    if not hasattr(ble, "gap_set_phy"):
        # Firmware built without MICROPY_PY_BLUETOOTH_ENABLE_PHY_SELECTION.
        multitest.skip()
    ble.active(1)
    try:
        supported = ble.config("phys")
    except OSError:
        # This backend can't ask the controller; attempt the change anyway.
        return
    if not (supported & bluetooth.PHY_2M):
        multitest.skip()


# Acting in peripheral role.
def instance0():
    activate_or_skip()
    multitest.globals(BDADDR=ble.config("mac"))
    print("gap_advertise")
    ble.gap_advertise(20_000, b"\x02\x01\x06\x04\xffMPY")
    multitest.next()
    try:
        wait_for_event(_IRQ_CENTRAL_CONNECT, TIMEOUT_MS)
        # The PHY change is driven by the central; both ends see the result.
        print("2M:", wait_for_event(_IRQ_PHY_UPDATE, TIMEOUT_MS))
        wait_for_event(_IRQ_CENTRAL_DISCONNECT, TIMEOUT_MS)
    finally:
        ble.active(0)


# Acting in central role.
def instance1():
    activate_or_skip()
    multitest.next()
    try:
        print("gap_connect")
        ble.gap_connect(*BDADDR)
        conn_handle = wait_for_event(_IRQ_PERIPHERAL_CONNECT, TIMEOUT_MS)

        print("gap_set_phy")
        try:
            ble.gap_set_phy(conn_handle, tx_phy=bluetooth.PHY_2M, rx_phy=bluetooth.PHY_2M)
        except OSError:
            # Capability wasn't known up front and the controller refused.
            multitest.skip()
        print("2M:", wait_for_event(_IRQ_PHY_UPDATE, TIMEOUT_MS))

        print("gap_disconnect:", ble.gap_disconnect(conn_handle))
        wait_for_event(_IRQ_PERIPHERAL_DISCONNECT, TIMEOUT_MS)
    finally:
        ble.active(0)
