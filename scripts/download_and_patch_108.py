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

revs_108 = [
    {
        "id": "c1",
        "name": "H**y P**z",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/fcd3e7bea311288744e02c1cc4a526d4~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=f3e2ab67&x-expires=1794405600&x-signature=w82TlE%2BEzfSclSpW2C4hqIvMeTA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "16/10",
        "variation": "Rosa, 110V",
        "comment": "Confesso que quando comprei, já estava preparada para devolver, mas o produto acabou de chegar e testei no mesmo momento. Adorei produto de boa qualidade, secou meu cabelo rapidinho, meninas podem comprar sem medo, pelo preço que paguei o produto é ótimo.",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/9031be4bba5e43819daae951f46696dd~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/a896c744d6904c6ca7b4bf7552a3421c~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/eddec0803f5d4bc984692dab3e6d6ca1~tplv-aphluv4xwc-crop-webp:300:300.webp"
        ]
    },
    {
        "id": "c2",
        "name": "Y**💋",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/6ed2d0d8c709c4c70b05b3182f76727c~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=de166e23&x-expires=1794405600&x-signature=2Dq7DHcmyZS4mcVX%2BH9gaEkTY0k%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "22/10",
        "variation": "Rosa, 110V",
        "comment": "Simplesmente maravilhoso!!! Seca o cabelo super rápido. Super útil meninas só comprem… Veio tudo certinho a embalagem não veio amassada e chegou antes do prazo.",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/bbe0c8894f424e7591f1b005b0923611~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/2dbf3390a30944e49a705849b803718a~tplv-aphluv4xwc-crop-webp:300:300.webp"
        ]
    },
    {
        "id": "c3",
        "name": "M**a G**s",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/b1088027c2f3971ec9626f132ece073b~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=20e200a2&x-expires=1794405600&x-signature=PUpCrurbFR%2Fv6h6G6fBEpbHJ5ek%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "18/10",
        "variation": "Rosa, 110V",
        "comment": "Chegou super rápido. Seca o cabelo rápido (considerando que tenho cabelo fino e em quantidade média). Amei o modelador. É muito leve.",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/c0c643c48de643aa8328b0c769066a77~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/425de6a5e648435eac05b7a8a2311783~tplv-aphluv4xwc-crop-webp:300:300.webp"
        ]
    }
]

with open('reviews_108_real.json', 'w', encoding='utf-8') as f:
    json.dump(revs_108, f, ensure_ascii=False, indent=2)

for r in revs_108:
    rid = r['id']
    av_path = f"img/reviews-avatars/review-user-108-{rid}.jpg"
    download_file(r['avatar'], av_path)
    for idx, p_url in enumerate(r['photos']):
        p_path = f"img/review-108-{rid}-{idx+1}.jpg"
        download_file(p_url, p_path)

with open('pages/produto-108.html', 'r', encoding='utf-8') as f:
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

for r in revs_108:
    rid = r['id']
    name = r['name']
    av_src = f"../img/reviews-avatars/review-user-108-{rid}.jpg"
    var = r['variation']
    date = r['date']
    comment = r['comment']
    
    photos_html = []
    for idx in range(len(r['photos'])):
        p_src = f"../img/review-108-{rid}-{idx+1}.jpg"
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

with open('pages/produto-108.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Patch applied to pages/produto-108.html!")
