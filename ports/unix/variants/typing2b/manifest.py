include("$(PORT_DIR)/variants/manifest.py")

include("$(MPY_DIR)/extmod/asyncio")

require("collections", opt_level=3)
# to reduce code size:
#  - default optimization level is 3
#  - extensions are disabled by default
require("bundle-typing", extensions=True)
