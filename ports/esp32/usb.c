/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2021 Damien P. George
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

#include "py/runtime.h"
#include "py/mphal.h"
#include "usb.h"

#if MICROPY_HW_ENABLE_USBDEV

#include "esp_mac.h"
#include "esp_rom_gpio.h"
#include "esp_private/usb_phy.h"

#include "shared/tinyusb/mp_usbd.h"

static usb_phy_handle_t phy_hdl;

void usb_phy_init(void) {
    // ref: https://github.com/espressif/esp-usb/blob/4b6a798d0bed444fff48147c8dcdbbd038e92892/device/esp_tinyusb/tinyusb.c

    // Configure USB PHY
    static const usb_phy_config_t phy_conf = {
        .controller = USB_PHY_CTRL_OTG,
        .otg_mode = USB_OTG_MODE_DEVICE,
        .target = USB_PHY_TARGET_INT,
    };

    // Init ESP USB Phy
    usb_new_phy(&phy_conf, &phy_hdl);
}

#if CONFIG_IDF_TARGET_ESP32S3 || CONFIG_IDF_TARGET_ESP32P4
void usb_usj_mode(void) {
    // Switch the USB PHY back to Serial/Jtag mode, disabling OTG support
    // This should be run before jumping to bootloader.
    usb_del_phy(phy_hdl);
    usb_phy_config_t phy_conf = {
        .controller = USB_PHY_CTRL_SERIAL_JTAG,
    };
    usb_new_phy(&phy_conf, &phy_hdl);
}
#endif

void mp_usbd_port_get_serial_number(char *serial_buf) {
    // use factory default MAC as serial ID
    uint8_t mac[8];
    esp_efuse_mac_get_default(mac);
    MP_STATIC_ASSERT(sizeof(mac) * 2 <= MICROPY_HW_USB_DESC_STR_MAX);
    mp_usbd_hex_str(serial_buf, mac, sizeof(mac));
}

#endif // MICROPY_HW_ENABLE_USBDEV

#if MICROPY_PY_MACHINE_USB_HOST

#include <string.h>
#include "esp_mac.h"
#include "esp_private/usb_phy.h"
#include "usb/usb_host.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "extmod/machine_usb_host.h"

static usb_phy_handle_t host_phy_hdl;
static bool usb_host_installed = false;
static bool usb_host_task_running = false;
static TaskHandle_t usb_host_task_handle = NULL;
static usb_host_client_handle_t usb_host_client_hdl = NULL;
static uint8_t usb_host_dev_addr = 0;

// Forward declarations
static void usb_host_lib_task(void *arg);
static void usb_host_client_event_cb(const usb_host_client_event_msg_t *event_msg, void *arg);

// Callback for synchronous transfer completion.
static void usb_host_xfer_done_cb(usb_transfer_t *transfer) {
    SemaphoreHandle_t sem = (SemaphoreHandle_t)transfer->context;
    xSemaphoreGive(sem);
}

static int esp32_usb_host_init(void) {
    if (usb_host_installed) {
        return 0;
    }

    // Configure USB PHY for host mode
    usb_phy_config_t phy_conf = {
        .controller = USB_PHY_CTRL_OTG,
        .otg_mode = USB_OTG_MODE_HOST,
        .target = USB_PHY_TARGET_INT,
    };

    esp_err_t err = usb_new_phy(&phy_conf, &host_phy_hdl);
    if (err != ESP_OK) {
        return -1;
    }

    // Install USB host library
    usb_host_config_t host_config = {
        .skip_phy_setup = true,
        .intr_flags = ESP_INTR_FLAG_LEVEL1,
    };
    err = usb_host_install(&host_config);
    if (err != ESP_OK) {
        usb_del_phy(host_phy_hdl);
        return -1;
    }
    usb_host_installed = true;

    // Register a client
    usb_host_client_config_t client_config = {
        .is_synchronous = false,
        .max_num_event_msg = 5,
        .async = {
            .client_event_callback = usb_host_client_event_cb,
            .callback_arg = NULL,
        },
    };
    err = usb_host_client_register(&client_config, &usb_host_client_hdl);
    if (err != ESP_OK) {
        usb_host_uninstall();
        usb_del_phy(host_phy_hdl);
        usb_host_installed = false;
        return -1;
    }

    // Start the USB host library task
    usb_host_task_running = true;
    xTaskCreatePinnedToCore(usb_host_lib_task, "usb_host", 4096, NULL, 2, &usb_host_task_handle, 0);

    return 0;
}

static void esp32_usb_host_deinit(void) {
    if (!usb_host_installed) {
        return;
    }

    usb_host_task_running = false;

    if (usb_host_client_hdl != NULL) {
        usb_host_client_deregister(usb_host_client_hdl);
        usb_host_client_hdl = NULL;
    }

    if (usb_host_task_handle != NULL) {
        // Give the task time to exit
        vTaskDelay(pdMS_TO_TICKS(100));
        usb_host_task_handle = NULL;
    }

    usb_host_uninstall();
    usb_del_phy(host_phy_hdl);
    usb_host_installed = false;
    usb_host_dev_addr = 0;
}

