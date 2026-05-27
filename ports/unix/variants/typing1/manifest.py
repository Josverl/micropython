include("$(PORT_DIR)/variants/manifest.py")

include("$(MPY_DIR)/extmod/asyncio")

freeze_as_mpy("typing", opt=3)
freeze_as_mpy("typing_extensions", opt=3)

require("__future__", opt_level=3)
require("abc", opt_level=3)

# belt and suspenders - collections is already included 
require("collections", opt_level=3)

# does not exist yet
# require("collections.abc")