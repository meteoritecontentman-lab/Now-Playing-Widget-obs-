================================================================
  NOW PLAYING BRIDGE  -  macOS
  HOW TO USE IT  (read me first!)
================================================================

WHAT THIS IS
  A tiny program that reads what's currently playing on your Mac
  (Spotify, Apple Music, YouTube in a browser, etc.) and feeds it
  to your "Now Playing" overlay in OBS. All data stays on your
  computer - nothing is uploaded anywhere.

WHAT YOU NEED
  - macOS (Apple Silicon or Intel)
  - Homebrew   ->  https://brew.sh   (installs once)
  - Python 3   ->  usually already on macOS

----------------------------------------------------------------
HOW TO START  (repeat each stream - takes 5 seconds)
----------------------------------------------------------------
  1. Unzip this folder (double-click the .zip).
  2. RIGHT-click  "Start Bridge.command"  and choose  "Open".
     (First time only - macOS shows "unidentified developer".
      Right-click > Open gets around it. After the first time,
      you can double-click it normally.)
  3. A terminal window opens. The FIRST time it installs a few
     small packages automatically - this takes 1-2 minutes.
  4. When you see "Now Playing Bridge (macOS)" leave the window
     OPEN while you stream.

----------------------------------------------------------------
USING IT IN OBS
----------------------------------------------------------------
  1. Open the Now Playing customizer (the main page / hub).
  2. Pick your colors and options -> click  "Generate link".
  3. OBS:  Sources  ->  +  ->  Browser
  4. Paste the link into the "URL" field.
     Suggested size: 480 x 140.
  5. Click OK. The card appears whenever music/track is playing.

----------------------------------------------------------------
TROUBLESHOOTING
----------------------------------------------------------------
  Q: The designer says "Bridge offline".
  A: The bridge almost certainly couldn't start. The #1 cause is
     the macOS "AirPlay Receiver" keeping the old port 5000 busy.
     Fix: System Settings > General > AirDrop & Handoff >
     turn OFF "AirPlay Receiver", then start the bridge again.
     (This version uses port 8123 to avoid that conflict.)

  Q: This build can't be opened / unidentified developer.
  A: Right-click the .command file and choose Open, then Open
     again in the dialog. You only do this once.

  Q: Nothing shows even though music is playing.
  A: Click "Generate link" again so the widget link matches your
     current setup, and make sure the bridge window is open.

----------------------------------------------------------------
ADVANCED
----------------------------------------------------------------
  Using a different port:
    NP_PORT=8124  python server.py
  (You must also change the port number in the widget link.)

  Privacy: the bridge listens only on 127.0.0.1 (this computer).
  No cloud, no account, no tracking.
================================================================