import re

with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Dados limpos das 15 avaliacoes oficiais
reviews_clean = [
    {
        "name": "K**s M**a",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_1.jpg?v=1795139",
        "variation": "38/39 Preto",
        "date": "15/02",
        "comment": "A forma é perfeita, pedi a numeração que uso habitualmente e serviu como uma luva. O brilho dos strass é surreal de lindo ao vivo, super macio no pé!",
        "photos": [f"../img/review-104-c1-{i}.jpg?v=3" for i in range(1, 6)]
    },
    {
        "name": "I**a S**a",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_2.jpg?v=1795139",
        "variation": "40/41 Preto",
        "date": "14/02",
        "comment": "Simplesmente apaixonada! Veio no tamanho certinho, o acabamento das pedras brilha demais na luz e chegou super rápido pela Stone Shop. Melhor compra que fiz por aqui!",
        "photos": [f"../img/review-104-c2-{i}.jpg?v=3" for i in range(1, 6)]
    },
    {
        "name": "B**z L**a",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_3.jpg?v=1795139",
        "variation": "36/37 Bege",
        "date": "12/02",
        "comment": "Pedi o 36/37 e ficou perfeito no meu pé! Muito confortável para usar o dia todo, não machuca entre os dedos e a sola é bem macia. Com certeza vou pedir outra cor.",
        "photos": [f"../img/review-104-c3-{i}.jpg?v=3" for i in range(1, 6)]
    },
    {
        "name": "N**a R**o",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_4.jpg?v=1795139",
        "variation": "36/37 Bege",
        "date": "11/02",
        "comment": "Meninas, é muito mais bonita pessoalmente do que nas fotos! O tom bege é super chique, combina com qualquer roupa e as pedrarias são muito bem coladas. Amei demais!",
        "photos": [f"../img/review-104-c4-{i}.jpg?v=3" for i in range(1, 7)]
    },
    {
        "name": "T**a L**s",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_5.jpg?v=1795139",
        "variation": "38/39 Preto",
        "date": "10/02",
        "comment": "Confesso que estava com receio de comprar pela internet e não ser igual ao anúncio, mas me surpreendi demais. A qualidade é impressionante, acabamento premium!",
        "photos": [f"../img/review-104-c5-{i}.jpg?v=3" for i in range(1, 4)]
    },
    {
        "name": "D**a F**s",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_6.jpg?v=1795139",
        "variation": "38/39 Preto",
        "date": "08/02",
        "comment": "Recomendo de olhos fechados! Material de primeira, sola antiderrapante segura e os detalhes em strass dão um ar de riqueza. Já quero comprar a dourada também.",
        "photos": [f"../img/review-104-c6-{i}.jpg?v=3" for i in range(1, 6)]
    },
    {
        "name": "E**a S**a",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_7.jpg?v=1795139",
        "variation": "42/43 Grafite",
        "date": "07/02",
        "comment": "Chegou antes do prazo previsto, super bem embalado na caixinha. O chinelo é leve, elegante e calça super bem. Minha primeira compra na loja e virei fã!",
        "photos": [f"../img/review-104-c7-{i}.jpg?v=3" for i in range(1, 5)]
    },
    {
        "name": "S**a M**s",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_8.jpg?v=1795139",
        "variation": "36/37 Bege",
        "date": "05/02",
        "comment": "Maravilhoso! Super levinho no pé, não cansa nada. Uso tanto em casa quanto para passear no shopping ou praia. Brilha que é uma beleza!",
        "photos": [f"../img/review-104-c8-{i}.jpg?v=3" for i in range(1, 5)]
    },
    {
        "name": "K**a L**a",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_9.jpg?v=1795139",
        "variation": "38/39 Preto",
        "date": "04/02",
        "comment": "Lindo demais! Veio exatamente como vi nos vídeos aqui do TikTok Shop. As tiras são confortáveis e não machucam o peito do pé. Recomendo muito!",
        "photos": [f"../img/review-104-c9-{i}.jpg?v=3" for i in range(1, 4)]
    },
    {
        "name": "L**u D**e",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_10.jpg?v=1795139",
        "variation": "40/41 Preto",
        "date": "02/02",
        "comment": "Serviu perfeitamente seguindo a tabela de medidas. O produto é idêntico aos vídeos, bem acabado e de excelente durabilidade. Podem comprar sem medo!",
        "photos": [f"../img/review-104-c10-{i}.jpg?v=3" for i in range(1, 4)]
    },
    {
        "name": "M**e C**o",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_11.jpg?v=1795139",
        "variation": "42/43 Grafite",
        "date": "01/02",
        "comment": "Extremamente brilhoso e confortável! A entrega foi super ágil, chegou bem antes do previsto. Ficou certinho no meu pé, nota 10!",
        "photos": ["../img/review-104-c11-1.jpg?v=3"]
    },
    {
        "name": "A**e M**s",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_12.jpg?v=1795139",
        "variation": "36/37 Bege",
        "date": "29/01",
        "comment": "Amei e achei muito confortável! Se for comprar, recomendo pedir o número que você calça normalmente que dá certinho. O brilho é divino!",
        "photos": ["../img/review-104-c12-1.jpg?v=3"]
    },
    {
        "name": "J**e F**s",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_13.jpg?v=1795139",
        "variation": "38/39 Preto",
        "date": "28/01",
        "comment": "Os chinelos são lindos, macios e muito elegantes! Valem super a pena, o acabamento das pedras é impecável. Podem comprar sem receio!",
        "photos": ["../img/review-104-c13-1.jpg?v=3"]
    },
    {
        "name": "C**a B**a",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_14.jpg?v=1795139",
        "variation": "40/41 Preto",
        "date": "26/01",
        "comment": "Comprei para presentear minha irmã e ela simplesmente amou! Super resistente, sola macia e não escorrega em piso molhado. Entrega impecável da Stone Shop.",
        "photos": ["../img/review-104-c14-1.jpg?v=3"]
    },
    {
        "name": "V**a F**a",
        "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_15.jpg?v=1795139",
        "variation": "38/39 Preto",
        "date": "25/01",
        "comment": "Melhor custo-benefício que já encontrei! Produto de qualidade garantida, embalado com muito cuidado e entrega relâmpago. Recomendo a todas!",
        "photos": ["../img/review-104-branco.jpg?v=3"]
    }
]

