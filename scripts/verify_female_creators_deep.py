import re, os
from PIL import Image

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    code = f.read()

target_maps = [
    'CHINELO_VIDEOS_MAP',
    'BODY_106_VIDEOS_MAP',
    'ESCOVA_108_VIDEOS_MAP',
    'MODELADOR_109_VIDEOS_MAP',
    'REBECCA_BONBON_28_VIDEOS_MAP'
]

for map_name in target_maps:
    m = re.search(r'const\s+' + map_name + r'\s*=\s*\[([\s\S]*?)\];', code)
    if not m:
        print(f"NOT FOUND: {map_name}")
        continue
    items = re.findall(r'name:\s*["\']([^"\']+)["\'],\s*username:\s*["\']([^"\']+)["\'],\s*avatar:\s*["\']([^"\']+)["\']', m.group(1))
    print(f"\n===============================")
    print(f"{map_name} ({len(items)} creators)")
    print(f"===============================")
    for idx, (name, user, avatar) in enumerate(items):
        clean_avatar = avatar.split('?')[0].replace('../', '')
        exists = os.path.exists(clean_avatar)
        size = 'N/A'
        if exists:
            try:
                im = Image.open(clean_avatar)
                size = f"{im.size[0]}x{im.size[1]}"
            except Exception as e:
                size = f"ERR: {e}"
        print(f"[{idx+1:02d}] {name} (@{user}) -> {avatar} (exists={exists}, size={size})")
