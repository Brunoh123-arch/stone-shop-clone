import re

for pid in [20, 56, 98]:
    fpath = f"pages/produto-{pid}.html"
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    # Pegar todo o bloco de reviews-section
    rev_m = re.search(r'(<div class="reviews-section">[\s\S]*?)(<div class="shop-reviews-section"|<!-- Fim|\Z)', html)
    if not rev_m:
        print(f"P{pid}: Não achou reviews-section")
        continue

    sec = rev_m.group(1)
    # Header da seção (antes do primeiro review-card)
    first_card_pos = sec.find('<div class="review-card"')
    if first_card_pos == -1:
        continue

    header_part = sec[:first_card_pos]
    
    cards = re.findall(r'<div class="review-card"[\s\S]*?(?=<div class="review-card"|\Z)', sec[first_card_pos:])
    seen_texts = set()
    cleaned_cards = []

    for c in cards:
        text_m = re.search(r'<p class="review-comment">([^<]+)</p>', c)
        if text_m:
            txt = text_m.group(1).strip()
            if txt in seen_texts:
                continue
            seen_texts.add(txt)
        cleaned_cards.append(c.strip())

    new_sec = header_part + "\n        " + "\n        ".join(cleaned_cards) + "\n      </div>\n\n      "
    
    # Substituir no html original
    html_new = html[:rev_m.start(1)] + new_sec + html[rev_m.start(2):]
    
    div_o = len(re.findall(r'<div\b', html_new))
    div_c = len(re.findall(r'</div>', html_new))
    diff = div_o - div_c
    print(f"P{pid}: Reduzido para {len(cleaned_cards)} reviews únicas! Diff = {diff}")
    
    if diff == 0:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html_new)
        print(f"P{pid}: Salvo com sucesso!")
