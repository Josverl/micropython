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

#include "py/mpconfig.h"

#if MICROPY_PY_MACHINE_USB_HOST

#include "py/runtime.h"
#include "py/mperrno.h"
#include "py/objstr.h"
#include "extmod/machine_usb_host.h"

// Implements the singleton runtime USB Host object.
//
// This provides a cross-port Python API for USB host mode. Each port
// must supply a HAL implementation (mp_usb_host_hal_t) via
// mp_usb_host_get_hal().

const mp_obj_type_t machine_usb_host_type;

static mp_obj_t usb_host_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    (void)type;
    mp_arg_check_num(n_args, n_kw, 0, 0, false);

    if (MP_STATE_VM(usbh) == MP_OBJ_NULL) {
        mp_obj_usb_host_t *o = m_new_obj(mp_obj_usb_host_t);
        o->base.type = &machine_usb_host_type;
        o->connect_cb = mp_const_none;
        o->disconnect_cb = mp_const_none;
        o->xfer_cb = mp_const_none;
        o->active = false;
        o->device_present = false;
        o->hal = mp_usb_host_get_hal();

        MP_STATE_VM(usbh) = MP_OBJ_FROM_PTR(o);
    }

    return MP_STATE_VM(usbh);
}

// Helper to get the singleton and check it is active.
static mp_obj_usb_host_t *usb_host_get_active(mp_obj_t self_in) {
    mp_obj_usb_host_t *self = MP_OBJ_TO_PTR(self_in);
    if (!self->active) {
        mp_raise_OSError(MP_EINVAL);
    }
    return self;
}

