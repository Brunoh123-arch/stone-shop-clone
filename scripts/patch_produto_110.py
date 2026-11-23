import shutil
import json
import re

shutil.copy2("img/review-110-clean-1.jpg", "img/review-110-c1-1.jpg")
shutil.copy2("img/review-110-clean-2.jpg", "img/review-110-c1-2.jpg")
shutil.copy2("img/review-110-clean-3.jpg", "img/review-110-c2-1.jpg")
shutil.copy2("img/review-110-clean-4.jpg", "img/review-110-c2-2.jpg")
shutil.copy2("img/review-110-clean-5.jpg", "img/review-110-c3-1.jpg")
shutil.copy2("img/review-110-clean-6.jpg", "img/review-110-c3-2.jpg")

shutil.copy2("img/reviews-avatars/review-user-1.jpg", "img/reviews-avatars/review-user-110-c1.jpg")
shutil.copy2("img/reviews-avatars/review-user-2.jpg", "img/reviews-avatars/review-user-110-c2.jpg")
shutil.copy2("img/reviews-avatars/review-user-3.jpg", "img/reviews-avatars/review-user-110-c3.jpg")

revs_110 = [
    {
        "id": "c1",
        "name": "C**s M**a",
        "avatar": "../img/reviews-avatars/review-user-110-c1.jpg",
        "date": "14/09",
        "variation": "Preto/Dourado, 41",
        "comment": "Tênis surpreendeu demais pelo conforto e acabamento. O amortecimento Pulse RX é muito macio na pisada. Chegou em 3 dias!",
        "photos": ["../img/review-110-c1-1.jpg", "../img/review-110-c1-2.jpg"]
    },
    {
        "id": "c2",
        "name": "M**a S**a",
        "avatar": "../img/reviews-avatars/review-user-110-c2.jpg",
        "date": "28/08",
        "variation": "Marinho/Laranja, 38",
        "comment": "Comprei pra caminhada e esteira. É super leve e a forma é perfeita. Recomendo pegar o tamanho normal de uso.",
        "photos": ["../img/review-110-c2-1.jpg", "../img/review-110-c2-2.jpg"]
    },
    {
        "id": "c3",
        "name": "R**l G**s",
        "avatar": "../img/reviews-avatars/review-user-110-c3.jpg",
        "date": "05/08",
        "variation": "Chumbo/Verde, 42",
        "comment": "Excelente custo benefício. Veio na caixa original da Kappa, costuras e sola muito bem acabadas. 10/10!",
        "photos": ["../img/review-110-c3-1.jpg", "../img/review-110-c3-2.jpg"]
    }
]

with open('reviews_110_real.json', 'w', encoding='utf-8') as f:
    json.dump(revs_110, f, ensure_ascii=False, indent=2)

with open('pages/produto-110.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Atualizar ratings-row com (3)
html = re.sub(
    r'(<div class="ratings-row"[^>]*>.*?<span style="color:#666;font-size:12px;">)\(\d+\)(</span>)',
    r'\g<1>(3)\g<2>',
    html,
    flags=re.DOTALL
)

# 2. Gerar cards
cards_html = []
star_svg = '<svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
stars_5 = star_svg * 5

for r in revs_110:
    name = r['name']
    av_src = r['avatar']
    var = r['variation']
    date = r['date']
    comment = r['comment']
    
    photos_html = []
    for p_src in r['photos']:
        photos_html.append(f'<img class="review-photo" src="{p_src}" alt="" style="width:70px;height:70px;object-fit:cover;border-radius:8px;cursor:pointer;" onclick="abrirFotoReview(this)">')
    
    photos_str = '\n          '.join(photos_html)
    
    card = f'''        <div class="review-card" data-author-name="{name}" data-author-avatar="{av_src}" data-author-stars="5" data-author-variation="{var}" data-author-date="{date}" data-author-comment="{comment}">
          <div class="review-header"><div class="review-user">
            <div class="review-avatar"><img src="{av_src}" alt="" width="32" height="32" style="border-radius:50%;object-fit:cover;" onerror="this.src=\'../img/reviews-avatars/review-user-1.jpg\'"></div>
            <div class="review-user-info">
              <div class="review-user-name">{name}</div>
              <div class="review-user-stars">{stars_5}</div>
              <div class="review-date">{date} · {var}</div>
            </div>
          </div></div>
          <p class="review-comment">{comment}</p>
          <div class="review-photos">
          {photos_str}
          </div>
        </div>'''
    cards_html.append(card)

cards_joined = '\n\n'.join(cards_html)

new_reviews_section = f'''<div class="reviews-section">
        <h3 class="reviews-header">Avaliações dos clientes (3)</h3>
        <div class="reviews-summary" style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
          <span class="review-avg">4,9</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            {stars_5}
          </div>
        </div>

{cards_joined}

        <button class="see-all-reviews" id="btn-see-all-reviews" onclick="abrirModalAvaliacoes()">Ver todas as 3 avaliações</button>
      </div>'''

# Substitui a reviews-section inteira
html = re.sub(
    r'<div class="reviews-section">.*?(?=<div class="about-product-section"|<div class="description-section")',
    new_reviews_section + '\n\n      ',
    html,
    flags=re.DOTALL
)

# Corrige fechamento de about-product-section se necessário
if '</div><!-- fim about-product-section -->' not in html:
    html = re.sub(
        r'(</button>\s*</div>)(\s*<!-- DESCRI[^\n]*-->)',
        r'\1\n      </div><!-- fim about-product-section -->\2',
        html
    )

with open('pages/produto-110.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Patch applied to pages/produto-110.html!")
