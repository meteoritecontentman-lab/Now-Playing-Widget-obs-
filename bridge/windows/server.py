#!/usr/bin/env python3
"""
Now Playing Bridge – Windows
Uses System Media Transport Controls (SMTC).
"""

import asyncio
import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

_cache = {"playing": False}


async def _fetch_smtc():
    try:
        from winsdk.windows.media.control import (
            GlobalSystemMediaTransportControlsSessionManager as MediaManager,
        )
    except ImportError:
        return {
            "playing": False,
            "error": "winsdk not installed. Run: pip install winsdk",
        }

    try:
        manager = await MediaManager.request_async()
        session = manager.get_current_session()
        if not session:
            return {"playing": False}

        info = await session.try_get_media_properties_async()
        timeline = session.get_timeline_properties()
        playback = session.get_playback_info()

        title = (info.title or "").strip()
        artist = (info.artist or "").strip()
        album = (info.album_title or "").strip() if hasattr(info, "album_title") else ""
        app_id = session.source_app_user_model_id or ""

        status = playback.playback_status
        # 4 = Playing, 5 = Paused (winsdk enum)
        playing = int(status) == 4

        position_ms = int(timeline.position.total_seconds() * 1000) if timeline else 0
        duration_ms = int(timeline.end_time.total_seconds() * 1000) if timeline else 0

        art = None
        try:
            ref = info.thumbnail
            if ref:
                stream = await ref.open_read_async()
                # Reading thumbnail from stream is complex; skip if hard
                # Many setups work without art on Windows first version
        except Exception:
            pass

        return {
            "playing": playing and bool(title),
            "title": title,
            "artist": artist,
            "album": album,
            "app": app_id,
            "position_ms": position_ms,
            "duration_ms": duration_ms,
            "art": art,
        }
    except Exception as e:
        return {"playing": False, "error": str(e)}


def fetch_now_playing():
    global _cache
    try:
        _cache = asyncio.run(_fetch_smtc())
    except Exception as e:
        _cache = {"playing": False, "error": str(e)}
    if _cache.get("title"):
        print(f"→ {_cache.get('title')} – {_cache.get('artist')} | playing={_cache.get('playing')}")
    return _cache


@app.route("/now-playing")
def now_playing():
    return jsonify(fetch_now_playing())


@app.route("/health")
def health():
    data = fetch_now_playing()
    return jsonify({
        "status": "ok",
        "bridge": "windows",
        "media_control": bool(data.get("title")),
    })


@app.route("/")
def root():
    return jsonify({"message": "Now Playing Bridge (Windows)", "endpoint": "/now-playing"})


if __name__ == "__main__":
    print("=" * 56)
    print("  Now Playing Bridge (Windows)")
    print("=" * 56)
    print("  Keep this window open while streaming.")
    print("  http://127.0.0.1:5000/now-playing")
    print("=" * 56)
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
