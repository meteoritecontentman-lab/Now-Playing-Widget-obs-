#!/bin/bash
cd "$(dirname "$0")"

echo "=============================================="
echo "  Now Playing Bridge – macOS"
echo "=============================================="
echo ""

# Check media-control
if ! command -v media-control &> /dev/null; then
  echo "media-control is not installed."
  echo "Installing with Homebrew..."
  if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Install from https://brew.sh then run this again."
    read -p "Press Enter to close..."
    exit 1
  fi
  brew install media-control
fi

# Setup venv if needed
if [ ! -d "venv" ]; then
  echo "First run – setting up (one time)..."
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install flask flask-cors
  echo "Setup complete."
  echo ""
else
  source venv/bin/activate
fi

echo "Starting bridge..."
echo "Leave this window open while you stream."
echo ""
python server.py

read -p "Bridge stopped. Press Enter to close..."
