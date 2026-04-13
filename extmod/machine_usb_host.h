/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2024 MicroPython Contributors
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#ifndef MICROPY_INCLUDED_EXTMOD_MACHINE_USB_HOST_H
#define MICROPY_INCLUDED_EXTMOD_MACHINE_USB_HOST_H

#include "py/mpconfig.h"

#if MICROPY_PY_MACHINE_USB_HOST

#include "py/obj.h"
#include "py/runtime.h"

// USB speed constants
#define MP_USB_HOST_SPEED_LOW   0
#define MP_USB_HOST_SPEED_FULL  1

// USB endpoint transfer types
#define MP_USB_HOST_XFER_CONTROL    0
#define MP_USB_HOST_XFER_ISOCHRONOUS 1
#define MP_USB_HOST_XFER_BULK       2
#define MP_USB_HOST_XFER_INTERRUPT  3

// USB host device info, filled in by the port HAL after enumeration.
typedef struct _mp_usb_host_dev_info_t {
    uint16_t vid;
    uint16_t pid;
    uint8_t speed; // MP_USB_HOST_SPEED_xxx
    char manufacturer[64];
    char product[64];
    uint8_t dev_addr;
} mp_usb_host_dev_info_t;

// Port-specific HAL interface for USB host operations.
// Each port that supports USB host mode must provide an implementation.
typedef struct _mp_usb_host_hal_t {
    // Initialize USB host hardware (PHY, clocks, interrupts).
    // Returns 0 on success, negative on error.
    int (*init)(void);

    // Deinitialize USB host hardware and release resources.
    void (*deinit)(void);

    // Process USB host events. Called periodically from the scheduler
    // or a dedicated task.
    void (*task)(void);

    // Check if a USB device is currently connected and enumerated.
    bool (*device_connected)(void);

    // Get information about the connected device.
    // Returns 0 on success, negative on error.
    int (*get_device_info)(mp_usb_host_dev_info_t *info);

    // Perform a blocking control transfer.
    // For IN transfers, data points to a buffer and length is max bytes to read.
    // For OUT transfers, data points to data to send and length is the byte count.
    // Returns number of bytes transferred on success, negative on error.
    int (*control_transfer)(uint8_t bmRequestType, uint8_t bRequest,
        uint16_t wValue, uint16_t wIndex,
        uint8_t *data, uint16_t length, uint32_t timeout_ms);

    // Open a USB endpoint for transfers.
    // ep_addr includes direction bit (0x80 for IN).
    // ep_type is one of MP_USB_HOST_XFER_xxx.
    // Returns 0 on success, negative on error.
    int (*open_endpoint)(uint8_t ep_addr, uint8_t ep_type, uint16_t max_pkt_size);

    // Close a previously opened endpoint.
    void (*close_endpoint)(uint8_t ep_addr);

    // Submit an asynchronous transfer on an endpoint.
    // Completion is signalled by calling mp_usb_host_xfer_complete_cb().
    // Returns 0 on success, negative on error.
    int (*submit_xfer)(uint8_t ep_addr, uint8_t *buf, uint16_t len);
} mp_usb_host_hal_t;

// Singleton USB host Python object.
typedef struct _mp_obj_usb_host_t {
    mp_obj_base_t base;

    // Python callback functions
    mp_obj_t connect_cb;
    mp_obj_t disconnect_cb;
    mp_obj_t xfer_cb;

    // Current state
    bool active;
    bool device_present;

    // Port HAL
    const mp_usb_host_hal_t *hal;
} mp_obj_usb_host_t;

// The port must provide this function to return the HAL implementation.
const mp_usb_host_hal_t *mp_usb_host_get_hal(void);

// Callback from port HAL when a device is connected.
void mp_usb_host_device_connect_cb(void);

// Callback from port HAL when a device is disconnected.
void mp_usb_host_device_disconnect_cb(void);

// Callback from port HAL when an async transfer completes.
void mp_usb_host_xfer_complete_cb(uint8_t ep_addr, bool result, uint16_t xferred_bytes);

#endif // MICROPY_PY_MACHINE_USB_HOST

#endif // MICROPY_INCLUDED_EXTMOD_MACHINE_USB_HOST_H
