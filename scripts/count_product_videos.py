# -*- coding: utf-8 -*-
import re

with open('js/videos-criadores-v3.js', 'r', encoding='utf-8') as f:
    txt = f.read()

cases = re.findall(r'case\s+(\d+):\s+activeDataset\s*=\s*([A-Za-z0-9_]+);', txt)
array_defs = dict(re.findall(r'const\s+([A-Za-z0-9_]+)\s*=\s*(\[\s*\{.*?\}\s*\]);', txt, re.DOTALL))
map_links = dict(re.findall(r'const\s+([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_]+)\.map', txt))

counts = {}
for pid_str, ds_name in cases:
    pid = int(pid_str)
    src = map_links.get(ds_name, ds_name)
    arr = array_defs.get(src, '') or array_defs.get(ds_name, '')
    vids = re.findall(r'video:\s*["\']([^"\']+)["\']', arr)
    counts[pid] = len(vids)

zeros = [p for p, c in counts.items() if c == 0]
ones = [p for p, c in counts.items() if c == 1]
fews = [p for p, c in counts.items() if 2 <= c <= 3]
plentiful = [p for p, c in counts.items() if c >= 4]

print(f"Total de produtos mapeados no switch: {len(counts)}")
print(f"Produtos com 0 videos: {len(zeros)} -> {zeros}")
print(f"Produtos com 1 video: {len(ones)} -> {sorted(ones)}")
print(f"Produtos com 2 a 3 videos: {len(fews)} -> {sorted(fews)}")
print(f"Produtos com 4+ videos: {len(plentiful)} -> {sorted(plentiful)}")
