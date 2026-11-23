import urllib.request
import re

url = "https://www.hqeletro.com.br/forno-eletrico-hq-48-litros-hq48d-1600w-preto-hq48d-/p"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Encoding': 'identity'
})
try:
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print(f"Texto puro decodificado: {len(content)} chars")
        with open('hq_decompressed.html', 'w', encoding='utf-8') as f:
            f.write(content)
        imgs = re.findall(r'https://[^\s"\']+\.(?:jpg|png|webp)', content)
        print(f"Total imgs: {len(imgs)}")
        for img in list(dict.fromkeys(imgs))[:15]:
            print("  IMG:", img)
except Exception as e:
    print("Erro:", e)
