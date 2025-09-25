# Source: reference\filesystem.rst:265
# Type: code_block

import os, vfs, pyb

vfs.umount("/flash")
p1 = pyb.Flash(start=0, len=256 * 1024)
p2 = pyb.Flash(start=256 * 1024)
vfs.VfsFat.mkfs(p1)
vfs.VfsLfs2.mkfs(p2)
vfs.mount(p1, "/flash")
vfs.mount(p2, "/data")
os.chdir("/flash")
