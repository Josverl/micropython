sudo DEBIAN_FRONTEND=noninteractive apt update -y
# Use autobuild setup from github actions
source tools/ci.sh

declare -F| grep ci_.*_setup

echo "To list defined functions type: declare -F |  declare -F| grep ci_.*_build"

