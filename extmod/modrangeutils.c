/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2023 Damien P. George
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
#include "py/objrange.h"

mp_obj_t mp_range_index(mp_obj_t range_in, mp_obj_t value_in) {
    mp_obj_range_t *range = MP_OBJ_TO_PTR(range_in);
    mp_int_t value = mp_obj_get_int(value_in);

    mp_int_t start = range->start;
    mp_int_t stop = range->stop;
    mp_int_t step = range->step;

    if (step > 0) {
        if (value < start || value >= stop) {
            mp_raise_ValueError(MP_ERROR_TEXT("value not in range"));
        }
    } else {
        if (value > start || value <= stop) {
            mp_raise_ValueError(MP_ERROR_TEXT("value not in range"));
        }
    }

    mp_int_t index = (value - start) / step;
    if (start + index * step != value) {
        mp_raise_ValueError(MP_ERROR_TEXT("value not in range"));
    }

    return MP_OBJ_NEW_SMALL_INT(index);
}
