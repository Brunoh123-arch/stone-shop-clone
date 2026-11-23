import urllib.request
import json
import os

with open('scripts_archive/found_target.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

revs = d.get('review_info', {}).get('product_reviews', [])
os.makedirs('img', exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for i, r in enumerate(revs):
    imgs = r.get('review_images', [])
    for j, url in enumerate(imgs):
        # convert to 800x800 high res jpeg
        base_url = url.split('~')[0]
        high_res_url = base_url + '~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg'
        out_name = f'img/review-104-c{i+1}-{j+1}.jpg'
        try:
            req = urllib.request.Request(high_res_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                with open(out_name, 'wb') as out_f:
                    out_f.write(data)
                print(f"Downloaded {out_name}: {len(data)} bytes")
        except Exception as e:
            print(f"Failed {high_res_url}: {e}, falling back to original {url}")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                with open(out_name, 'wb') as out_f:
                    out_f.write(data)
                print(f"Downloaded fallback {out_name}: {len(data)} bytes")
