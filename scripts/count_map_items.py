with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
maps = re.findall(r'const\s+([A-Z0-9_]+VIDEOS_MAP)\s*=\s*\[(.*?)\];', text, re.DOTALL)
for name, body in maps:
    items = body.count('name:')
    print(f"{name}: {items} videos")