// USBHost.config(*, connect_cb=None, disconnect_cb=None, xfer_cb=None)
static mp_obj_t usb_host_config(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    mp_obj_usb_host_t *self = MP_OBJ_TO_PTR(pos_args[0]);

    enum { ARG_connect_cb, ARG_disconnect_cb, ARG_xfer_cb };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_connect_cb, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_disconnect_cb, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_xfer_cb, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (args[ARG_connect_cb].u_obj != MP_OBJ_NULL) {
        self->connect_cb = args[ARG_connect_cb].u_obj;
    }
    if (args[ARG_disconnect_cb].u_obj != MP_OBJ_NULL) {
        self->disconnect_cb = args[ARG_disconnect_cb].u_obj;
    }
    if (args[ARG_xfer_cb].u_obj != MP_OBJ_NULL) {
        self->xfer_cb = args[ARG_xfer_cb].u_obj;
    }

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(usb_host_config_obj, 1, usb_host_config);

// USBHost.active([value])
static mp_obj_t usb_host_active(size_t n_args, const mp_obj_t *args) {
    mp_obj_usb_host_t *self = MP_OBJ_TO_PTR(args[0]);

    bool result = self->active;
    if (n_args == 2) {
        bool value = mp_obj_is_true(args[1]);

        if (value && !result) {
            // Activating host mode
            if (self->hal == NULL || self->hal->init == NULL) {
                mp_raise_OSError(MP_ENODEV);
            }

            int ret = self->hal->init();
            if (ret != 0) {
                mp_raise_OSError(MP_EIO);
            }
            self->active = true;
        } else if (!value && result) {
            // Deactivating host mode
            if (self->hal != NULL && self->hal->deinit != NULL) {
                self->hal->deinit();
            }
            self->active = false;
            self->device_present = false;
        }
    }

    return mp_obj_new_bool(result);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(usb_host_active_obj, 1, 2, usb_host_active);

// USBHost.info()
// Returns a dict with device information, or None if no device is connected.
static mp_obj_t usb_host_info(mp_obj_t self_in) {
    mp_obj_usb_host_t *self = usb_host_get_active(self_in);

    if (self->hal == NULL || self->hal->device_connected == NULL || !self->hal->device_connected()) {
        return mp_const_none;
    }

    mp_usb_host_dev_info_t info;
    if (self->hal->get_device_info(&info) != 0) {
        return mp_const_none;
    }

    mp_obj_t dict = mp_obj_new_dict(5);

    mp_obj_dict_store(dict, MP_OBJ_NEW_QSTR(MP_QSTR_vid), mp_obj_new_int(info.vid));
    mp_obj_dict_store(dict, MP_OBJ_NEW_QSTR(MP_QSTR_pid), mp_obj_new_int(info.pid));

    const char *speed_str = (info.speed == MP_USB_HOST_SPEED_LOW) ? "LS" : "FS";
    mp_obj_dict_store(dict, MP_OBJ_NEW_QSTR(MP_QSTR_speed), mp_obj_new_str(speed_str, strlen(speed_str)));

    mp_obj_dict_store(dict, MP_OBJ_NEW_QSTR(MP_QSTR_manufacturer),
        mp_obj_new_str(info.manufacturer, strlen(info.manufacturer)));
    mp_obj_dict_store(dict, MP_OBJ_NEW_QSTR(MP_QSTR_product),
        mp_obj_new_str(info.product, strlen(info.product)));

    return dict;
}
static MP_DEFINE_CONST_FUN_OBJ_1(usb_host_info_obj, usb_host_info);

// USBHost.control_transfer(bmRequestType, bRequest, wValue, wIndex, data_or_length, *, timeout=5000)
static mp_obj_t usb_host_control_transfer(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    mp_obj_usb_host_t *self = usb_host_get_active(pos_args[0]);

    enum { ARG_bmRequestType, ARG_bRequest, ARG_wValue, ARG_wIndex, ARG_data_or_length, ARG_timeout };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_bmRequestType, MP_ARG_REQUIRED | MP_ARG_INT },
        { MP_QSTR_bRequest, MP_ARG_REQUIRED | MP_ARG_INT },
        { MP_QSTR_wValue, MP_ARG_REQUIRED | MP_ARG_INT },
        { MP_QSTR_wIndex, MP_ARG_REQUIRED | MP_ARG_INT },
        { MP_QSTR_data_or_length, MP_ARG_REQUIRED | MP_ARG_OBJ },
        { MP_QSTR_timeout, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 5000} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    uint8_t bmRequestType = args[ARG_bmRequestType].u_int;
    uint8_t bRequest = args[ARG_bRequest].u_int;
    uint16_t wValue = args[ARG_wValue].u_int;
    uint16_t wIndex = args[ARG_wIndex].u_int;
    uint32_t timeout = args[ARG_timeout].u_int;

    if (self->hal == NULL || self->hal->control_transfer == NULL) {
        mp_raise_OSError(MP_ENODEV);
    }

    mp_obj_t data_or_length = args[ARG_data_or_length].u_obj;

    if (mp_obj_is_int(data_or_length)) {
        // IN transfer: data_or_length is the max number of bytes to read
        uint16_t length = mp_obj_get_int(data_or_length);
        uint8_t *buf = m_new(uint8_t, length);

        int ret = self->hal->control_transfer(bmRequestType, bRequest,
            wValue, wIndex, buf, length, timeout);

        if (ret < 0) {
            m_del(uint8_t, buf, length);
            mp_raise_OSError(MP_EIO);
        }

        mp_obj_t result = mp_obj_new_bytes(buf, ret);
        m_del(uint8_t, buf, length);
        return result;
    } else {
        // OUT transfer: data_or_length is the data to send
        mp_buffer_info_t buf_info;
        mp_get_buffer_raise(data_or_length, &buf_info, MP_BUFFER_READ);

        int ret = self->hal->control_transfer(bmRequestType, bRequest,
            wValue, wIndex, buf_info.buf, buf_info.len, timeout);

        if (ret < 0) {
            mp_raise_OSError(MP_EIO);
        }

        return mp_obj_new_int(ret);
    }
}
static MP_DEFINE_CONST_FUN_OBJ_KW(usb_host_control_transfer_obj, 1, usb_host_control_transfer);

// USBHost.open_endpoint(ep_addr, ep_type, max_pkt_size)
static mp_obj_t usb_host_open_endpoint(size_t n_args, const mp_obj_t *args) {
    mp_obj_usb_host_t *self = usb_host_get_active(args[0]);

    uint8_t ep_addr = mp_obj_get_int(args[1]);
    uint8_t ep_type = mp_obj_get_int(args[2]);
    uint16_t max_pkt_size = mp_obj_get_int(args[3]);

    if (self->hal == NULL || self->hal->open_endpoint == NULL) {
        mp_raise_OSError(MP_ENODEV);
    }

    int ret = self->hal->open_endpoint(ep_addr, ep_type, max_pkt_size);
    if (ret != 0) {
        mp_raise_OSError(MP_EIO);
    }

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(usb_host_open_endpoint_obj, 4, 4, usb_host_open_endpoint);

// USBHost.close_endpoint(ep_addr)
static mp_obj_t usb_host_close_endpoint(mp_obj_t self_in, mp_obj_t ep_in) {
    mp_obj_usb_host_t *self = usb_host_get_active(self_in);

    uint8_t ep_addr = mp_obj_get_int(ep_in);

    if (self->hal != NULL && self->hal->close_endpoint != NULL) {
        self->hal->close_endpoint(ep_addr);
    }

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(usb_host_close_endpoint_obj, usb_host_close_endpoint);

// USBHost.submit_xfer(ep_addr, buffer)
static mp_obj_t usb_host_submit_xfer(mp_obj_t self_in, mp_obj_t ep_in, mp_obj_t buffer_in) {
    mp_obj_usb_host_t *self = usb_host_get_active(self_in);

    uint8_t ep_addr = mp_obj_get_int(ep_in);

    mp_buffer_info_t buf_info;
    // IN endpoints need a writable buffer, OUT endpoints need readable
    if (ep_addr & 0x80) {
        mp_get_buffer_raise(buffer_in, &buf_info, MP_BUFFER_RW);
    } else {
        mp_get_buffer_raise(buffer_in, &buf_info, MP_BUFFER_READ);
    }

    if (self->hal == NULL || self->hal->submit_xfer == NULL) {
        mp_raise_OSError(MP_ENODEV);
    }

    int ret = self->hal->submit_xfer(ep_addr, buf_info.buf, buf_info.len);
    if (ret != 0) {
        mp_raise_OSError(MP_EIO);
    }

    return mp_obj_new_bool(true);
}
static MP_DEFINE_CONST_FUN_OBJ_3(usb_host_submit_xfer_obj, usb_host_submit_xfer);

// Method table
static const mp_rom_map_elem_t usb_host_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_config), MP_ROM_PTR(&usb_host_config_obj) },
    { MP_ROM_QSTR(MP_QSTR_active), MP_ROM_PTR(&usb_host_active_obj) },
    { MP_ROM_QSTR(MP_QSTR_info), MP_ROM_PTR(&usb_host_info_obj) },
    { MP_ROM_QSTR(MP_QSTR_control_transfer), MP_ROM_PTR(&usb_host_control_transfer_obj) },
    { MP_ROM_QSTR(MP_QSTR_open_endpoint), MP_ROM_PTR(&usb_host_open_endpoint_obj) },
    { MP_ROM_QSTR(MP_QSTR_close_endpoint), MP_ROM_PTR(&usb_host_close_endpoint_obj) },
    { MP_ROM_QSTR(MP_QSTR_submit_xfer), MP_ROM_PTR(&usb_host_submit_xfer_obj) },

    // Transfer type constants
    { MP_ROM_QSTR(MP_QSTR_XFER_CONTROL), MP_ROM_INT(MP_USB_HOST_XFER_CONTROL) },
    { MP_ROM_QSTR(MP_QSTR_XFER_ISOCHRONOUS), MP_ROM_INT(MP_USB_HOST_XFER_ISOCHRONOUS) },
    { MP_ROM_QSTR(MP_QSTR_XFER_BULK), MP_ROM_INT(MP_USB_HOST_XFER_BULK) },
    { MP_ROM_QSTR(MP_QSTR_XFER_INTERRUPT), MP_ROM_INT(MP_USB_HOST_XFER_INTERRUPT) },
};
static MP_DEFINE_CONST_DICT(usb_host_locals_dict, usb_host_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    machine_usb_host_type,
    MP_QSTR_USBHost,
    MP_TYPE_FLAG_NONE,
    make_new, usb_host_make_new,
    locals_dict, &usb_host_locals_dict
    );

