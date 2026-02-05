#!/bin/bash
# Installation and setup script for MicroPython Skill Builder

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                   MicroPython C Code Review Skill Builder                    ║"
echo "║                          Setup and Installation                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "[1/4] Checking Python version..."
python3 --version
python3_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
required_version="3.7"

if (( $(echo "$python3_version < $required_version" | bc -l) )); then
    echo "❌ Error: Python 3.7+ required (found $python3_version)"
    exit 1
fi
echo "✓ Python $python3_version installed"
echo ""

# Install dependencies
echo "[2/4] Installing dependencies..."
if pip install -q -r "$SCRIPT_DIR/requirements.txt"; then
    echo "✓ Dependencies installed"
else
    echo "❌ Error installing dependencies"
    exit 1
fi
echo ""

# Create data directory
echo "[3/4] Creating data directory..."
mkdir -p "$SCRIPT_DIR/data"
echo "✓ Data directory created at $SCRIPT_DIR/data"
echo ""

# Make scripts executable
echo "[4/4] Making scripts executable..."
chmod +x "$SCRIPT_DIR"/*.py
echo "✓ Scripts are executable"
echo ""

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                          Setup Complete!                                    ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

echo "Next steps:"
echo ""
echo "1. Set your GitHub token (optional but recommended):"
echo "   export GITHUB_TOKEN=your_github_token"
echo ""
echo "2. Run the skill builder:"
echo "   python3 $SCRIPT_DIR/main.py --all"
echo ""
echo "3. Or use the interactive setup:"
echo "   python3 $SCRIPT_DIR/quickstart.py"
echo ""
echo "For more information, see README.md"
