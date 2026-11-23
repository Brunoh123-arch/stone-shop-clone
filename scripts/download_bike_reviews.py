import urllib.request
import os
from PIL import Image
import io

urls = [
    'https://http2.mlstatic.com/D_NQ_NP_2X_931714-MLA82795826349_022025-O.webp',
    'https://http2.mlstatic.com/D_NQ_NP_2X_664580-MLA85301462413_052025-O.webp',
    'https://http2.mlstatic.com/D_NQ_NP_2X_934568-MLA83672165904_042025-O.webp',
    'https://http2.mlstatic.com/D_NQ_NP_2X_904126-MLA85035998173_052025-O.webp',
    'https://http2.mlstatic.com/D_NQ_NP_2X_637414-MLA86414782137_062025-O.webp',
    'https://http2.mlstatic.com/D_NQ_NP_2X_660015-MLA86098967792_062025-O.webp'
]

os.makedirs('img', exist_ok=True)

for i, url in enumerate(urls, 1):
    dest = f'img/review-6-c{i}-1.jpg'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = urllib.request.urlopen(req, timeout=15).read()
        img = Image.open(io.BytesIO(data))
        img = img.convert('RGB')
        img.save(dest, 'JPEG', quality=90)
        print(f"Salvo: {dest} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"Erro {dest}: {e}")
