include("$(PORT_DIR)/variants/manifest.py")

include("$(MPY_DIR)/extmod/asyncio")

add_library("unix-ffi", "$(MPY_LIB_DIR)/unix-ffi")

# Require some micropython-lib modules.

# not yet included 
# require("debugpy")
