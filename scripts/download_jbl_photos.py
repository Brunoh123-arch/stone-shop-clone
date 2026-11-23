import urllib.request
import os
from PIL import Image
import io

os.makedirs('img', exist_ok=True)

# 1. Gallery images
gallery_urls = [
    "https://http2.mlstatic.com/D_NQ_NP_2X_932616-MLA99475097854_112025-F.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_866750-MLU74810519490_032024-F.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_711382-MLU74945500283_032024-F.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_699104-MLU74810012176_032024-F.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_880946-MLU75980414337_042024-F.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_721498-MLA74670647272_022024-F.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_755160-MLA74670637314_022024-F.webp"
]

for idx, url in enumerate(gallery_urls, 1):
    dest = f"img/jbl-boombox3-{idx}.jpg"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = urllib.request.urlopen(req, timeout=15).read()
        im = Image.open(io.BytesIO(data)).convert('RGB')
        im.save(dest, 'JPEG', quality=92)
        print(f"Salvo gallery: {dest} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"Erro ao salvar {dest}: {e}")

# 2. Review photos
review_urls = [
    "https://http2.mlstatic.com/D_NQ_NP_2X_779447-MLA75501106359_032024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_943775-MLA75500872595_032024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_868977-MLA75500784263_032024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_748853-MLA75348815538_032024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_950429-MLA75241962716_032024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_836480-MLA77239059139_062024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_737893-MLA76464971825_052024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_602160-MLA76211069360_052024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_769016-MLA76399440589_052024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_645392-MLA76210724118_052024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_943849-MLA76210724120_052024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_630368-MLA76211010400_052024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_813417-MLA76210813098_052024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_723456-MLA76210743992_052024-O.webp",
    "https://http2.mlstatic.com/D_NQ_NP_2X_894281-MLA76399400743_052024-O.webp"
]

for idx, url in enumerate(review_urls, 1):
    dest = f"img/review-4-c{idx}-1.jpg"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = urllib.request.urlopen(req, timeout=15).read()
        im = Image.open(io.BytesIO(data)).convert('RGB')
        im.save(dest, 'JPEG', quality=90)
        print(f"Salvo review: {dest} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"Erro ao salvar {dest}: {e}")
