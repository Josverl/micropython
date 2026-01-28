# FAT VFS Unicode Error Handling Fix

## Problem Description

Users reported encountering confusing `UnicodeError` exceptions when accessing files on FAT filesystems with corrupted directory entries. For example:

```python
>>> import os
>>> os.listdir('/sd')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeError: 
```

The actual issue was filesystem corruption, but the error message didn't make this clear. The corruption resulted in invalid UTF-8 byte sequences in filenames (e.g., `b"Fr\x81hst\x81ck.wav"` instead of valid UTF-8 like `b"Fr\xc3\xbchst\xc3\xbcck.wav"`).

## Root Cause

1. **FAT Filesystem Encoding**: The FatFS library (oofatfs) with `FF_LFN_UNICODE=0` uses ANSI/OEM encoding (typically CP437) for filenames
2. **UTF-8 Expectation**: MicroPython expects all string objects to contain valid UTF-8
3. **Corruption Impact**: When FAT directory entries are corrupted, the resulting byte sequences may not be valid UTF-8
4. **Error Propagation**: The `mp_obj_new_str_from_cstr()` function validates UTF-8 and raises `UnicodeError` for invalid sequences

This led to a misleading error message - users thought they had an encoding problem when they actually had filesystem corruption.

## Solution

Modified `extmod/vfs_fat.c` to proactively check for invalid UTF-8 in filenames before attempting to create string objects:

1. Added UTF-8 validation using `utf8_check()` function
2. When invalid UTF-8 is detected, raise `OSError` with errno `EIO` (I/O error) instead
3. Applied the fix to:
   - `mp_vfs_fat_ilistdir_it_iternext()`: Directory listing operations
   - `fat_vfs_getcwd()`: Get current working directory operations

## Changes Made

### extmod/vfs_fat.c

```c
// Added include for UTF-8 validation
#include "py/unicode.h"

// In mp_vfs_fat_ilistdir_it_iternext():
if (self->is_str) {
    // Check if the filename from the FAT filesystem is valid UTF-8
    // Invalid UTF-8 indicates filesystem corruption
    size_t fn_len = strlen(fn);
    if (!utf8_check((const byte *)fn, fn_len)) {
        // Filesystem corruption detected - raise OSError with EIO (I/O error)
        mp_raise_OSError(MP_EIO);
    }
    t->items[0] = mp_obj_new_str_from_cstr(fn);
}

// Similar change in fat_vfs_getcwd()
```

## User Impact

**Before the fix:**
```python
>>> import os
>>> os.listdir('/sd')  # On corrupted filesystem
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeError: 
```

**After the fix:**
```python
>>> import os
>>> os.listdir('/sd')  # On corrupted filesystem
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: [Errno 5] EIO
```

The `OSError` with `EIO` (I/O error) clearly indicates a hardware or filesystem issue, guiding users to:
1. Check the physical media (SD card, flash storage)
2. Run filesystem check/repair tools
3. Backup data and reformat if necessary

## Testing

- All existing FAT VFS tests pass (13 tests, 117 individual test cases)
- No regression in extmod tests (180 tests passed)
- The fix only affects string listings; byte listings continue to work even with invalid UTF-8

## Related Issues

This fix addresses reports from users experiencing:
- Files with non-ASCII names showing corrupted on FAT filesystems
- Inability to list directories after filesystem corruption
- Confusing UnicodeError messages when the real issue was hardware/filesystem corruption

## Future Considerations

1. **Enhanced Error Messages**: Could include more specific corruption details
2. **Recovery Options**: Could attempt to sanitize filenames for read-only access
3. **Logging**: Could add debug logging to help diagnose filesystem issues
4. **Configuration**: Future option to use UTF-8 encoding (FF_LFN_UNICODE=2) instead of ANSI/OEM

## References

- FatFS (oofatfs) documentation: `lib/oofatfs/ff.h`
- Unicode validation: `py/unicode.c`
- Error codes: `py/mperrno.h`
- VFS implementation: `extmod/vfs_fat.c`
