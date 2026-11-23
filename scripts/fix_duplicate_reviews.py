import os
import glob
import re
from collections import Counter

def clean_duplicate_photos_in_page(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Procurar todos os blocos de review-card
    # Estrutura padrão: <div class="review-card" ... > ... </div>
    # Vamos achar cada <div class="review-photos" ... >...</div>
    
    # 1. Checar se há repetição de imagem no mesmo arquivo
    all_photos = re.findall(r'<img[^>]+class=[\'"][^\'"]*review-photo[^\'"]*[\'"][^>]+src=[\'"]([^\'"]+)[\'"]', html)
    if not all_photos:
        all_photos = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"][^>]+class=[\'"][^\'"]*review-photo[^\'"]*[\'"]', html)

    counts = Counter(all_photos)
    duplicates = {k: v for k, v in counts.items() if v > 1}

    if not duplicates:
        return 0

    print(f"[*] Corrigindo duplicatas em {html_path}: {duplicates}")

    # Separar o HTML por <div class="review-card"
    splits = html.split('<div class="review-card"')
    prefix = splits[0]
    cards = splits[1:]

    seen_photos = set()
    new_cards = []

    for card in cards:
        full_card = '<div class="review-card"' + card
        # Encontrar fotos dentro desse card
        card_photos = re.findall(r'<img[^>]+class=[\'"][^\'"]*review-photo[^\'"]*[\'"][^>]+src=[\'"]([^\'"]+)[\'"]', full_card)
        if not card_photos:
            card_photos = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"][^>]+class=[\'"][^\'"]*review-photo[^\'"]*[\'"]', full_card)

        cleaned_card = full_card
        for p in card_photos:
            if p in seen_photos:
                # Se já vimos essa foto antes, removemos ela deste card!
                # Remove a tag <img ... src="p" ... />
                pattern = rf'<img[^>]+src=[\'"]{re.escape(p)}[\'"][^>]*\/?>'
                cleaned_card = re.sub(pattern, '', cleaned_card)
                # Se sobrar <div class="review-photos">\s*</div>, remove o container vazio
                cleaned_card = re.sub(r'<div class="review-photos"[^>]*>\s*</div>', '', cleaned_card)
            else:
                seen_photos.add(p)

        # Remove o <div class="review-card" do inicio antes de dar append
        if cleaned_card.startswith('<div class="review-card"'):
            cleaned_card = cleaned_card[len('<div class="review-card"'):]
        new_cards.append(cleaned_card)

    rebuilt_html = prefix + '<div class="review-card"' + '<div class="review-card"'.join(new_cards)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(rebuilt_html)

    return len(duplicates)

pages = sorted(glob.glob('pages/produto-*.html'), key=lambda p: int(re.search(r'produto-(\d+)', p).group(1)))
total_fixed = 0
for p in pages:
    fixed = clean_duplicate_photos_in_page(p)
    if fixed > 0:
        total_fixed += 1

print(f"\n[SUCESSO] Total de paginas com fotos de unboxing duplicadas corrigidas: {total_fixed}")
