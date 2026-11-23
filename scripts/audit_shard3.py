import os
import re

ids = [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 68, 70, 72, 73, 74, 75, 76]

for i in ids:
    p = f'pages/produto-{i}.html'
    if not os.path.exists(p):
        print(f"P{i}: NOT FOUND")
        continue
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    title_m = re.search(r'<title>(.*?)</title>', html, re.I)
    title = title_m.group(1).strip() if title_m else 'No Title'

    # Check creators section tag
    cs = re.findall(r'<div[^>]*id=["\']creators-section["\'][^>]*>', html)
    # Check video block
    pv = re.findall(r'<div[^>]*class=["\'][^"\']*product-video-block[^"\']*["\'][^>]*>', html)
    vids = re.findall(r'<video[^>]*src=["\']([^"\']+)["\'][^>]*>', html)
    
    print(f"P{i} ({title[:35]}):")
    print(f"   Creators section tags: {cs}")
    print(f"   Product-video-block count: {len(pv)}")
    if vids:
        print(f"   Video src: {vids}")
