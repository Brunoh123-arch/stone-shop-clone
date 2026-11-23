import subprocess

urls = [
    ('74_75', 'https://files.catbox.moe/m3uloo.mp4'),
    ('76', 'https://files.catbox.moe/0hhasi.mp4'),
    ('53_59', 'https://files.catbox.moe/s6vnyh.mp4'),
    ('54', 'https://files.catbox.moe/0qd90i.mp4'),
    ('56', 'https://files.catbox.moe/2t30kf.mp4'),
    ('68', 'https://files.catbox.moe/sdcjn0.mp4')
]

for label, url in urls:
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size', '-of', 'default=noprint_wrappers=1', url]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        print(f"[{label}] {url} -> {res.stdout.strip() if res.stdout else res.stderr.strip()[:100]}")
    except Exception as e:
        print(f"[{label}] {url} -> ERROR: {e}")
