import re

# 1. Atualizar produto-35.html para usar os avatares REAIS do TikTok recém-extraídos
with open("pages/produto-35.html", "r", encoding="utf-8") as f:
    p35_content = f.read()

# Substituir avatares das 8 avaliações de P35 pelos novos avatares oficiais do TikTok CDN
p35_content = p35_content.replace("../img/reviews-avatars/unique/m_5.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_2.jpg")
p35_content = p35_content.replace("../img/reviews-avatars/unique/w_12.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_3.jpg")
p35_content = p35_content.replace("../img/reviews-avatars/unique/m_18.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_4.jpg")
p35_content = p35_content.replace("../img/reviews-avatars/unique/w_25.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_6.jpg")
p35_content = p35_content.replace("../img/reviews-avatars/unique/m_22.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_8.jpg")
p35_content = p35_content.replace("../img/reviews-avatars/unique/m_31.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_10.jpg")
p35_content = p35_content.replace("../img/reviews-avatars/unique/w_44.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_12.jpg")
p35_content = p35_content.replace("../img/reviews-avatars/unique/m_41.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_14.jpg")

with open("pages/produto-35.html", "w", encoding="utf-8") as f:
    f.write(p35_content)
print("Produto 35: Avatares atualizados com fotos reais do TikTok CDN!")

# 2. Desduplicar comentários em P56, P98 e P20
for pid in [20, 56, 98]:
    fpath = f"pages/produto-{pid}.html"
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Encontrar cards de review e desduplicar comentários repetidos
    cards = re.findall(r'<div class="review-card"[\s\S]*?(?=<div class="review-card"|<div class="shop-reviews-section"|<!-- Fim|\Z)', html)
    seen_texts = set()
    cleaned_cards = []
    
    for c in cards:
        text_m = re.search(r'<p class="review-comment">([^<]+)</p>', c)
        if text_m:
            txt = text_m.group(1).strip()
            if txt in seen_texts:
                continue
            seen_texts.add(txt)
        cleaned_cards.append(c)
        
    if len(cleaned_cards) < len(cards):
        print(f"Produto {pid}: Reduzido de {len(cards)} para {len(cleaned_cards)} avaliações 100% únicas (removidas {len(cards) - len(cleaned_cards)} duplicatas)!")
        # Achar início do primeiro card e fim do último card
        first_card_pos = html.find('<div class="review-card"')
        last_card_end = html.find('</div>\n      <div class="shop-reviews-section"', first_card_pos)
        if last_card_end == -1:
            last_card_end = html.find('<div class="shop-reviews-section"', first_card_pos)
        if last_card_end == -1:
            last_card_end = html.find('</div>\n<!-- PRODUTOS RELACIONADOS', first_card_pos)
            
        if first_card_pos != -1 and last_card_end != -1:
            new_cards_html = "\n".join(cleaned_cards)
            html = html[:first_card_pos] + new_cards_html + "\n      </div>\n\n      " + html[last_card_end:]
            
            div_o = len(re.findall(r'<div\b', html))
            div_c = len(re.findall(r'</div>', html))
            diff = div_o - div_c
            print(f"Produto {pid}: Diff = {diff}")
            if diff == 0:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"Produto {pid}: Salvo com sucesso!")
