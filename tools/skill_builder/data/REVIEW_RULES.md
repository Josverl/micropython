# MicroPython C Code Review Rules

This document describes the automated code review rules for MicroPython C code.
These rules were derived from analysis of ~100 commits and PRs from core MicroPython
contributors.

## Rule Summary

| ID | Category | Severity | Title |
|----|----------|----------|-------|
| `micropy-memory-allocation` | memory_safety | **ERROR** | Use MicroPython memory allocation functions |
| `micropy-error-handling` | error_handling | **WARNING** | Use mp_raise_* functions for exceptions |
| `micropy-error-text-macro` | error_handling | **WARNING** | Use MP_ERROR_TEXT for error messages |
| `micropy-config-guard` | configuration | **SUGGESTION** | Consider using configuration guards for optional features |
| `micropy-type-safety` | type_safety | **WARNING** | Use MicroPython type definitions |
| `micropy-encapsulation` | code_style | **SUGGESTION** | Use static and const for encapsulation |
| `micropy-inline-docs` | documentation | **SUGGESTION** | Add inline comments for non-obvious code |
| `micropy-boundary-check` | memory_safety | **ERROR** | Validate buffer boundaries and sizes |
| `micropy-mp-obj-new` | api_usage | **SUGGESTION** | Use mp_obj_new_* helpers |
| `micropy-qstr-usage` | memory_safety | **SUGGESTION** | Prefer qstr for interned strings |
| `micropy-mp-arg` | api_usage | **SUGGESTION** | Use mp_arg_* for argument parsing |
| `micropy-mp-stream` | io | **SUGGESTION** | Use mp_stream_* for stream protocol |
| `micropy-rom-table` | memory_safety | **SUGGESTION** | Use MP_ROM_PTR/MP_ROM_QSTR for ROM tables |
| `micropy-mp-printf` | logging | **SUGGESTION** | Use mp_printf for diagnostics |
| `micropy-const-fun-obj` | api_binding | **WARNING** | Use MP_DEFINE_CONST_FUN_OBJ_* for function bindings |
| `micropy-vstr-usage` | memory_safety | **SUGGESTION** | Use vstr for dynamic string building |
| `micropy-auto-type-safety` | auto | **SUGGESTION** | Review pattern: type safety |
| `micropy-auto-inline-comments` | auto | **SUGGESTION** | Review pattern: inline comments |
| `micropy-auto-encapsulation` | auto | **SUGGESTION** | Review pattern: encapsulation |
| `micropy-auto-config-guard` | auto | **SUGGESTION** | Review pattern: config guard |
| `micropy-auto-boundary-check` | auto | **SUGGESTION** | Review pattern: boundary check |
| `micropy-auto-error-handling` | auto | **SUGGESTION** | Review pattern: error handling |
| `micropy-auto-error-text-macro` | auto | **SUGGESTION** | Review pattern: error text macro |
| `micropy-auto-memory-allocation` | auto | **SUGGESTION** | Review pattern: memory allocation |

## Detailed Rules

### micropy-memory-allocation

**Category:** memory_safety  
**Severity:** ERROR  

Use m_new, m_renew, and m_del for memory management instead of malloc/free. This ensures consistent memory tracking and debugging.

**Examples:**

❌ **Bad:**
```c
void *ptr = malloc(size);
```

✅ **Good:**
```c
mp_obj_t *ptr = m_new(mp_obj_t, size);
```

### micropy-error-handling

**Category:** error_handling  
**Severity:** WARNING  

Raise MicroPython exceptions using mp_raise_* functions with proper error types. This ensures consistent exception handling across the codebase.

**Examples:**

❌ **Bad:**
```c
if (!valid) assert(0);
```

✅ **Good:**
```c
if (!valid) mp_raise_ValueError(MP_ERROR_TEXT("invalid value"));
```

### micropy-error-text-macro

**Category:** error_handling  
**Severity:** WARNING  

Wrap error message strings with MP_ERROR_TEXT macro for proper handling of compile-time error text storage.

**Examples:**

❌ **Bad:**
```c
mp_raise_ValueError("invalid");
```

✅ **Good:**
```c
mp_raise_ValueError(MP_ERROR_TEXT("invalid"));
```

### micropy-config-guard

