include("$(PORT_DIR)/variants/manifest.py")

include("$(MPY_DIR)/extmod/asyncio")

freeze_as_mpy("typing")
freeze_as_mpy("typing_extensions")

require("__future__")
require("abc")

# belt and suspenders - collections is already included 
require("collections")

# does not exist yet
# require("collections.abc")