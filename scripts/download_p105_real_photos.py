import urllib.request
import io
from PIL import Image

jobs = [
    ("https://http2.mlstatic.com/D_NQ_NP_796129-MLA90259532472_082025-F.jpg", "img/review-105-real-1.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_669590-MLA89893366056_082025-F.jpg", "img/review-105-real-2.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_782698-MLA91210674183_082025-F.jpg", "img/review-105-real-3.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_611428-MLA90660209463_082025-F.jpg", "img/review-105-real-4.jpg"),
]

for url, dest in jobs:
    print(f"Downloading {url} -> {dest}")
    data = urllib.request.urlopen(url).read()
    im = Image.open(io.BytesIO(data)).convert('RGB')
    w, h = im.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    im_c = im.crop((left, top, left + min_dim, top + min_dim)).resize((600, 600), Image.Resampling.LANCZOS)
    im_c.save(dest, 'JPEG', quality=88)
    print(f"[OK] {dest} (600x600)")
