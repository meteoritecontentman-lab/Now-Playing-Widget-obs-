#!/usr/bin/env python3
"""
Now Playing Bridge – Linux (MPRIS via playerctl)
"""

import json
import subprocess
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def run(*args) -> str:
    try:
        r = subprocess.run(
            args, capture_output=True, text=True, timeout=4
        )
        if r.returncode != 0:
            return ""
        return (r.stdout or "").strip()
    except FileNotFoundError:
        print("ERROR: playerctl not found. Install: sudo apt install playerctl")
        return ""
    except Exception as e:
        print("playerctl error:", e)
        return ""


def fetch_now_playing() -> dict:
    # Prefer the first active player
    status = run("playerctl", "status")
    if not status:
        return {"playing": False}

    playing = status.lower() == "playing"
    title = run("playerctl", "metadata", "xesam:title") or ""
    artist = run("playerctl", "metadata", "xesam:artist") or ""
    album = run("playerctl", "metadata", "xesam:album") or ""
    art_url = run("playerctl", "metadata", "mpris:artUrl") or ""
    length_us = run("playerctl", "metadata", "mpris:length") or "0"
    position = run("playerctl", "position") or "0"
    player = run("playerctl", "metadata", "--format", "{{playerName}}") or ""

    try:
        duration_ms = int(int(length_us) / 1000)  # microseconds -> ms
    except ValueError:
        duration_ms = 0
    try:
        position_ms = int(float(position) * 1000)
    except ValueError:
        position_ms = 0

    art = None
    if art_url.startswith("http") or art_url.startswith("file:"):
        art = art_url  # browser may load http; file: works on same machine

    result = {
        "playing": playing and bool(title),
        "title": title,
        "artist": artist,
        "album": album,
        "app": player,
        "position_ms": position_ms,
        "duration_ms": duration_ms,
        "art": art,
    }
    if title:
        print(f"→ {title} – {artist} | playing={result['playing']} | app={player}")
    return result


@app.route("/now-playing")
def now_playing():
    return jsonify(fetch_now_playing())


@app.route("/health")
def health():
    data = fetch_now_playing()
    return jsonify({
        "status": "ok",
        "bridge": "linux",
        "media_control": bool(data.get("title")),
    })


@app.route("/")
def root():
    return jsonify({"message": "Now Playing Bridge (Linux)", "endpoint": "/now-playing"})


if __name__ == "__main__":
    print("=" * 56)
    print("  Now Playing Bridge (Linux)")
    print("=" * 56)
    print("  Requires: playerctl (sudo apt install playerctl)")
    print("  http://127.0.0.1:5000/now-playing")
    print("=" * 56)
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
