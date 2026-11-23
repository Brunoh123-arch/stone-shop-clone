import urllib.request
import os
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def download_file(url, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if '~tplv-aphluv4xwc' in url:
        base = url.split('~tplv-aphluv4xwc')[0]
        url = base + '~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg'
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(out_path, 'wb') as f:
                f.write(data)
            print(f"Downloaded: {out_path} ({len(data)} bytes)")
            return True
    except Exception as e:
        print(f"Error {url} -> {out_path}: {e}")
        return False

# Download novas fotos do 109
download_file(
    "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/34aaf5377a744a00a16ca96c31a00ea0~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
    "img/review-109-c1-1.jpg"
)
download_file(
    "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/26b522e7a1ba4575b65e40294131ffbf~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
    "img/review-109-c1-2.jpg"
)
download_file(
    "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/1d7e049928e846b0a2fb40e905c0cc59~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
    "img/review-109-c2-1.jpg"
)
download_file(
    "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/3ba5a700f202444498e76c6c7f96aabe~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
    "img/review-109-c2-2.jpg"
)

import shutil
shutil.copy2("img/review-109-real-1.jpg", "img/review-109-c3-1.jpg")
shutil.copy2("img/review-109-real-2.jpg", "img/review-109-c3-2.jpg")
shutil.copy2("img/review-109-real-3.jpg", "img/review-109-c4-1.jpg")
shutil.copy2("img/review-109-real-4.jpg", "img/review-109-c4-2.jpg")

shutil.copy2("img/reviews-avatars/review-user-1.jpg", "img/reviews-avatars/review-user-109-c1.jpg")
shutil.copy2("img/reviews-avatars/review-user-2.jpg", "img/reviews-avatars/review-user-109-c2.jpg")
shutil.copy2("img/reviews-avatars/review-user-3.jpg", "img/reviews-avatars/review-user-109-c3.jpg")
shutil.copy2("img/reviews-avatars/review-user-4.jpg", "img/reviews-avatars/review-user-109-c4.jpg")

revs_109 = [
    {
        "id": "c1",
        "name": "K**a S**a",
        "avatar": "../img/reviews-avatars/review-user-109-c1.jpg",
        "date": "17/11",
        "variation": "Branco Perolado, Bivolt",
        "comment": "Incrível como é bom esse modelador. Carrega rápido, deixa o cabelo com aspecto natural e super leve. Chegou muito antes do esperado.",
        "photos": ["../img/review-109-c1-1.jpg", "../img/review-109-c1-2.jpg"]
    },
    {
        "id": "c2",
        "name": "K**a R**s",
        "avatar": "../img/reviews-avatars/review-user-109-c2.jpg",
        "date": "17/11",
        "variation": "Branco Perolado, Bivolt",
        "comment": "Perfeito. Muito prático, leve e com resultado ótimo. Chegou muuuuito rápido.",
        "photos": ["../img/review-109-c2-1.jpg", "../img/review-109-c2-2.jpg"]
    },
    {
        "id": "c3",
        "name": "J**a M**a",
        "avatar": "../img/reviews-avatars/review-user-109-c3.jpg",
        "date": "24/10",
        "variation": "Cinza Chumbo, Bivolt",
        "comment": "Amei demais! Cachos perfeitos em segundos sem queimar a mão nem o cabelo. Esquenta na medida certa.",
        "photos": ["../img/review-109-c3-1.jpg", "../img/review-109-c3-2.jpg"]
    },
    {
        "id": "c4",
        "name": "B**a F**e",
        "avatar": "../img/reviews-avatars/review-user-109-c4.jpg",
        "date": "08/10",
        "variation": "Rosa Quartzo, Bivolt",
        "comment": "Excelente qualidade, bateria dura para fazer a cabeça toda tranquilamente. Super recomendo!",
        "photos": ["../img/review-109-c4-1.jpg", "../img/review-109-c4-2.jpg"]
    }
]

with open('reviews_109_real.json', 'w', encoding='utf-8') as f:
    json.dump(revs_109, f, ensure_ascii=False, indent=2)

with open('pages/produto-109.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Atualizar ratings-row com (4)
html = re.sub(
    r'(<div class="ratings-row"[^>]*>.*?<span style="color:#666;font-size:12px;">)\(\d+\)(</span>)',
    r'\g<1>(4)\g<2>',
    html,
    flags=re.DOTALL
)

# 2. Gerar cards
cards_html = []
star_svg = '<svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
stars_5 = star_svg * 5

for r in revs_109:
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
        <h3 class="reviews-header">Avaliações dos clientes (4)</h3>
        <div class="reviews-summary" style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
          <span class="review-avg">4,9</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            {stars_5}
          </div>
        </div>

{cards_joined}

        <button class="see-all-reviews" id="btn-see-all-reviews" onclick="abrirModalAvaliacoes()">Ver todas as 4 avaliações</button>
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

with open('pages/produto-109.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Patch applied to pages/produto-109.html!")