static void esp32_usb_host_task(void) {
    if (usb_host_client_hdl != NULL) {
        usb_host_client_handle_events(usb_host_client_hdl, 0);
    }
}

static bool esp32_usb_host_device_connected(void) {
    return usb_host_dev_addr != 0;
}

static int esp32_usb_host_get_device_info(mp_usb_host_dev_info_t *info) {
    if (usb_host_dev_addr == 0) {
        return -1;
    }

    usb_device_handle_t dev_hdl;
    esp_err_t err = usb_host_device_open(usb_host_client_hdl, usb_host_dev_addr, &dev_hdl);
    if (err != ESP_OK) {
        return -1;
    }

    const usb_device_desc_t *dev_desc;
    err = usb_host_get_device_descriptor(dev_hdl, &dev_desc);
    if (err != ESP_OK) {
        usb_host_device_close(usb_host_client_hdl, dev_hdl);
        return -1;
    }

    info->vid = dev_desc->idVendor;
    info->pid = dev_desc->idProduct;
    info->dev_addr = usb_host_dev_addr;

    usb_device_info_t dev_info_raw;
    err = usb_host_device_info(dev_hdl, &dev_info_raw);
    if (err == ESP_OK) {
        info->speed = (dev_info_raw.speed == USB_SPEED_LOW) ? MP_USB_HOST_SPEED_LOW : MP_USB_HOST_SPEED_FULL;
    } else {
        info->speed = MP_USB_HOST_SPEED_FULL;
    }

    // Try to read string descriptors
    info->manufacturer[0] = '\0';
    info->product[0] = '\0';

    usb_host_device_close(usb_host_client_hdl, dev_hdl);
    return 0;
}

static int esp32_usb_host_control_transfer(uint8_t bmRequestType, uint8_t bRequest,
    uint16_t wValue, uint16_t wIndex,
    uint8_t *data, uint16_t length, uint32_t timeout_ms) {

    if (usb_host_dev_addr == 0 || usb_host_client_hdl == NULL) {
        return -1;
    }

    usb_device_handle_t dev_hdl;
    esp_err_t err = usb_host_device_open(usb_host_client_hdl, usb_host_dev_addr, &dev_hdl);
    if (err != ESP_OK) {
        return -1;
    }

    // Allocate transfer with space for SETUP packet + data
    size_t xfer_size = sizeof(usb_setup_packet_t) + length;
    usb_transfer_t *transfer;
    err = usb_host_transfer_alloc(xfer_size, 0, &transfer);
    if (err != ESP_OK) {
        usb_host_device_close(usb_host_client_hdl, dev_hdl);
        return -1;
    }

    // Fill in SETUP packet
    usb_setup_packet_t *setup = (usb_setup_packet_t *)transfer->data_buffer;
    setup->bmRequestType = bmRequestType;
    setup->bRequest = bRequest;
    setup->wValue = wValue;
    setup->wIndex = wIndex;
    setup->wLength = length;

    // For OUT transfers, copy data after SETUP packet
    if (!(bmRequestType & 0x80) && length > 0 && data != NULL) {
        memcpy(transfer->data_buffer + sizeof(usb_setup_packet_t), data, length);
    }

    transfer->num_bytes = xfer_size;
    transfer->device_handle = dev_hdl;
    transfer->bEndpointAddress = 0;
    transfer->timeout_ms = timeout_ms;

    // Use a semaphore to synchronize with the transfer callback
    SemaphoreHandle_t xfer_done = xSemaphoreCreateBinary();
    transfer->context = xfer_done;
    transfer->callback = usb_host_xfer_done_cb;

    err = usb_host_transfer_submit_control(usb_host_client_hdl, transfer);
    if (err != ESP_OK) {
        usb_host_transfer_free(transfer);
        usb_host_device_close(usb_host_client_hdl, dev_hdl);
        vSemaphoreDelete(xfer_done);
        return -1;
    }

    // Wait for completion
    if (xSemaphoreTake(xfer_done, pdMS_TO_TICKS(timeout_ms + 100)) != pdTRUE) {
        usb_host_transfer_free(transfer);
        usb_host_device_close(usb_host_client_hdl, dev_hdl);
        vSemaphoreDelete(xfer_done);
        return -1;
    }
    vSemaphoreDelete(xfer_done);

    int result = -1;
    if (transfer->status == USB_TRANSFER_STATUS_COMPLETED) {
        // For IN transfers, copy data back
        if ((bmRequestType & 0x80) && data != NULL) {
            int actual = transfer->actual_num_bytes - sizeof(usb_setup_packet_t);
            if (actual > 0) {
                if ((uint16_t)actual > length) {
                    actual = length;
                }
                memcpy(data, transfer->data_buffer + sizeof(usb_setup_packet_t), actual);
            }
            result = actual > 0 ? actual : 0;
        } else {
            result = transfer->actual_num_bytes - sizeof(usb_setup_packet_t);
            if (result < 0) {
                result = 0;
            }
        }
    }

    usb_host_transfer_free(transfer);
    usb_host_device_close(usb_host_client_hdl, dev_hdl);
    return result;
}

