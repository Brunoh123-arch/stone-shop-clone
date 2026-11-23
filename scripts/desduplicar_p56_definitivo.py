import re

with open("pages/produto-56.html", "r", encoding="utf-8") as f:
    c = f.read()

idx_mais = c.find('id="mais-reviews-56"')
idx_end = c.find('<!-- PRODUTOS RELACIONADOS -->')

# Achar onde fecha mais-reviews-56
pos_btn = c.find('id="ver-mais-btn-56"', idx_mais)
# O fechamento de mais-reviews-56 fica antes de ver-mais-btn-56
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

print(f"P56 mais-reviews: Reduzido de {len(cards)} para {len(unique_cards)} reviews únicas!")

new_mais_block = 'id="mais-reviews-56" style="display:none">\n\n        ' + "\n        ".join(unique_cards) + "\n    "

c_new = c[:idx_mais] + new_mais_block + c[last_div_mais:]

div_o = len(re.findall(r'<div\b', c_new))
div_c = len(re.findall(r'</div>', c_new))
diff = div_o - div_c
print(f"P56: Diff = {diff}")

if diff == 0:
    with open("pages/produto-56.html", "w", encoding="utf-8") as f:
        f.write(c_new)
    print("P56 desduplicado com sucesso e Diff: 0!")
