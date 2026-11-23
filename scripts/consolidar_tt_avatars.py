import re
import os
import urllib.request

urls = set()
for s in ['scripts/baixar_avatares_tiktok.py', 'scripts/baixar_avatares_tiktok_2.py', 'scripts/baixar_avatares_tiktok_3.py']:
    if os.path.exists(s):
        with open(s, 'r', encoding='utf-8') as f:
            text = f.read()
            found = re.findall(r'(https://p\d+-[^"\s]+)', text)
            urls.update(found)

print(f"Total de URLs unicas encontradas: {len(urls)}")

os.makedirs('img/reviews-avatars/tiktok_real', exist_ok=True)

success = 0
for i, url in enumerate(sorted(urls)):
    dest = f"img/reviews-avatars/tiktok_real/tt_avatar_{i+1}.jpg"
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        success += 1
        continue
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as resp, open(dest, 'wb') as out:
            out.write(resp.read())
        if os.path.getsize(dest) > 1000:
            success += 1
            print(f"[{i+1}/{len(urls)}] Baixado: {dest} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"Erro em {i+1}: {e}")

print(f"Sucesso total em disco: {success} avatares reais do TikTok CDN!")
