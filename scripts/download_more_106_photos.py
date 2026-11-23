import json
import urllib.request
import io
import re
from PIL import Image

with open('reviews_106_real.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect all photos from data
all_urls = []
for r in data:
    for p in r.get('photos', []):
        if p not in all_urls:
            all_urls.append(p)

print(f"Total unique URLs in reviews_106_real.json: {len(all_urls)}")

# Download photos 5 to 10 (index 4 to 9)
for idx in range(5, 11):
    url = all_urls[idx - 1]
    dest = f"img/review-106-real-{idx}.jpg"
    print(f"Downloading {idx}: {url} -> {dest}")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        img_bytes = resp.read()
    im = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    w, h = im.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    im_c = im.crop((left, top, left + min_dim, top + min_dim)).resize((600, 600), Image.Resampling.LANCZOS)
    im_c.save(dest, 'JPEG', quality=88)
    print(f"Saved {dest}")

print("Done downloading photos 5 to 10 for P106!")
