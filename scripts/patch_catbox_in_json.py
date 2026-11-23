import glob
import json
import os

MAP_FILE = 'scripts/catbox_videos_map.json'
with open(MAP_FILE, 'r', encoding='utf-8') as f:
    vmap = json.load(f)

# Also ensure product 9 is in vmap
vmap['criador-9-1.mp4'] = 'https://files.catbox.moe/9e4pfq.mp4'
vmap['criador-9-2.mp4'] = 'https://files.catbox.moe/zmlngs.mp4'
vmap['criador-9-3.mp4'] = 'https://files.catbox.moe/byfq7d.mp4'
with open(MAP_FILE, 'w', encoding='utf-8') as f:
    json.dump(vmap, f, indent=2, ensure_ascii=False)

for jf in glob.glob('scripts/data/produto_*.json'):
    with open(jf, 'r', encoding='utf-8') as f:
        d = json.load(f)
    pid = d['id']
    modified = False
    for c in d.get('creators', []):
        local_v = c.get('localVideo', '')
        base = os.path.basename(local_v)
        if base in vmap:
            c['video'] = vmap[base]
            modified = True
        elif not c.get('video', '').startswith('https://files.catbox.moe/'):
            # Fallback to an existing reliable catbox video
            fallback_map = {
                1: 'https://files.catbox.moe/p7r4vc.mp4',
                2: 'https://files.catbox.moe/ac2l43.mp4',
                3: 'https://files.catbox.moe/byfq7d.mp4'
            }
            v_idx = 1
            if '-2.mp4' in local_v: v_idx = 2
            elif '-3.mp4' in local_v: v_idx = 3
            c['video'] = fallback_map[v_idx]
            modified = True
    if modified:
        with open(jf, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"Patched Catbox URLs in {jf}")
