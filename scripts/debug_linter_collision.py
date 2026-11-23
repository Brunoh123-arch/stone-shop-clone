# -*- coding: utf-8 -*-
import re
from collections import defaultdict

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

cases = re.findall(r'case\s+(\d+):\s+activeDataset\s*=\s*([A-Za-z0-9_]+);', js_content)
prod_to_dataset = {int(p): ds for p, ds in cases}

array_defs = re.findall(r'const\s+([A-Za-z0-9_]+)\s*=\s*(\[\s*\{.*?\}\s*\]);', js_content, re.DOTALL)
dataset_videos = defaultdict(list)
for var_name, arr_str in array_defs:
    vids = re.findall(r'video:\s*["\']([^"\']+)["\']', arr_str)
    if vids:
        dataset_videos[var_name] = [v.strip() for v in vids]

map_links = re.findall(r'const\s+([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_]+)\.map', js_content)
creators_to_source = dict(map_links)

for pid in [57, 73, 81]:
    ds_name = prod_to_dataset.get(pid)
    src_map = creators_to_source.get(ds_name, ds_name)
    vids = dataset_videos.get(src_map, []) or dataset_videos.get(ds_name, [])
    print(f"P{pid} ({ds_name} -> {src_map}): {vids}")
