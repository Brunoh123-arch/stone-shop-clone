import urllib.request

hashes = [
    'd7d22a74fadf473aaa2306adceca1bdd',
    '486e31e7e16c46618948fe0894e72f6a',
    '02dfe8e2b03e4bc0b8a3f8bf808b3a12',
    '6463ed3db44a4801921537f1ed095372',
    'd87ba131961c43a690e05ed65a575f24'
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for idx, h in enumerate(hashes):
    url = f"https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/{h}~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
    dest = f"img/review-104-ks-{idx+1}.jpg"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            with open(dest, 'wb') as f:
                f.write(data)
            print(f"Downloaded {dest}: {len(data)} bytes")
    except Exception as e:
        print(f"Failed {url}: {e}")
