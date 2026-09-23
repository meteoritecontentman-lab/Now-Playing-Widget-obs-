================================================================
  NOW PLAYING BRIDGE  -  Windows
  HOW TO USE IT  (read me first!)
================================================================

WHAT THIS IS
  A tiny program that reads what's currently playing on your PC
  (via Windows System Media Transport Controls - works with
  Spotify, Chrome/Edge, VLC, etc.) and feeds it to your
  "Now Playing" overlay in OBS. All data stays on your computer -
  nothing is uploaded anywhere.

WHAT YOU NEED
  - Windows 10 or Windows 11
  - Python 3 from https://python.org
    IMPORTANT: during install, tick  "Add Python to PATH".

----------------------------------------------------------------
HOW TO START  (repeat each stream)
----------------------------------------------------------------
  1. Unzip this folder.
  2. Double-click  "Start Bridge.bat".
     (SmartScreen may ask: click "More info" -> "Run anyway".)
  3. The FIRST time it installs a few small packages
     automatically - this takes 1-2 minutes.
  4. Leave the terminal window OPEN while you stream.

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
  Q: "Python was not found".
  A: Python isn't installed or wasn't added to PATH.
     Reinstall from https://python.org and tick
     "Add Python to PATH".

  Q: The designer says "Bridge offline".
  A: Make sure the bridge window is open and that something is
     actually playing (Spotify, Edge, VLC...). Some apps only
     report media while actively playing.

  Q: "Address already in use".
  A: Another program is using port 8123. Start with a different
     port (and update the widget link accordingly):
        set NP_PORT=8124
        python server.py

----------------------------------------------------------------
ADVANCED
----------------------------------------------------------------
  Using a different port:
    set NP_PORT=8124
    python server.py
  (You must also change the port number in the widget link.)

  Note: album art is supported through the system API on most
  apps. If a source doesn't provide it, a clean placeholder is
  shown instead.

  Privacy: the bridge listens only on 127.0.0.1 (this computer).
  No cloud, no account, no tracking.
================================================================