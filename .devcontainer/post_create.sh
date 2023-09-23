sudo DEBIAN_FRONTEND=noninteractive apt update -y

echo "# always load micropython ci.sh" >> ~/.bashrc
echo "source tools/ci.sh" >> ~/.bashrc
echo "To list defined functions type: declare -F |  declare -F| grep ci_.*_build"

# simple menu to setup for build
pip install -U pick
# pre-commit
pip install -U pre-commit
pre-commit install --hook-type pre-commit --hook-type commit-msg

# Use autobuild setup from github actions
source tools/ci.sh