star_svg = '<svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
five_stars = star_svg * 5

cards_html = []
for idx, r in enumerate(reviews_clean):
    photos_markup = ""
    if r['photos']:
        img_tags = "\n".join([f'  <img alt="Foto da avaliação" decoding="async" loading="lazy" src="{p}" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>' for p in r['photos']])
        photos_markup = f"""<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px; flex-wrap: wrap;">
{img_tags}
</div>"""

    card = f"""<!-- Avaliação {idx+1} Oficial TikTok Shop: {r['name']} ({r['variation']}) -->
<div class="review-card" data-author-avatar="{r['avatar']}" data-author-comment="{r['comment']}" data-author-date="{r['date']}" data-author-name="{r['name']}" data-author-stars="5" data-author-variation="{r['variation']}">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="{r['name']}" decoding="async" loading="lazy" src="{r['avatar']}"/>
</div>
<div class="review-user-info">
<div class="review-user-name">{r['name']}</div>
<div class="review-user-stars">{five_stars}</div>
<div class="review-date">{r['date']} · {r['variation']}</div>
</div>
</div>
</div>
<p class="review-comment">{r['comment']}</p>
{photos_markup}
</div>"""
    cards_html.append(card)

new_reviews_body = "\n".join(cards_html)

# Localizar ponto de insercao
cut_start_marker = '<div class="reviews-summary">'
cut_end_marker = '<!-- SOBRE ESTE PRODUTO:'

idx_sum = content.find(cut_start_marker)
idx_first_card = content.find('class="review-card"', idx_sum)
# Vamos pegar o final da div reviews-summary
idx_after_sum = content.find('</div>\n</div>', idx_sum) + len('</div>\n</div>')

idx_end = content.find(cut_end_marker)
# recuar ate o fechamento da secao de reviews
idx_before_about = content.rfind('</div>\n</div>', 0, idx_end)

print(f"Corte: {idx_after_sum} ate {idx_before_about}")

new_content = content[:idx_after_sum] + "\n" + new_reviews_body + "\n" + content[idx_before_about:]

with open('pages/produto-104.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("pages/produto-104.html REESCRITO COM SUCESSO ABSOLUTO!")
