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

# Download novas mídias do 107
download_file(
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/df6e0b005fbcff81e310302a27af5609~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=6935a35f&x-expires=1794405600&x-signature=ma1qX0aU%2B7GMu02CIm%2FfXT01GxE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
    "img/reviews-avatars/review-user-107-c1.jpg"
)
download_file(
    "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/2a5655d54a504e1a9a8aed38c97d8751~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
    "img/review-107-c1-1.jpg"
)

download_file(
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/67a1b7974a5d358239678fd7a6104a42~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=39e490d0&x-expires=1794405600&x-signature=v1TRTfwb4kEDuKFMgdb2%2Fo0tfps%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
    "img/reviews-avatars/review-user-107-c2.jpg"
)
download_file(
    "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/ac10b31832a14550918bf1e8ce37e29e~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
    "img/review-107-c2-1.jpg"
)

# Copia as fotos reais locais existentes para c3
import shutil
shutil.copy2("img/review-107-1.jpg", "img/review-107-c3-1.jpg")
shutil.copy2("img/review-107-2.jpg", "img/review-107-c3-2.jpg")
shutil.copy2("img/reviews-avatars/review-user-2.jpg", "img/reviews-avatars/review-user-107-c3.jpg")

revs_107 = [
    {
        "id": "c1",
        "name": "m**o p** m**s",
        "avatar": "../img/reviews-avatars/review-user-107-c1.jpg",
        "date": "16/02",
        "variation": "Aspirador 3 em 1",
        "comment": "Produto muito bom, simples e eficaz! Comprei pra limpar o carro e atendeu perfeitamente.",
        "photos": ["../img/review-107-c1-1.jpg"]
    },
    {
        "id": "c2",
        "name": "c**s s**a",
        "avatar": "../img/reviews-avatars/review-user-107-c2.jpg",
        "date": "25/09",
        "variation": "Preto Fosco",
        "comment": "Material: Bom. Eu amei, tamanho compacto e potência excelente de sucção e sopro.",
        "photos": ["../img/review-107-c2-1.jpg"]
    },
    {
        "id": "c3",
        "name": "r**o c**a",
        "avatar": "../img/reviews-avatars/review-user-107-c3.jpg",
        "date": "12/08",
        "variation": "Kit Completo com Bicos",
        "comment": "Chegou certinho com todos os adaptadores e o cabo de carregar. A função soprador é muito forte!",
        "photos": ["../img/review-107-c3-1.jpg", "../img/review-107-c3-2.jpg"]
    }
]

with open('reviews_107_real.json', 'w', encoding='utf-8') as f:
    json.dump(revs_107, f, ensure_ascii=False, indent=2)

with open('pages/produto-107.html', 'r', encoding='utf-8') as f:
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

for r in revs_107:
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

with open('pages/produto-107.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Patch applied to pages/produto-107.html!")
