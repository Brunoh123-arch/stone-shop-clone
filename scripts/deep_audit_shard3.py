import os
import re

ids = [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 68, 70, 72, 73, 74, 75, 76]

competitors_pattern = re.compile(r'\b(shopee|shope|aliexpress|ali express|magalu|magazine luiza|amazon|mercado livre|mercadolivre)\b', re.I)

print("="*80)
print("DEEP AUDIT SHARD 3 - DETALHES POR PRODUTO")
print("="*80)

for pid in ids:
    filepath = f"pages/produto-{pid}.html"
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    title_m = re.search(r'<title>(.*?)</title>', html, re.I)
    title = title_m.group(1).strip() if title_m else 'Sem Titulo'

    # Check 1: Creators section
    cs_match = re.search(r'<div[^>]*id=["\']creators-section["\'][^>]*>', html)
    cs_tag = cs_match.group(0) if cs_match else 'NAO EXISTE'
    cs_hidden = 'display: none' in cs_tag or 'display:none' in cs_tag

    # Check 2: Video in description
    vid_block = 'product-video-block' in html or 'tt-product-video' in html
    vid_srcs = re.findall(r'<video[^>]+src=["\']([^"\']+)["\']', html)
    
    # Check 3: Reviews with images
    rev_cards = re.findall(r'<div class="review-card".*?</div>\s*</div>', html, re.DOTALL)
    photos = re.findall(r'<img[^>]+class=["\'][^"\']*review-photo[^"\']*["\'][^>]*src=["\']([^"\']+)["\']', html)
    if not photos:
        photos = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*review-photo[^"\']*["\']', html)
        
    # Check competitor words in reviews
    comp_matches = competitors_pattern.findall(html)
    
    # Check redirects
    has_redirect = 'location.replace' in html or 'http-equiv="refresh"' in html

    print(f"\n[P{pid}] {title[:60]}")
    print(f"  CS Tag: {cs_tag} (Hidden={cs_hidden})")
    print(f"  Video Block: {vid_block} | URLs: {vid_srcs}")
    print(f"  Reviews: {len(rev_cards)} cards | Photos: {len(photos)} -> {photos[:4]}")
    if comp_matches:
        print(f"  [ALERTA CONCORRENTES]: {set(comp_matches)}")
    if has_redirect:
        print(f"  [ALERTA REDIRECT]: Encontrado redirect em P{pid}!")
