import urllib.request
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# URLs do Magazine Luiza / Casas Bahia / MadeiraMadeira
urls = [
    "https://www.magazineluiza.com.br/busca/forno+eletrico+hq+48+litros+hq48d/",
    "https://www.casasbahia.com.br/forno-eletrico-hq-48-litros/b"
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # encontra links de imagens
            imgs = re.findall(r'https://[^\s"\']+\.(?:jpg|png|webp)', html)
            print(f"URL {u[:40]} -> {len(imgs)} imagens encontradas")
            hq_imgs = [i for i in imgs if any(k in i.lower() for k in ['forno', 'hq', 'eletro', 'product', '800x800', '1000x1000', '700x700'])]
            print(f"  Filtradas: {len(hq_imgs)}")
            for img in hq_imgs[:5]:
                print(f"    {img}")
    except Exception as e:
        print(f"Erro em {u[:40]}: {e}")
