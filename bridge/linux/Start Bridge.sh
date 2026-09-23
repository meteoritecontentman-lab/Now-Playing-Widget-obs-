#!/bin/bash
cd "$(dirname "$0")"

echo "=============================================="
echo "  Now Playing Bridge – Linux"
echo "=============================================="
echo ""

if ! command -v playerctl &> /dev/null; then
  echo "playerctl is required."
  echo "  Debian/Ubuntu: sudo apt install playerctl"
  echo "  Fedora:        sudo dnf install playerctl"
  echo "  Arch:          sudo pacman -S playerctl"
  read -p "Press Enter to close..."
  exit 1
fi

if [ ! -d "venv" ]; then
  echo "First run – setting up..."
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install flask flask-cors
  echo "Setup complete."
  echo ""
else
  source venv/bin/activate
fi

echo "Starting bridge... Leave this window open while streaming."
echo ""
python server.py
