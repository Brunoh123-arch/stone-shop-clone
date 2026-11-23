import os
import re

ids = [52, 53, 54, 55, 57, 58, 59, 60, 63, 64, 65, 68, 70, 72, 73]

for pid in ids:
    filepath = f"pages/produto-{pid}.html"
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    title_m = re.search(r'<title>(.*?)</title>', html, re.I)
    title = title_m.group(1).strip() if title_m else 'Sem Titulo'

    # Find cards that have review-photo
    rev_cards = re.findall(r'<div class="review-card".*?</div>\s*</div>', html, re.DOTALL)
    photo_cards = []
    for rc in rev_cards:
        if 'review-photo' in rc or 'review-photos' in rc:
            comm = re.search(r'data-author-comment=["\'](.*?)["\']', rc)
            comm_text = comm.group(1) if comm else ''
            var = re.search(r'<div class="review-date">(.*?)</div>', rc)
            var_text = var.group(1) if var else ''
            imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', rc)
            photo_cards.append((var_text, comm_text, [img for img in imgs if 'avatar' not in img]))

    print(f"\n[P{pid}] {title[:40]}")
    for var, comm, imgs in photo_cards:
        print(f"   Var: {var} | Imgs: {imgs} | Comment: {comm[:80]}")
