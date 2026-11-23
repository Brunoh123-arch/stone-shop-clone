import re

reviews_data = [
    {
        "name": "M**a S.",
        "avatar": "../img/reviews-avatars/review-user-104-vanessa.jpg?v=1794225",
        "date": "12/10",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "O kit de praia mais completo que já vi! O carrinho da Mor vira mesinha com porta copos, cabe as 4 cadeiras, o guarda-sol e o cooler de 18L certinho em cima!",
        "photos": ["../img/review-18-c1-1.jpg", "../img/review-18-c1-2.jpg"]
    },
    {
        "name": "C**s E.",
        "avatar": "../img/reviews-avatars/review-user-104-juliana.jpg?v=1794225",
        "date": "08/10",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "As cadeiras reclináveis são maravilhosas, super leves em alumínio e têm 4 posições. Deitam bem pra tomar sol na praia. Recomendo demais!",
        "photos": ["../img/review-18-c2-1.jpg", "../img/review-18-c2-2.jpg"]
    },
    {
        "name": "F**a R.",
        "avatar": "../img/reviews-avatars/review-user-1.jpg",
        "date": "04/10",
        "variation": "Azul, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "O cooler de 18 litros segurou o gelo e a cerveja o dia inteiro geladinha no sol quente de Ubatuba. Qualidade Mor top!",
        "photos": ["../img/review-18-c3-1.jpg"]
    },
    {
        "name": "R**o S.",
        "avatar": "../img/reviews-avatars/review-user-2.jpg",
        "date": "29/09",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "Chegou tudo perfeitamente embalado na caixa original da Mor. O saca areia facilita muito pra firmar o guarda-sol no vento forte.",
        "photos": ["../img/review-18-c4-1.jpg"]
    },
    {
        "name": "A**a O.",
        "avatar": "../img/reviews-avatars/review-user-3.jpg",
        "date": "24/09",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "Muito prático pra levar pra praia com a família. O carrinho puxa super leve na areia fofa e virando mesa não suja nada de areia.",
        "photos": ["../img/review-18-c5-1.jpg"]
    },
    {
        "name": "J**a L.",
        "avatar": "../img/reviews-avatars/review-user-4.jpg",
        "date": "19/09",
        "variation": "Vermelha, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "Material de primeira linha, alumínio não enferruja com a maresia. As cores das cadeiras vieram lindas e bem vivas!",
        "photos": ["../img/review-18-c6-1.jpg"]
    },
    {
        "name": "L**s M.",
        "avatar": "../img/reviews-avatars/review-user-5.jpg",
        "date": "14/09",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "Comprei pro feriado e foi a melhor aquisição do ano. O cooler cabe bastante lata e as cadeiras são confortáveis demais.",
        "photos": ["../img/review-18-c7-1.jpg"]
    },
    {
        "name": "T**o B.",
        "avatar": "../img/reviews-avatars/review-user-6.jpg",
        "date": "09/09",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "Excelente custo-benefício, comprar separado na loja física ia sair mais de mil reais. Chegou em 4 dias aqui em Santos.",
        "photos": ["../img/review-18-c8-1.jpg"]
    },
    {
        "name": "B**a N.",
        "avatar": "../img/reviews-avatars/review-user-7.jpg",
        "date": "03/09",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "Carrinho muito resistente, aguenta o peso de tudo e ainda sobra espaço pra estender as toalhas. Recomendo de olhos fechados!",
        "photos": []
    },
    {
        "name": "P**o V.",
        "avatar": "../img/reviews-avatars/review-user-8.jpg",
        "date": "28/08",
        "variation": "Azul, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "Amei demais o kit! O guarda sol tem proteção UV e a regulagem de inclinação é perfeita quando o sol vai baixando na praia.",
        "photos": []
    },
    {
        "name": "G**a F.",
        "avatar": "../img/reviews-avatars/review-user-104-c13.jpg?v=1794225",
        "date": "21/08",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "Tudo original da Mor, acabamento reforçado. Minha esposa e meus filhos adoraram, praia agora é outro nível.",
        "photos": []
    },
    {
        "name": "D**o M.",
        "avatar": "../img/reviews-avatars/review-user-104-c14.jpg?v=1794225",
        "date": "16/08",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "Entrega super rápida da Stone Shop! Veio tudo certinho, 4 cadeiras, cooler, carrinho mesa, guarda-sol e o saca areia.",
        "photos": []
    },
    {
        "name": "E**a T.",
        "avatar": "../img/reviews-avatars/review-user-104-juliana.jpg?v=1794225",
        "date": "10/08",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "As cadeiras são bem largas e confortáveis, não machucam as pernas. O carrinho como mesa é a melhor invenção.",
        "photos": []
    },
    {
        "name": "H**o K.",
        "avatar": "../img/reviews-avatars/review-user-1.jpg",
        "date": "05/08",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "Muito leve pra carregar no porta-malas do carro, cabe tudo dobradinho. Qualidade Mor dispensa comentários.",
        "photos": []
    },
    {
        "name": "V**a L.",
        "avatar": "../img/reviews-avatars/review-user-104-vanessa.jpg?v=1794225",
        "date": "30/07",
        "variation": "Sortidas, Kit Completo 4 Cadeiras + Carrinho + Cooler",
        "comment": "Sensacional! Fomos pra praia no fim de semana e todo mundo perguntou onde compramos esse kit completo. Nota 10!",
        "photos": []
    }
]

star_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
stars_5_html = star_svg * 5

cards_html = []
for r in reviews_data:
    photos_html = ""
    if r["photos"]:
        imgs = "".join([f'<img loading="lazy" decoding="async" class="review-photo" src="{p}" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">' for p in r["photos"]])
        photos_html = f'<div class="review-photos">{imgs}</div>'
    
    card = f"""<div class="review-card" data-author-name="{r['name']}" data-author-avatar="{r['avatar']}" data-author-stars="5" data-author-variation="{r['variation']}" data-author-date="{r['date']}" data-author-comment="{r['comment']}">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img loading="lazy" decoding="async" src="{r['avatar']}" alt="{r['name']}">
</div>
<div class="review-user-info">
<div class="review-user-name">{r['name']}</div>
<div class="review-user-stars">{stars_5_html}</div>
<div class="review-date">{r['date']} · {r['variation']}</div>
</div>
</div>
</div>
<p class="review-comment">{r['comment']}</p>
{photos_html}
</div>"""
    cards_html.append(card)

new_reviews_list_content = "\n".join(cards_html)

with open('pages/produto-18.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace <div class="reviews-list">...</div>
pattern = r'(<div class="reviews-list">)[\s\S]*?(</div>\s*<!-- Fim da Lista de Avaliações -->|</div>\s*</section>)'
match = re.search(pattern, html)
if match:
    new_section = match.group(1) + "\n" + new_reviews_list_content + "\n</div>\n</section>"
    html = html[:match.start()] + new_section + html[match.end():]
    print("Replaced reviews-list in pages/produto-18.html!")
else:
    print("reviews-list pattern not matched! Trying broader match...")
    pattern2 = r'(<div class="reviews-list">)[\s\S]*?(</section>)'
    html = re.sub(pattern2, r'\1\n' + new_reviews_list_content + r'\n</div>\n\2', html, count=1)
    print("Broad replacement performed!")

with open('pages/produto-18.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("pages/produto-18.html updated with 15 canonical reviews!")
