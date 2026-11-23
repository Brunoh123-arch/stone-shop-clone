import re

for pid in [20, 98]:
    fpath = f"pages/produto-{pid}.html"
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()

    idx_mais = c.find(f'id="mais-reviews-{pid}"')
    if idx_mais != -1:
        pos_btn = c.find(f'id="ver-mais-btn-{pid}"', idx_mais)
        last_div_mais = c.rfind('</div>', idx_mais, pos_btn)
        mais_block = c[idx_mais:last_div_mais]
        cards = re.findall(r'<div class="review-card"[\s\S]*?(?=<div class="review-card"|\Z)', mais_block)
        seen_texts = set()
        unique_cards = []
        for card in cards:
            txt_m = re.search(r'<p class="review-comment">([^<]+)</p>', card)
            if txt_m:
                txt = txt_m.group(1).strip()
                if txt in seen_texts:
                    continue
                seen_texts.add(txt)
            unique_cards.append(card.strip())
        print(f"P{pid} mais-reviews: {len(cards)} -> {len(unique_cards)} únicas")
        new_mais_block = f'id="mais-reviews-{pid}" style="display:none">\n\n        ' + "\n        ".join(unique_cards) + "\n    "
        c_new = c[:idx_mais] + new_mais_block + c[last_div_mais:]
        div_o = len(re.findall(r'<div\b', c_new))
        div_c = len(re.findall(r'</div>', c_new))
        diff = div_o - div_c
        print(f"P{pid}: Diff = {diff}")
        if diff == 0:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(c_new)
            print(f"P{pid} desduplicado com sucesso!")
    else:
        print(f"P{pid}: Não tem mais-reviews-{pid}")
