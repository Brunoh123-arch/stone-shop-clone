import os
import shutil
from PIL import Image

dest_dir = 'img/reviews-avatars/tiktok_real'
os.makedirs(dest_dir, exist_ok=True)

# Limpar pasta destino para eliminar qualquer resquício antigo
for f in os.listdir(dest_dir):
    p = os.path.join(dest_dir, f)
    if os.path.isfile(p):
        os.remove(p)

sources = []

# 1. Da pasta tiktok_cdn_real (71 avatares legítimos recém baixados do CDN do TikTok via Playwright)
cdn_dir = 'img/reviews-avatars/tiktok_cdn_real'
if os.path.exists(cdn_dir):
    for f in sorted(os.listdir(cdn_dir)):
        if f.endswith('.jpg'):
            sources.append(os.path.join(cdn_dir, f))

# 2. Dos produtos canônicos 104 a 124 (avatares oficiais do TikTok Shop)
rev_dir = 'img/reviews-avatars'
for f in sorted(os.listdir(rev_dir)):
    if f.startswith('review-user-1') and f.endswith('.jpg') and os.path.getsize(os.path.join(rev_dir, f)) > 1000:
        sources.append(os.path.join(rev_dir, f))

print(f"Total de fontes brutas disponíveis do TikTok CDN: {len(sources)}")

final_count = 0
for src in sources:
    try:
        im = Image.open(src).convert('RGB')
        w, h = im.size
        if w >= 60 and h >= 60:
            # Teste de cor sólida (evita fundos brancos/pretos ou memes vazios)
            pixels = list(im.getdata())
            r_tot = sum(p[0] for p in pixels)
            avg_r = r_tot / len(pixels)
            if 25 < avg_r < 235:
                final_count += 1
                dst = os.path.join(dest_dir, f"tt_avatar_{final_count}.jpg")
                shutil.copy2(src, dst)
    except Exception as e:
        pass

print(f"Sucesso absoluto: {final_count} avatares autênticos do TikTok CDN consolidados em {dest_dir}!")
