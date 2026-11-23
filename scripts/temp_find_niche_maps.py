with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

import re

# Find all map definitions and their video lists
maps = re.findall(r'const\s+([A-Za-z0-9_]+_VIDEOS_MAP|[A-Za-z0-9_]+_VIDEOS|CREATORS_[A-Za-z0-9_]+)\s*=\s*\[(.*?)\];', vc, re.DOTALL)
print(f"Total array definitions: {len(maps)}")

for name, body in maps:
    vids = re.findall(r'https?://[^\s"\'<>]+\.mp4', body)
    if any(k in name.lower() for k in ['aiwa', 'jbl', 'som', 'boombox', 'hisense', 'midea', 'lava', 'jantar', 'copo', 'ryo', 'prato', 'panelas']):
        print(f"Array {name}: {len(vids)} videos")
        for v in vids[:3]:
            print(f"    {v}")
