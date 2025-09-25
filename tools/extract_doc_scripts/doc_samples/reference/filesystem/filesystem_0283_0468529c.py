# Source: reference\filesystem.rst:283
# Type: code_block

import vfs, pyb

p2 = pyb.Flash(start=256 * 1024)
vfs.mount(p2, "/data")
