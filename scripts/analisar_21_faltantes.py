import os
import re

missing_pids = [19, 23, 24, 25, 26, 34, 38, 40, 41, 45, 46, 50, 53, 54, 60, 64, 68, 72, 75, 82, 88]

# Carregar catalogo
with open('js/catalogo.js', encoding='utf-8') as f:
    cat_text = f.read()

items_raw = re.findall(r'\{\s*id:\s*(\d+)\s*,\s*nome:\s*[\'"]([^\'"]+)[\'"]', cat_text)
cat_map = {int(pid): nome for pid, nome in items_raw}

print(f"=== ANALISANDO OS {len(missing_pids)} PRODUTOS SEM CRIADORES ===")
for pid in missing_pids:
    pfile = f"pages/produto-{pid}.html"
    nome = cat_map.get(pid, "Desconhecido")
    if os.path.exists(pfile):
        with open(pfile, encoding='utf-8') as f:
            html = f.read()
        
        # Checar se tem vídeo no HTML
        vids = re.findall(r'<video[^>]+src=[\'"]([^\'"]+)[\'"]', html)
        # Checar fotos de unboxing
        photos = re.findall(r'<div class=[\'"]review-photos[\'"][^>]*>(.*?)</div>', html, re.DOTALL)
        photo_count = 0
        if photos:
            for blk in photos:
                photo_count += len(re.findall(r'<img', blk))
        
        print(f"P{pid:02d} [{nome[:35]}]: Videos HTML: {len(vids)} | Unboxing photos: {photo_count}")
    else:
        print(f"P{pid:02d} [{nome[:35]}]: ARQUIVO NÃO EXISTE")
