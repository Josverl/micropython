# Source: reference\filesystem.rst:160
# Type: code_block

with open("/ramdisk/hello.txt", "w") as f:
    f.write("Hello world")
print(open("/ramdisk/hello.txt").read())
