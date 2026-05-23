include("$(PORT_DIR)/variants/manifest.py")

include("$(MPY_DIR)/extmod/asyncio")

freeze_as_mpy("typing")

require("__future__")

# belt and suspenders - collections is already included 
require("collections")

# does not exist yet
# require("collections.abc")