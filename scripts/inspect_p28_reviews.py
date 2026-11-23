# -*- coding: utf-8 -*-
with open('pages/produto-28.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
# Achar todas as tags de imagem nas avaliações
reviews_section = html[html.find('class="reviews-section"'):]

review_items = re.findall(r'<div[^>]*class=["\']review-item["\'][^>]*>(.*?)</div>\s*</div>\s*</div>', reviews_section, re.DOTALL)
if not review_items:
    # outro seletor de review
    review_items = re.findall(r'<div[^>]*class=["\']review-card["\'][^>]*>(.*?)(?=<div[^>]*class=["\']review-card|\s*<div class="reviews-pagination|\s*<footer|\s*</section|\s*</main)', reviews_section, re.DOTALL)

print(f"Total de reviews encontradas: {len(review_items)}")
for i, r in enumerate(review_items):
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', r)
    unboxing_imgs = [img for img in imgs if 'avatar' not in img and 'star' not in img and 'icon' not in img]
    if unboxing_imgs:
        name = re.findall(r'<div class="review-author[^"]*">([^<]+)</div>', r) or re.findall(r'<span class="review-author[^"]*">([^<]+)</span>', r) or re.findall(r'<div class="review-name[^"]*">([^<]+)</div>', r)
        print(f"\n--- REVIEW {i+1} ---")
        print("Autor:", name)
        print("Fotos de unboxing:", unboxing_imgs)
        # Mostrar um trecho do texto
        txt = re.sub(r'<[^>]+>', ' ', r)
        print("Texto:", ' '.join(txt.split())[:120])
