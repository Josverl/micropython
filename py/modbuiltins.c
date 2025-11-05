/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2013, 2014 Damien P. George
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

#include <stdio.h>
#include <assert.h>

#include "py/smallint.h"
#include "py/objint.h"
#include "py/objstr.h"
#include "py/objtype.h"
#include "py/runtime.h"
#include "py/builtin.h"
#include "py/stream.h"

#if MICROPY_PY_BUILTINS_FLOAT
#include <math.h>
#endif

#if MICROPY_PY_IO
extern struct _mp_dummy_t mp_sys_stdout_obj; // type is irrelevant, just need pointer
#endif

// args[0] is function from class body
// args[1] is class name
// args[2:] are base objects
#if MICROPY_METACLASS || MICROPY_INIT_SUBCLASS
// Keyword arguments may include 'metaclass'
static mp_obj_t mp_builtin___build_class__(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
#else
static mp_obj_t mp_builtin___build_class__(size_t n_args, const mp_obj_t *args) {
