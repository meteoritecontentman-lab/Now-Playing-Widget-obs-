#!/usr/bin/env python3
"""
Now Playing Bridge – macOS
Reads system Now Playing and serves it to the widget.
"""

import json
import subprocess
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

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
        position_ms = int(float(data.get("elapsedTime") or 0) * 1000)
    except (TypeError, ValueError):
        duration_ms = 0
        position_ms = 0

    art = None
    artwork_data = data.get("artworkData")
    mime = data.get("artworkMimeType") or "image/jpeg"
    if artwork_data and isinstance(artwork_data, str) and len(artwork_data) < 2_000_000:
        artwork_data = artwork_data.replace(r"\/", "/")
        art = f"data:{mime};base64,{artwork_data}"

    app_id = data.get("bundleIdentifier") or ""

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
        print(f"→ {title} – {artist} | playing={result['playing']} | app={app_id}")
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
    print("  Widget reads from: http://127.0.0.1:5000/now-playing")
    print("=" * 56)
    print()
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
