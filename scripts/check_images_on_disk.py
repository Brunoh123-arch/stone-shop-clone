import os
import re

ids = [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 68, 70, 72, 73, 74, 75, 76]

for pid in ids:
    filepath = f"pages/produto-{pid}.html"
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Find all img src in the html
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    
    missing_local = []
    remote_urls = []
    existing_local = []
    
    for img in imgs:
        if img.startswith('http://') or img.startswith('https://'):
            remote_urls.append(img)
        else:
            # relative path from pages/
            # e.g. ../img/... -> img/...
            norm = os.path.normpath(os.path.join("pages", img))
            if not os.path.exists(norm):
                missing_local.append((img, norm))
            else:
                existing_local.append((img, norm))
                
    # Also find videos
    vids = re.findall(r'<video[^>]+src=["\']([^"\']+)["\']', html)
    missing_vids = []
    for v in vids:
        if not (v.startswith('http://') or v.startswith('https://')):
            norm_v = os.path.normpath(os.path.join("pages", v))
            if not os.path.exists(norm_v):
                missing_vids.append((v, norm_v))

    print(f"P{pid}: {len(imgs)} imgs ({len(existing_local)} local ok, {len(missing_local)} MISSING local, {len(remote_urls)} remote) | {len(vids)} vids")
    if missing_local:
        print(f"   MISSING IMAGES in P{pid}: {missing_local}")
    if missing_vids:
        print(f"   MISSING VIDEOS in P{pid}: {missing_vids}")
