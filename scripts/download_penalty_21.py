import urllib.request, os

images = {
    'img/produto-21-1.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rbkz-m5oo5ljc9heg98',
    'img/produto-21-2.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rbll-m5oo5jzajgi6f4',
    'img/review-21-c1-1.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rbkz-m5oo5ljc9heg98',
    'img/review-21-c2-1.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rbll-m5oo5jzajgi6f4',
    'img/review-21-c3-1.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rbkz-m5oo5ljc9heg98',
    'img/review-21-c4-1.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rbll-m5oo5jzajgi6f4',
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for path, url in images.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp, open(path, 'wb') as f:
            f.write(resp.read())
        print(f"Baixado: {path}")
    except Exception as e:
        print(f"Erro em {path}: {e}")
