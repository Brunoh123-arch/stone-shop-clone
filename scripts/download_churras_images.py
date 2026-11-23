import urllib.request, os

os.makedirs('img', exist_ok=True)

images = {
    'img/produto-14-1.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rdwx-lzpm7626yvg7c9',
    'img/produto-14-2.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rdx3-lzpm762qy23wb0',
    'img/produto-14-3.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rdyx-lzpm7733ia3ue2',
    'img/produto-14-4.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rdwz-lzpm76gmdrp06a',
    'img/review-14-c1-1.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rdx3-lzpm762qy23wb0',
    'img/review-14-c2-1.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rdwx-lzpm7626yvg7c9',
    'img/review-14-c3-1.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rdyx-lzpm7733ia3ue2',
    'img/review-14-c4-1.jpg': 'https://down-br.img.susercontent.com/file/sg-11134201-7rdwz-lzpm76gmdrp06a',
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
