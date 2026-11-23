import re

html_path = 'pages/produto-104.html'
with open(html_path, 'r', encoding='utf-8', errors='surrogatepass') as f:
    content = f.read()

# Update top rating count
content = re.sub(
    r'(<span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document\.querySelector\(\'\.reviews-section\'\)\?\.scrollIntoView\(\{behavior:\'smooth\'\}\)">)\(\d+\)(</span>)',
    r'\g<1>(14)\g<2>',
    content
)

# Update reviews-header
content = re.sub(
    r'<h3 class="reviews-header">Avaliações dos clientes \([^\)]*\)</h3>',
    r'<h3 class="reviews-header">Avaliações dos clientes (14)</h3>',
    content
)

star_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
five_stars = star_svg * 5

reviews_data = [
    {
        "id": "c1",
        "name": "K**s",
        "avatar": "../img/reviews-avatars/review-user-104-c1.jpg",
        "variation": "CARAMELO, 35/36",
        "date": "20/10",
        "comment": "Forma normal, pedir a numeração que uso e veio certinho, ótimo preço, entrega foi muito rápido, pensei que demoraria mais, comprarei mais em outras cores",
        "photos": [f"../img/review-104-c1-{i}.jpg?v=3" for i in range(1, 6)]
    },
    {
        "id": "c2",
        "name": "S**a M.",
        "avatar": "../img/reviews-avatars/review-user-104-c2.jpg",
        "variation": "BRANCO, 37/38",
        "date": "29/09",
        "comment": "Simplesmente perfeito. Veio do tamanho certo , brilha demais , chegou rápido. Melhor comprar que fiz aqui",
        "photos": [f"../img/review-104-c2-{i}.jpg?v=3" for i in range(1, 6)]
    },
    {
        "id": "c3",
        "name": "J**a",
        "avatar": "../img/reviews-avatars/review-user-104-c3.jpg",
        "variation": "CARAMELO, 37/38",
        "date": "21/09",
        "comment": "Forma e tamanho: Pedi a 37/38 ficou perfeita no meu pé, muito confortável. E sem contar que é linda.",
        "photos": [f"../img/review-104-c3-{i}.jpg?v=3" for i in range(1, 6)]
    },
    {
        "id": "c4",
        "name": "k**e R**e R**u",
        "avatar": "../img/reviews-avatars/review-user-104-c4.jpg",
        "variation": "BRANCO, 35/36",
        "date": "17/09",
        "comment": "Forma e tamanho: 35 cor branca Muito linda ameiiii",
        "photos": [f"../img/review-104-c4-{i}.jpg?v=3" for i in range(1, 7)]
    },
    {
        "id": "c5",
        "name": "S**a",
        "avatar": "../img/reviews-avatars/review-user-104-c5.jpg",
        "variation": "BRANCO, 37/38",
        "date": "25/09",
        "comment": "Eu estava com medo de comprar e não ser do mesmo jeito que estava na propaganda. Mas quando chegou fiquei impressionada com a qualidade e conforto do produto. Com certeza",
        "photos": [f"../img/review-104-c5-{i}.jpg?v=3" for i in range(1, 4)]
    },
    {
        "id": "c6",
        "name": "k**\ud83d\udc9f",
        "avatar": "../img/reviews-avatars/review-user-104-c6.jpg",
        "variation": "BRANCO, 37/38",
        "date": "07/09",
        "comment": "Recomendo para quem for comprar muito bonita material bom detalhes bonitos calço 37 comprei um 37/38 e ficou excelente no meu pé vou comprar mas uma novamente mas em outra cor Cor: Branca Usabilidade: Boa Aroma: Bom Forma e tamanho: 37/38",
        "photos": [f"../img/review-104-c6-{i}.jpg?v=3" for i in range(1, 6)]
    },
    {
        "id": "c7",
        "name": "A**1",
        "avatar": "../img/reviews-avatars/review-user-104-c7.jpg",
        "variation": "BRANCO, 37/38",
        "date": "25/08",
        "comment": "Chegou no prazo certo, muito linda ela, amei gente super recomendo, foi a minha primeira compra no tiktok eu amei \ud83d\ude0d Cor: Branca Aroma: Muito cheirosa ela Forma e tamanho: Tanha 37:38 perfeita",
        "photos": [f"../img/review-104-c7-{i}.jpg?v=3" for i in range(1, 5)]
    },
    {
        "id": "c8",
        "name": "e**h",
        "avatar": "../img/reviews-avatars/review-user-104-c8.jpg",
        "variation": "CARAMELO, 37/38",
        "date": "07/07",
        "comment": "Linda e muito confortável Calço 36 mas pedi o 37 e ficou muito boa Forma e tamanho: Bom Cor: Perfeita Aroma: Sem cheiro Usabilidade: Para qualquer lugar",
        "photos": [f"../img/review-104-c8-{i}.jpg?v=3" for i in range(1, 5)]
    },
    {
        "id": "c9",
        "name": "C**e C**\ud83d\udc06",
        "avatar": "../img/reviews-avatars/review-user-104-c9.jpg",
        "variation": "CARAMELO, 37/38",
        "date": "15/07",
        "comment": "Lindas. Forma e tamanho: Bom Aroma: Nenhum Usabilidade: Boa Cor: Cores bonitas",
        "photos": [f"../img/review-104-c9-{i}.jpg?v=3" for i in range(1, 4)]
    },
    {
        "id": "c10",
        "name": "L**a L**",
        "avatar": "../img/reviews-avatars/review-user-104-c10.jpg",
        "variation": "BRANCO, 35/36",
        "date": "02/09",
        "comment": "Cor: Igual anúncio Forma e tamanho: Serviu direitinho conforme medidas de pesquisa Usabilidade: Para varias ocasiões. Chegou dentro do prazo. O único problema e q pedi com brilho em toda lateral, mas não veio Mas, vou ficar assim mesmo, pq gostei muito",
        "photos": [f"../img/review-104-c10-{i}.jpg?v=3" for i in range(1, 4)]
    },
    {
        "id": "c11",
        "name": "2**_",
        "avatar": "../img/reviews-avatars/review-user-104-c11.jpg",
        "variation": "BRANCO, 35/36",
        "date": "16/07",
        "comment": "Eu gostei demais, extremamente lindo e brilhoso. Recomendo super e chegou no dentro do prazo certinho. Lembrando que eu peguei 35/36 e eu uso 36, e ficou bem certinho",
        "photos": [f"../img/review-104-c11-1.jpg?v=3"]
    },
    {
        "id": "c12",
        "name": "K**n G**s",
        "avatar": "../img/reviews-avatars/review-user-104-c12.jpg",
        "variation": "PRETO, 35/36",
        "date": "29/08",
        "comment": "Amei e achei muito confortável, se for comprar compra o número que usa certinho",
        "photos": [f"../img/review-104-c12-1.jpg?v=3"]
    },
    {
        "id": "c13",
        "name": "L**a C**a",
        "avatar": "../img/reviews-avatars/review-user-104-c13.jpg",
        "variation": "BRANCO, 39/0",
        "date": "10/10",
        "comment": "Forma e tamanho: Padrão Aroma: Sem Usabilidade: Perfeita Cor: Linda Os chinelos são lindos… Valem super a pena! Podem comprar sem medo! \ud83e\udd0d",
        "photos": [f"../img/review-104-c13-1.jpg?v=3"]
    },
    {
        "id": "c14",
        "name": "V**a L**a R**g",
        "avatar": "../img/reviews-avatars/review-user-104-c14.jpg",
        "variation": "BRANCO, 37/38",
        "date": "07/11",
        "comment": "Ela nao é branca é creme",
        "photos": [f"../img/review-104-c14-1.jpg?v=3"]
    }
]