MP_REGISTER_ROOT_POINTER(mp_obj_t usbh);

// Callbacks invoked by port HAL code

void mp_usb_host_device_connect_cb(void) {
    if (MP_STATE_VM(usbh) == MP_OBJ_NULL) {
        return;
    }
    mp_obj_usb_host_t *self = MP_OBJ_TO_PTR(MP_STATE_VM(usbh));
    self->device_present = true;

    if (self->connect_cb != mp_const_none) {
        mp_sched_schedule(self->connect_cb, MP_STATE_VM(usbh));
    }
}

void mp_usb_host_device_disconnect_cb(void) {
    if (MP_STATE_VM(usbh) == MP_OBJ_NULL) {
        return;
    }
    mp_obj_usb_host_t *self = MP_OBJ_TO_PTR(MP_STATE_VM(usbh));
    self->device_present = false;

    if (self->disconnect_cb != mp_const_none) {
        mp_sched_schedule(self->disconnect_cb, MP_STATE_VM(usbh));
    }
}

void mp_usb_host_xfer_complete_cb(uint8_t ep_addr, bool result, uint16_t xferred_bytes) {
    if (MP_STATE_VM(usbh) == MP_OBJ_NULL) {
        return;
    }
    mp_obj_usb_host_t *self = MP_OBJ_TO_PTR(MP_STATE_VM(usbh));

    if (self->xfer_cb != mp_const_none) {
        mp_obj_t cb_args[3] = {
            mp_obj_new_int(ep_addr),
            mp_obj_new_bool(result),
            mp_obj_new_int(xferred_bytes),
        };
        // Use tuple to pass multiple args via mp_sched_schedule
        mp_sched_schedule(self->xfer_cb, mp_obj_new_tuple(3, cb_args));
    }
}

#endif // MICROPY_PY_MACHINE_USB_HOST
