# Now Playing

OBS Now Playing overlay. Works on **macOS**, **Windows**, and **Linux**.

## How to upload to GitHub Pages

1. Download and **unzip** `now-playing-site.zip`
2. You will see a folder (e.g. `now-playing-pages`) with files like:
   - `index.html`
   - `widget.html`
   - `bridge-macos.zip`
   - `bridge-windows.zip`
   - `bridge-linux.zip`
   - `README.md`
   - `bridge/` folder (optional to upload; the zips are what users download)
3. Create a new GitHub repository
4. Upload the **contents inside** that folder to the **root** of the repo  
   (upload `index.html`, `widget.html`, the three `bridge-*.zip` files, etc.  
   Do **not** upload the outer `now-playing-site.zip`.  
   Do **not** put everything inside an extra nested folder.)
5. Repo **Settings → Pages → Deploy from branch → `main` → `/ (root)`**
6. Open `https://YOUR_USERNAME.github.io/REPO_NAME/`

## Bridge per OS

| OS | Download | How to start | Needs |
|----|----------|--------------|--------|
| macOS | `bridge-macos.zip` | Double-click `Start Bridge.command` | Homebrew + `media-control` |
| Windows | `bridge-windows.zip` | Double-click `Start Bridge.bat` | Python 3 (Add to PATH) |
| Linux | `bridge-linux.zip` | Run `./Start Bridge.sh` | `playerctl` + Python 3 |

Keep the Bridge window open while streaming. Data stays on your computer.