**Category:** configuration  
**Severity:** SUGGESTION  

Use #if MICROPY_* preprocessor guards for optional features to reduce binary size on constrained devices.

**Examples:**


### micropy-type-safety

**Category:** type_safety  
**Severity:** WARNING  

Use mp_obj_t, mp_int_t, size_t, and other MicroPython types for consistency and portability across platforms.

**Examples:**

❌ **Bad:**
```c
void process(int *data, int len) {}
```

✅ **Good:**
```c
void process(mp_obj_t *data, size_t len) {}
```

### micropy-encapsulation

**Category:** code_style  
**Severity:** SUGGESTION  

Mark internal functions and data as static, and use const for immutable data to reduce namespace pollution and enable optimization.


### micropy-inline-docs

**Category:** documentation  
**Severity:** SUGGESTION  

Include comments explaining intent for complex logic, memory optimizations, and MicroPython-specific decisions.


### micropy-boundary-check

**Category:** memory_safety  
**Severity:** ERROR  

Always validate array bounds and buffer sizes to prevent buffer overflows on embedded systems with limited memory.


### micropy-mp-obj-new

**Category:** api_usage  
**Severity:** SUGGESTION  

Create MicroPython objects using mp_obj_new_* helpers for consistent object construction.

**Examples:**


### micropy-qstr-usage

**Category:** memory_safety  
**Severity:** SUGGESTION  

Use qstr (MP_QSTR_*) for interned strings to save memory and enable fast comparisons.

**Examples:**


### micropy-mp-arg

**Category:** api_usage  
**Severity:** SUGGESTION  

Use mp_arg_* helpers for consistent argument parsing and validation.

**Examples:**


### micropy-mp-stream

**Category:** io  
**Severity:** SUGGESTION  

Use mp_stream_* helpers to implement stream protocol consistently across ports.

**Examples:**


### micropy-rom-table

**Category:** memory_safety  
**Severity:** SUGGESTION  

Store constant pointers and qstrs in ROM with MP_ROM_PTR/MP_ROM_QSTR to reduce RAM usage.

**Examples:**


### micropy-mp-printf

**Category:** logging  
**Severity:** SUGGESTION  

Prefer mp_printf/mp_vprintf for diagnostic output to integrate with MicroPython's print backend.

**Examples:**


### micropy-const-fun-obj

**Category:** api_binding  
**Severity:** WARNING  

Expose C functions to Python using MP_DEFINE_CONST_FUN_OBJ_* macros for consistent bindings.

**Examples:**


### micropy-vstr-usage

**Category:** memory_safety  
**Severity:** SUGGESTION  

Use vstr_* helpers for incremental string construction to avoid repeated reallocations.

**Examples:**


### micropy-auto-type-safety

**Category:** auto  
**Severity:** SUGGESTION  

This rule was auto-generated from observed code patterns. Review usage for consistency with MicroPython practices.


### micropy-auto-inline-comments

**Category:** auto  
**Severity:** SUGGESTION  

This rule was auto-generated from observed code patterns. Review usage for consistency with MicroPython practices.


### micropy-auto-encapsulation

**Category:** auto  
**Severity:** SUGGESTION  

This rule was auto-generated from observed code patterns. Review usage for consistency with MicroPython practices.


### micropy-auto-config-guard

**Category:** auto  
**Severity:** SUGGESTION  

This rule was auto-generated from observed code patterns. Review usage for consistency with MicroPython practices.

**Examples:**


### micropy-auto-boundary-check

**Category:** auto  
**Severity:** SUGGESTION  

This rule was auto-generated from observed code patterns. Review usage for consistency with MicroPython practices.


### micropy-auto-error-handling

**Category:** auto  
**Severity:** SUGGESTION  

This rule was auto-generated from observed code patterns. Review usage for consistency with MicroPython practices.

**Examples:**


### micropy-auto-error-text-macro

**Category:** auto  
**Severity:** SUGGESTION  

This rule was auto-generated from observed code patterns. Review usage for consistency with MicroPython practices.

**Examples:**


### micropy-auto-memory-allocation

**Category:** auto  
**Severity:** SUGGESTION  

This rule was auto-generated from observed code patterns. Review usage for consistency with MicroPython practices.

**Examples:**

