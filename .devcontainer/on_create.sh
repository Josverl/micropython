sudo DEBIAN_FRONTEND=noninteractive apt update -y

echo "# always load micropython ci.sh" >> ~/.bashrc
echo "source tools/ci.sh" >> ~/.bashrc

# simple menu to setup for build
pip install pick
python3 .devcontainer/setup_picker.py



# Use autobuild setup from github actions
source tools/ci.sh
declare -F| grep ci_.*_build
echo "To list defined functions type: declare -F |  declare -F| grep ci_.*_build"

