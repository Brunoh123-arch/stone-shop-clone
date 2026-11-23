import urllib.request
import re
import json

url = "https://www.hqeletro.com.br/forno-eletrico-hq-48-litros-hq48d-1600w-preto-hq48d-/p"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"HTML baixado: {len(html)} bytes")
        
        # Procura por imagens da VTEX / hqeletro
        imgs = re.findall(r'https://hqeletro\.vtexassets\.com/arquivos/ids/\d+[^\s"\']+', html)
        if not imgs:
            imgs = re.findall(r'https://[^\s"\']*?vteximg\.com\.br/arquivos/ids/\d+[^\s"\']+', html)
        if not imgs:
            imgs = re.findall(r'https://[^\s"\']*?/arquivos/ids/\d+[^\s"\']+', html)
            
        print(f"Total de imagens oficiais encontradas: {len(imgs)}")
        unique_imgs = list(dict.fromkeys(imgs))
        for idx, img in enumerate(unique_imgs[:10]):
            print(f"  Foto {idx+1}: {img}")
            
        # Procura descrição
        desc_match = re.search(r'<div[^>]*class="[^"]*product-description[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        if desc_match:
            print("Descrição encontrada!")
        else:
            # tenta pegar do JSON-LD
            json_lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
            print(f"JSON-LD encontrados: {len(json_lds)}")
            for j in json_lds:
                try:
                    data = json.loads(j)
                    if data.get('@type') == 'Product':
                        print("Produto JSON-LD:")
                        print("Nome:", data.get('name'))
                        print("Descrição:", data.get('description')[:200])
                        print("Imagens:", data.get('image'))
                        print("Ofertas:", data.get('offers'))
                except Exception:
                    pass

except Exception as e:
    print("Erro ao acessar hqeletro:", e)
