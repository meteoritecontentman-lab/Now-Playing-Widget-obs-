================================================================
  NOW PLAYING BRIDGE  -  Linux
  HOW TO USE IT  (read me first!)
================================================================

WHAT THIS IS
  A tiny program that reads what's currently playing on your Linux
  machine (via MPRIS/playerctl - works with most music players)
  and feeds it to your "Now Playing" overlay in OBS. All data
  stays on your computer - nothing is uploaded anywhere.

WHAT YOU NEED
  - Linux with systemd/DBus (standard on Ubuntu, Fedora, Arch...)
  - playerctl    ->  sudo apt install playerctl   (Debian/Ubuntu)
                      sudo dnf install playerctl   (Fedora)
                      sudo pacman -S playerctl     (Arch)
  - Python 3 with venv (python3-venv on Debian/Ubuntu)

----------------------------------------------------------------
HOW TO START  (repeat each stream)
----------------------------------------------------------------
  1. Unzip this folder.
  2. Open a terminal in this folder and run:
       ./Start\ Bridge.sh
     (If you get "Permission denied":
        chmod +x "Start Bridge.sh"
     then try again.)
  3. The FIRST time it sets itself up automatically.
  4. Keep the terminal window OPEN while you stream.

----------------------------------------------------------------
USING IT IN OBS
----------------------------------------------------------------
  1. Open the Now Playing customizer (the main page / hub).
  2. Pick your colors and options -> click  "Generate link".
  3. OBS:  Sources  ->  +  ->  Browser
  4. Paste the link into the "URL" field.
     Suggested size: 480 x 140.
  5. Click OK. The card appears whenever a track is playing.

----------------------------------------------------------------
TROUBLESHOOTING
----------------------------------------------------------------
  Q: The designer says "Bridge offline".
  A: Make sure the bridge window is OPEN, playerctl is installed,
     and at least one music player is running with media playing.

  Q: No album art shown.
  A: Some players don't expose art over MPRIS. Nothing is wrong -
     a clean placeholder is shown instead.

  Q: "Address already in use".
  A: Another program is using port 8123. Start with a different
     port (and update the widget link accordingly):
        NP_PORT=8124  python server.py

----------------------------------------------------------------
ADVANCED
----------------------------------------------------------------
  Using a different port:
    NP_PORT=8124  python server.py
  (You must also change the port number in the widget link.)

  Privacy: the bridge listens only on 127.0.0.1 (this computer).
  No cloud, no account, no tracking.
================================================================