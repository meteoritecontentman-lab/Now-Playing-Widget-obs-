<div align="center">

# 🎵 Now Playing — OBS Overlay

**A beautiful, live "Now Playing" card for your OBS stream.**
Design it once, generate a link, paste it into OBS — done.

[![Platforms](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-22c55e?style=for-the-badge&logo=obsstudio&logoColor=white&labelColor=0f0f12)](https://github.com/meteoritecontentman-lab/Now-Playing-Widget-obs-)
[![Privacy](https://img.shields.io/badge/privacy-100%25%20local-0ea5e9?style=for-the-badge&labelColor=0f0f12)](https://github.com/meteoritecontentman-lab/Now-Playing-Widget-obs-)
[![No Account](https://img.shields.io/badge/no%20account%E2%80%A2no%20cloud-f59e0b?style=for-the-badge&labelColor=0f0f12)](https://github.com/meteoritecontentman-lab/Now-Playing-Widget-obs-)

</div>

---

## ✨ What is it?

A **live Now Playing overlay** that shows the song/track currently playing
on your computer — right in your OBS scene.

- 🖥️ Works on **macOS**, **Windows**, and **Linux**
- ⚡ **Always live** — Worker-powered polling means the card updates in real time even when the OBS scene/tab isn't focused (plain timers get throttled by browsers)
- 🎚️ Full **customizer** — pick your accent color, opacity, radius, size, which elements to show (album art, progress bar, time, play button, artist), or add the optional **voice visualizer**
- 🔒 **100% private** — a tiny local "Bridge" reads your music and serves it straight to the widget. **Nothing ever leaves your computer.**
- 🧩 Paste **one link** into OBS Browser Source and you're live

> No account. No cloud. No sign-up. Just an overlay that knows what you're playing.

---

## 🗺️ How it works

```
┌──────────────┐   config (in URL)   ┌──────────────┐   poll every 1.6s   ┌─────────────────┐
│  Customizer  │ ──────────────────▶ │    Widget    │ ──────────────────▶ │  Bridge (local) │
│  (web page)  │                     │  (OBS overlay)│                     │  reads your OS   │
└──────────────┘                     └──────────────┘                     │  Now Playing     │
                                                                            └─────────────────┘
```

- **Customizer** — the web page you edit your overlay on
- **Widget** — the actual overlay; a glassy card with album art, title, artist, progress bar & time
- **Bridge** — a tiny Python server that runs **on your computer** and feeds the widget live track data

---

## 🚀 Quick start (3 steps)

### 1️⃣ Download the Bridge for your system

<details>
<summary><b>macOS</b> — <code>bridge-macos.zip</code></summary>

| | |
|---|---|
| **Download** | `bridge-macos.zip` (button in the customizer) |
| **How to start** | First time: **right-click** `Start Bridge.command` → **Open**. After that, double-click. |
| **Needs** | [Homebrew](https://brew.sh) (auto-installed by the script) |

</details>

<details>
<summary><b>Windows</b> — <code>bridge-windows.zip</code></summary>

| | |
|---|---|
| **Download** | `bridge-windows.zip` (button in the customizer) |
| **How to start** | Double-click `Start Bridge.bat` |
| **Needs** | Python 3 from [python.org](https://python.org) — tick **"Add Python to PATH"** during install |

</details>

<details>
<summary><b>Linux</b> — <code>bridge-linux.zip</code></summary>

| | |
|---|---|
| **Download** | `bridge-linux.zip` (button in the customizer) |
| **How to start** | `./Start Bridge.sh` in the unzipped folder |
| **Needs** | `playerctl` (`sudo apt install playerctl`) + Python 3 |

</details>

> 📖 Every bridge zip also ships with its own **`README.txt`** — a full step-by-step guide, right in the setup.

### 2️⃣ Design your overlay & generate the link

Open the **customizer** page → pick your colors & options → click **`Save settings`**.

### 3️⃣ Paste it into OBS

1. OBS → **Sources** → **＋** → **Browser**
2. Paste the link into the **URL** field
3. Set the size to **`480 × 140`** (or *Fit to screen*)
4. Start your music — the card appears 🎶

Keep the Bridge window **open** while streaming.

---

## 🎛️ What you can customize

| Option | What it does |
|---|---|
| 🎨 **Accent** | Color of the progress bar, glow & art tint |
| 🔍 **Show only** | Widget only appears for *Any app / Spotify / Apple Music / YouTube-Browser* |
| 🌫️ **Opacity** | Glass effect strength (25% → 95%) |
| 📐 **Radius / Width / Art size** | Shape & dimensions of the card |
| 🔘 **Elements** | Toggle album art, progress bar, time, play button, artist on/off |
| 🎤 **Visualizer** | Animated audio bars at the bottom of the card (accent colored, dances while music plays) |

The preview updates **live** — and when you hit **`Save settings`**, your choices are baked into the link
so anyone you share it with sees **your** design. Change the controls without saving and the link stays
untouched (an "Unsaved" badge reminds you to hit save).

---

## 🔧 Troubleshooting

### 😵 The bridge won't start on macOS ("Address already in use")
<details>
<summary>This is almost always the <b>AirPlay Receiver</b> — here's the fix</summary>

macOS's **AirPlay Receiver** (System Settings → General → AirDrop & Handoff) grabs
**port 5000**, which is why the old bridge crashed on startup.

**This version uses port `8123` instead**, which avoids the conflict.
If you still see *Address already in use*:

1. System Settings → **General** → **AirDrop & Handoff**
2. Turn **OFF** → **AirPlay Receiver**
3. Start the Bridge again

Or pick your own port: `NP_PORT=8124 python server.py`
(also update the port number in the widget link).
</details>

### 📴 The designer says "Bridge offline"
- Make sure the Bridge window is **open** (look for `Now Playing Bridge (…OS)` in the title)
- Make sure **something is actually playing** (Spotify, Apple Music, a browser tab with YouTube…)

### 🚫 "This build can't be opened" (macOS)
macOS Gatekeeper blocks unsigned scripts. **Right-click** the `.command` file → **Open** → **Open**.
You only do this once.

### 🖼️ No album art
Most apps expose art (Spotify, Apple Music, Chrome…). Some sources don't — the widget
shows a clean placeholder instead. Nothing is broken.

---

## 🔒 Privacy

<span style="color:#22c55e">✔ **No cloud. No account. No tracking.**</span>

The Bridge listens **only on `127.0.0.1`** — your own computer. All track data
(title, artist, art) stays local. The widget is served from GitHub Pages, but it talks
only to your machine's local Bridge.

---

## 🛠️ Project structure

```
├── index.html          → Customizer (design your overlay, generate the link)
├── widget.html         → The OBS overlay widget itself
├── bridge/
│   ├── macos/          → macOS Bridge (media-control + Flask)
│   ├── windows/        → Windows Bridge (winsdk SMTC + Flask)
│   └── linux/          → Linux Bridge (playerctl MPRIS + Flask)
├── bridge-*.zip        → Ready-to-download per-OS bridge packages
└── README.md           → You are here ✌️
```

---

<div align="center">

**Made with ❤️ for streamers.**
<span style="color:#71717a">Now Playing · Private · Local · Live</span>

</div>