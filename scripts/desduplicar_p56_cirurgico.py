import re

with open("pages/produto-56.html", "r", encoding="utf-8") as f:
    c = f.read()

idx_start = c.find('<div class="review-card"')
idx_end = c.find('<!-- PRODUTOS RELACIONADOS -->')

# Achar o último </div> antes de <!-- PRODUTOS RELACIONADOS -->
last_div_reviews = c.rfind('</div>', 0, idx_end)

reviews_block = c[idx_start:last_div_reviews]

cards = re.findall(r'<div class="review-card"[\s\S]*?(?=<div class="review-card"|\Z)', reviews_block)
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

print(f"P56: Reduzido de {len(cards)} para {len(unique_cards)} reviews únicas!")
new_block = "\n        ".join(unique_cards) + "\n      "

c_new = c[:idx_start] + new_block + c[last_div_reviews:]

div_o = len(re.findall(r'<div\b', c_new))
div_c = len(re.findall(r'</div>', c_new))
diff = div_o - div_c
print(f"P56: Diff = {diff}")

if diff == 0:
    with open("pages/produto-56.html", "w", encoding="utf-8") as f:
        f.write(c_new)
    print("P56 desduplicado e salvo com sucesso!")
