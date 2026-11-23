import urllib.request
import urllib.parse
import json
import re
import os
from PIL import Image
import io

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_bing_images(query, count=20):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;.*?&quot;t&quot;:&quot;([^&]+)&quot;', html)
            res = []
            for murl, title in matches:
                res.append({'url': murl, 'title': title})
            return res[:count]
    except Exception as e:
        print(f"Erro buscando {query}: {e}")
        return []

def download_and_crop_square(url, dest_path, target_size=(800, 800)):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = resp.read()
        if len(data) < 3000:
            return False
        img = Image.open(io.BytesIO(data))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Crop square centered
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        cropped = img.crop((left, top, right, bottom))
        resized = cropped.resize(target_size, Image.Resampling.LANCZOS)
        
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        resized.save(dest_path, 'JPEG', quality=90)
        print(f"[OK] Salvo {dest_path} ({target_size[0]}x{target_size[1]})")
        return True
    except Exception as e:
        print(f"[FAIL] {url} -> {e}")
        return False

if __name__ == '__main__':
    # Test queries
    q111 = search_bing_images('USB Christmas LED projector night light card rotation')
    print("111 results:", len(q111))
    for r in q111[:5]:
        print(" ", r['title'][:60], "->", r['url'])
