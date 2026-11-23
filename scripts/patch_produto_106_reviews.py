import re
import json

with open('pages/produto-106.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('reviews_106_real.json', 'r', encoding='utf-8') as f:
    revs = json.load(f)

# 1. Atualizar ratings-row com (6)
html = re.sub(
    r'(<div class="ratings-row"[^>]*>.*?<span style="color:#666;font-size:12px;">)\(\d+\)(</span>)',
    r'\g<1>(6)\g<2>',
    html,
    flags=re.DOTALL
)

# 2. Gerar cards
cards_html = []
star_svg = '<svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
stars_5 = star_svg * 5

for r in revs:
    rid = r['id']
    name = r['name']
    var = r['variation']
    date = r['date']
    comment = r['comment']
    
    if r['avatar']:
        av_src = f"../img/reviews-avatars/review-user-106-{rid}.jpg"
    else:
        av_src = "../img/reviews-avatars/review-user-1.jpg"
    
    photos_html = []
    for idx in range(len(r['photos'])):
        p_src = f"../img/review-106-{rid}-{idx+1}.jpg"
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
        <h3 class="reviews-header">Avaliações dos clientes (6)</h3>
        <div class="reviews-summary" style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
          <span class="review-avg">4,9</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            {stars_5}
          </div>
        </div>

{cards_joined}

        <button class="see-all-reviews" id="btn-see-all-reviews" onclick="abrirModalAvaliacoes()">Ver todas as 6 avaliações</button>
      </div>'''

# Substitui a reviews-section inteira
html = re.sub(
    r'<div class="reviews-section">.*?(?=<div class="about-product-section"|<div class="description-section")',
    new_reviews_section + '\n\n      ',
    html,
    flags=re.DOTALL
)

# Salva
with open('pages/produto-106.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Patch applied to pages/produto-106.html!")
