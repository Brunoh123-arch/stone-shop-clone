import urllib.request
import subprocess
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
videos = [
    ("v0", "https://files.catbox.moe/8oqszr.mp4"),
    ("v1", "https://files.catbox.moe/mp9tua.mp4"),
]

for name, url in videos:
    fn = f"temp_{name}.mp4"
    jpg = f"temp_{name}.jpg"
    try:
        print(f"Downloading {url}...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp, open(fn, 'wb') as out:
            out.write(resp.read())
        subprocess.run(["ffmpeg", "-y", "-i", fn, "-ss", "00:00:02", "-vframes", "1", jpg], capture_output=True)
        print(f"Frame extracted: {jpg}")
    except Exception as e:
        print(f"Error {name}: {e}")
