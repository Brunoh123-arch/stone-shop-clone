import urllib.request
import os

hashes = [
    '13cb2651da0b4f74b45a5973cfa4d96f',
    '72a8389aeec340f199c03ffa21a3ba88'
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for h in hashes:
    url_800 = f'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/{h}~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg'
    out_file = f'scratch/{h}.jpg'
    try:
        req = urllib.request.Request(url_800, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            with open(out_file, 'wb') as f:
                f.write(data)
            print(f"Downloaded {out_file}: {len(data)} bytes")
    except Exception as e:
        print(f"Failed {url_800}: {e}")
