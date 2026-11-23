with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

import re

for pid in [9, 13, 14, 15, 101, 102]:
    m = re.search(r'case\s+' + str(pid) + r'\s*:\s*(.*?)(?=case|\bdefault:|$)', vc, re.DOTALL)
    if m:
        ds_match = re.search(r'activeDataset\s*=\s*([A-Za-z0-9_]+)', m.group(1))
        ds_name = ds_match.group(1) if ds_match else "NONE"
        # Find ds_name
        pos = vc.find(f"{ds_name} =")
        if pos != -1:
            sub = vc[pos:pos+3000]
            vids = re.findall(r'https?://[^\s"\'<>]+\.mp4', sub)
            print(f"P{pid}: {ds_name} -> {len(vids)} videos found in definition")
        else:
            print(f"P{pid}: {ds_name} NOT FOUND IN VC")
