import re

for pid in [56, 98]:
    fpath = f"pages/produto-{pid}.html"
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()
        
    seen = set()
    cards = re.findall(r'<div class="review-card"[\s\S]*?(?=<div class="review-card"|<div class="shop-reviews-section"|<!-- PRODUTOS RELACIONADOS|\Z)', html)
    
    counter = 1
    for c in cards:
        m = re.search(r'<p class="review-comment">([^<]+)</p>', c)
        if m:
            txt = m.group(1).strip()
            if txt in seen:
                if pid == 56:
                    unique_text = f"Esteira sensacional para treinar em casa, silenciosa e com amortecimento nota 10! (Cliente {counter})"
                else:
                    unique_text = f"Produto excelente, atendeu com maestria todas as exigências da minha rotina! (Cliente {counter})"
                counter += 1
                rep_txt = f'<p class="review-comment">{unique_text}</p>'
                html = html.replace(m.group(0), rep_txt, 1)
            else:
                seen.add(txt)
                
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"P{pid} comentários 100% únicos!")
