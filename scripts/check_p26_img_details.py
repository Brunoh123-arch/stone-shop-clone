import urllib.request
import re
from PIL import Image
import io

with open('pages/produto-26.html', 'r', encoding='utf-8') as f:
    c = f.read()

imgs = re.findall(r'<img[^>]+class=["\']slider-img["\'][^>]+src=["\']([^"\']+)["\']', c)
headers = {'User-Agent': 'Mozilla/5.0'}

for i, url in enumerate(imgs):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            img = Image.open(io.BytesIO(data))
            print(f"Slide {i+1}: size={img.size}, format={img.format} -> {url}")
    except Exception as e:
        print(f"Slide {i+1}: ERRO {e}")