cards_html = []
for idx, r in enumerate(reviews_data):
    photos_html = "\n".join([
        f'            <img loading="lazy" decoding="async" class="review-photo" src="{p}" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">'
        for p in r['photos']
    ])
    card = f"""        <!-- Avaliação {idx+1} Oficial TikTok Shop: {r['name']} ({r['variation']}) com {len(r['photos'])} fotos reais -->
        <div class="review-card" data-author-name="{r['name']}" data-author-avatar="{r['avatar']}" data-author-stars="5" data-author-variation="{r['variation']}" data-author-date="{r['date']}" data-author-comment="{r['comment']}">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="{r['avatar']}" alt="{r['name']}">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">{r['name']}</div>
                <div class="review-user-stars">{five_stars}</div>
                <div class="review-date">{r['date']} · {r['variation']}</div>
              </div>
            </div>
          </div>
          <p class="review-comment">{r['comment']}</p>
          <div class="review-photos">
{photos_html}
          </div>
        </div>"""
    cards_html.append(card)

all_cards_str = "\n\n".join(cards_html)

pattern = r'(<div class="reviews-summary">[\s\S]*?</div>\s*)([\s\S]*?)(\s*</div><style id="tt-sobre-produto-style">)'

m = re.search(pattern, content)
if not m:
    print("ERROR: Could not find reviews section pattern!")
else:
    new_content = content[:m.start(2)] + "\n" + all_cards_str + "\n      " + content[m.end(2):]
    with open(html_path, 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(new_content)
    print("SUCCESS: produto-104.html updated!")

# Verify tag depth
with open(html_path, 'r', encoding='utf-8', errors='surrogatepass') as f:
    c = f.read()
opens = len(re.findall(r'<div[\s>]', c))
closes = len(re.findall(r'</div>', c))
diff = opens - closes
print(f"P104 diff: {diff} (opens={opens}, closes={closes})")