static int esp32_usb_host_open_endpoint(uint8_t ep_addr, uint8_t ep_type, uint16_t max_pkt_size) {
    // Endpoint management is handled via the ESP-IDF USB host interface
    // claim. In a full implementation this would claim the interface
    // containing the endpoint.
    (void)ep_addr;
    (void)ep_type;
    (void)max_pkt_size;
    return 0;
}

static void esp32_usb_host_close_endpoint(uint8_t ep_addr) {
    (void)ep_addr;
}

// Default timeout for non-control transfers
#define ESP32_USB_HOST_XFER_TIMEOUT_MS 5000

static int esp32_usb_host_submit_xfer(uint8_t ep_addr, uint8_t *buf, uint16_t len) {
    if (usb_host_dev_addr == 0 || usb_host_client_hdl == NULL) {
        return -1;
    }

    usb_device_handle_t dev_hdl;
    esp_err_t err = usb_host_device_open(usb_host_client_hdl, usb_host_dev_addr, &dev_hdl);
    if (err != ESP_OK) {
        return -1;
    }

    usb_transfer_t *transfer;
    err = usb_host_transfer_alloc(len, 0, &transfer);
    if (err != ESP_OK) {
        usb_host_device_close(usb_host_client_hdl, dev_hdl);
        return -1;
    }

    if (!(ep_addr & 0x80)) {
        memcpy(transfer->data_buffer, buf, len);
    }

    transfer->num_bytes = len;
    transfer->device_handle = dev_hdl;
    transfer->bEndpointAddress = ep_addr;
    transfer->timeout_ms = ESP32_USB_HOST_XFER_TIMEOUT_MS;

    // Use a semaphore for synchronous completion. The xfer_cb in the
    // Python layer is scheduled after this returns.
    SemaphoreHandle_t xfer_done = xSemaphoreCreateBinary();
    transfer->context = xfer_done;
    transfer->callback = usb_host_xfer_done_cb;

    err = usb_host_transfer_submit(transfer);
    if (err != ESP_OK) {
        usb_host_transfer_free(transfer);
        usb_host_device_close(usb_host_client_hdl, dev_hdl);
        vSemaphoreDelete(xfer_done);
        return -1;
    }

    // Wait for completion
    bool success = false;
    uint16_t xferred = 0;
    if (xSemaphoreTake(xfer_done, pdMS_TO_TICKS(ESP32_USB_HOST_XFER_TIMEOUT_MS + 100)) == pdTRUE) {
        success = (transfer->status == USB_TRANSFER_STATUS_COMPLETED);
        xferred = transfer->actual_num_bytes;
        if (success && (ep_addr & 0x80) && buf != NULL) {
            // IN transfer: copy received data back
            uint16_t copy_len = (xferred > len) ? len : xferred;
            memcpy(buf, transfer->data_buffer, copy_len);
        }
    }
    vSemaphoreDelete(xfer_done);

    // Notify the Python xfer_cb
    mp_usb_host_xfer_complete_cb(ep_addr, success, xferred);

    usb_host_transfer_free(transfer);
    usb_host_device_close(usb_host_client_hdl, dev_hdl);
    return success ? 0 : -1;
}

static void usb_host_client_event_cb(const usb_host_client_event_msg_t *event_msg, void *arg) {
    switch (event_msg->event) {
        case USB_HOST_CLIENT_EVENT_NEW_DEV:
            usb_host_dev_addr = event_msg->new_dev.address;
            mp_usb_host_device_connect_cb();
            break;
        case USB_HOST_CLIENT_EVENT_DEV_GONE:
            usb_host_dev_addr = 0;
            mp_usb_host_device_disconnect_cb();
            break;
        default:
            break;
    }
}

static void usb_host_lib_task(void *arg) {
    while (usb_host_task_running) {
        usb_host_lib_handle_events(100, NULL);
    }
    vTaskDelete(NULL);
}

// HAL implementation table
static const mp_usb_host_hal_t esp32_usb_host_hal = {
    .init = esp32_usb_host_init,
    .deinit = esp32_usb_host_deinit,
    .task = esp32_usb_host_task,
    .device_connected = esp32_usb_host_device_connected,
    .get_device_info = esp32_usb_host_get_device_info,
    .control_transfer = esp32_usb_host_control_transfer,
    .open_endpoint = esp32_usb_host_open_endpoint,
    .close_endpoint = esp32_usb_host_close_endpoint,
    .submit_xfer = esp32_usb_host_submit_xfer,
};

const mp_usb_host_hal_t *mp_usb_host_get_hal(void) {
    return &esp32_usb_host_hal;
}

#endif // MICROPY_PY_MACHINE_USB_HOST
