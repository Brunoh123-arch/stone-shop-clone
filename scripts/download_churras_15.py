import urllib.request, os

images = {
    'img/produto-15-1.jpg': 'https://down-br.img.susercontent.com/file/br-11110105-7r98o-lr96mg3y7nja34',
    'img/produto-15-2.jpg': 'https://down-br.img.susercontent.com/file/br-11134207-7r98o-lqnmb7oulw6f02',
    'img/produto-15-3.jpg': 'https://down-br.img.susercontent.com/file/br-11134207-7r98o-lyzm72oahjk1ad',
    'img/produto-15-4.jpg': 'https://down-br.img.susercontent.com/file/br-11134207-7r98o-m1zzq0be55us49',
    'img/review-15-c1-1.jpg': 'https://down-br.img.susercontent.com/file/br-11110105-7r98o-lr96mg3y7nja34',
    'img/review-15-c2-1.jpg': 'https://down-br.img.susercontent.com/file/br-11134207-7r98o-lqnmb7oulw6f02',
    'img/review-15-c3-1.jpg': 'https://down-br.img.susercontent.com/file/br-11134207-7r98o-lyzm72oahjk1ad',
    'img/review-15-c4-1.jpg': 'https://down-br.img.susercontent.com/file/br-11134207-7r98o-m1zzq0be55us49',
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
