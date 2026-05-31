TYPE_CHECKING = False
if TYPE_CHECKING:
    from manifestfile import *

include("$(PORT_DIR)/variants/manifest.py")

include("$(MPY_DIR)/extmod/asyncio")

# to reduce code size:
#  - default optimization level is 3
#  - extensions are disabled by default
require("bundle-typing", extensions=False)

# BEST SO FAR:
# freeze_as_str("$(MPY_LIB_DIR)/python-stdlib/__future__")

#require("typing", opt_level=3) # 2_112
# require("__future__", opt_level=3) # 664
# require("future", opt_level=3) # 664
# module( "__future__.py", "$(MPY_LIB_DIR)/python-stdlib/__future__", opt=3) # 608 bytes
# freeze_as_mpy("$(MPY_LIB_DIR)/python-stdlib/__future__", script = "__future__.py", opt=3) # 608 bytes