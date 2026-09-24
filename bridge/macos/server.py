#!/usr/bin/env python3
"""
Now Playing Bridge – macOS
Reads system Now Playing and serves it to the widget.
"""

import json
import os
import subprocess
from datetime import datetime, timezone
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# Port note: we do NOT use 5000. On macOS the AirPlay Receiver
# (ControlCenter) hijacks port 5000, which crashed the old bridge.
# Default: 8123. Override with: NP_PORT=8124  python server.py
PORT = int(os.environ.get("NP_PORT", "8123"))

app = Flask(__name__, static_folder=".")
CORS(app)


def run_media_control(*args) -> str:
    try:
        result = subprocess.run(
            ["media-control", *args],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return ""
        return result.stdout.strip()
    except FileNotFoundError:
        print("ERROR: media-control not found. Install with: brew install media-control")
        return ""
    except Exception as e:
        print("media-control error:", e)
        return ""


def real_position_ms(data: dict) -> int:
    """media-control returns coarse, frozen positions: some apps (e.g.
    Nuclear) only set Now Playing info ONCE at track start and never update
    elapsedTime, while others update in chunks every few seconds. The
    `timestamp` field is when the app last updated its info, so while
    playback is active we reconstruct the true position from the wall clock:

        real = elapsedTime + (now - timestamp) * playbackRate

    This turns frozen/chunky sources into a smooth, real-time position.
    Falls back to the raw elapsedTime when paused or timestamp is missing.
    """
    try:
        elapsed = float(data.get("elapsedTime") or 0)
        rate = float(data.get("playbackRate") or 0)
        duration = float(data.get("duration") or 0)
    except (TypeError, ValueError):
        return 0

    try:
        stamp = datetime.fromisoformat((data.get("timestamp") or "").replace("Z", "+00:00"))
    except (ValueError, TypeError, AttributeError):
        stamp = None

    pos = elapsed
    if rate > 0 and stamp is not None:
        pos = elapsed + (datetime.now(timezone.utc) - stamp).total_seconds() * rate
        if duration and pos > duration:
            pos = duration
    return int(round(max(0.0, pos) * 1000))


def fetch_now_playing() -> dict:
    raw = run_media_control("get")
    if not raw or raw == "null":
        return {"playing": False}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"playing": False}

    if not isinstance(data, dict):
        return {"playing": False}

    title = data.get("title") or ""
    artist = data.get("artist") or ""
    album = data.get("album") or ""
    playing = bool(data.get("playing", False))

    try:
        duration_ms = int(float(data.get("duration") or 0) * 1000)
    except (TypeError, ValueError):
        duration_ms = 0
    position_ms = real_position_ms(data)

    art = None
    artwork_data = data.get("artworkData")
    mime = data.get("artworkMimeType") or "image/jpeg"
    if artwork_data and isinstance(artwork_data, str) and len(artwork_data) < 2_000_000:
        artwork_data = artwork_data.replace(r"\/", "/")
        art = f"data:{mime};base64,{artwork_data}"

    # Electron / WebKit apps (e.g. Nuclear) register their media session
    # under the WebKit subprocess; the parent bundle id is the real app.
    app_id = data.get("parentApplicationBundleIdentifier") or data.get("bundleIdentifier") or ""

    result = {
        "playing": playing and bool(title),
        "title": title,
        "artist": artist,
        "album": album,
        "app": app_id,
        "position_ms": position_ms,
        "duration_ms": duration_ms,
        "art": art,
    }

    if title:
        print(f"→ {title} – {artist} | playing={result['playing']} | pos={position_ms}ms | app={app_id}")
    return result


@app.route("/now-playing")
def now_playing():
    return jsonify(fetch_now_playing())


@app.route("/health")
def health():
    raw = run_media_control("get")
    return jsonify({
        "status": "ok",
        "bridge": "macos",
        "media_control": bool(raw and raw != "null"),
    })


@app.route("/")
def root():
    return jsonify({
        "message": "Now Playing Bridge is running",
        "endpoint": "/now-playing",
        "health": "/health",
    })


if __name__ == "__main__":
    print("=" * 56)
    print("  Now Playing Bridge (macOS)")
    print("=" * 56)
    print("  Keep this window open while streaming.")
    print(f"  Widget reads from: http://127.0.0.1:{PORT}/now-playing")
    print("=" * 56)
    print()
    try:
        app.run(host="127.0.0.1", port=PORT, debug=False, threaded=True)
    except OSError as e:
        if e.errno == 48 or "Address already in use" in str(e):
            print()
            print(f"  Port {PORT} is already in use — the bridge could not start.")
            print("  On macOS this is usually the AIRPLAY RECEIVER.")
            print("  Fix: System Settings → General → AirDrop & Handoff")
            print("       → turn OFF \"AirPlay Receiver\", then run again.")
            print("  Or use another port:  NP_PORT=8124  python server.py")
            print("  (you must also update the port in the widget link)")
        else:
            raise
