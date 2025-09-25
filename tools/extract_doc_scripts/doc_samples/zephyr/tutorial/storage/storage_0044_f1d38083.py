# Source: zephyr\tutorial\storage.rst:44
# Type: code_block

import vfs
from zephyr import FlashArea

bdev = FlashArea(FlashArea.STORAGE, 4096)  # create block device object using FlashArea
vfs.VfsLfs2.mkfs(bdev)  # create Little filesystem object using the flash area block
vfs.mount(bdev, "/flash")  # mount the filesystem at the flash storage subdirectory
with open("/flash/hello.txt", "w") as f:  # open a new file in the directory
    f.write("Hello world")  # write to the file
print(open("/flash/hello.txt").read())  # print contents of the file
