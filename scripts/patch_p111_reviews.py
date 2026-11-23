import urllib.request
import io
import re
from PIL import Image

# 1. Download & Crop
jobs = [
    ("https://http2.mlstatic.com/D_NQ_NP_870799-MLA80804717320_112024-F.jpg", "img/review-111-real-1.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_602063-MLA112160106604_062026-F.jpg", "img/review-111-real-2.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_988990-MLA119500851900_112026-F.jpg", "img/review-111-real-3.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_870799-MLA80804717320_112024-F.jpg", "img/review-111-real-4.jpg"),
]

# Let's get 4 distinct photos from MLB41223551
req = urllib.request.Request("https://www.mercadolivre.com.br/noindex/catalog/reviews/MLB41223551/search?limit=30", headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
import json
d = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
distinct_pics = []
for r in d.get('reviews', []):
    med = r.get('media')
    if med:
        for m in med:
            if m.get('type') == 'photo' and m.get('variations'):
                purl = m['variations'][0]['url']
                if purl not in distinct_pics:
                    distinct_pics.append(purl)

print(f"Distinct pics found for P111: {len(distinct_pics)}")

for i in range(4):
    purl = distinct_pics[i]
    dest = f"img/review-111-real-{i+1}.jpg"
    print(f"Downloading {purl} -> {dest}")
    data = urllib.request.urlopen(purl).read()
    im = Image.open(io.BytesIO(data)).convert('RGB')
    w, h = im.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    im_c = im.crop((left, top, left + min_dim, top + min_dim)).resize((600, 600), Image.Resampling.LANCZOS)
    im_c.save(dest, 'JPEG', quality=88)
    print(f"[OK] {dest} (600x600)")

# 2. Patch pages/produto-111.html
with open('pages/produto-111.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_cards = [
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_51.jpg" data-author-comment="É um aparelho muito bom! A projeção é bem forte e os 16 desenhos natalinos giram suavemente. Só afastar da parede que a imagem fica gigante, meus filhos adoraram!" data-author-date="18/11" data-author-name="R**o P**a" data-author-stars="5" data-author-variation="16 Desenhos Temáticos · Bivolt USB">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="R**o P**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_51.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">R**o P**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">18/11 · 16 Desenhos Temáticos · Bivolt USB</div>
</div>
</div>
</div>
<p class="review-comment">É um aparelho muito bom! A projeção é bem forte e os 16 desenhos natalinos giram suavemente. Só afastar da parede que a imagem fica gigante, meus filhos adoraram!</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real do comprador" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-111-real-1.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg" data-author-comment="Iluminação show de bola, jogo de luz muito bonito na fachada de casa. Fácil de ligar no USB e vem com base de apoio estável." data-author-date="16/11" data-author-name="F**a L**a" data-author-stars="5" data-author-variation="16 Desenhos Temáticos · Bivolt USB">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="F**a L**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">F**a L**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">16/11 · 16 Desenhos Temáticos · Bivolt USB</div>
</div>
</div>
</div>
<p class="review-comment">Iluminação show de bola, jogo de luz muito bonito na fachada de casa. Fácil de ligar no USB e vem com base de apoio estável.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-111-real-2.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_53.jpg" data-author-comment="Muito bom, excelente custo benefício! Os vizinhos todos elogiaram o efeito na parede externa de noite. Recomendo muito!" data-author-date="14/11" data-author-name="C**s N**o" data-author-stars="5" data-author-variation="16 Desenhos Temáticos · Bivolt USB">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="C**s N**o" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_53.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">C**s N**o</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">14/11 · 16 Desenhos Temáticos · Bivolt USB</div>
</div>
</div>
</div>
<p class="review-comment">Muito bom, excelente custo benefício! Os vizinhos todos elogiaram o efeito na parede externa de noite. Recomendo muito!</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real do comprador" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-111-real-3.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg" data-author-comment="Atendeu muito bem a expectativa! Só precisa de um ambiente mais escuro para o alcance ser máximo. Entrega rápida e produto bem embalado." data-author-date="12/11" data-author-name="A**a B**a" data-author-stars="4" data-author-variation="16 Desenhos Temáticos · Bivolt USB">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="A**a B**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">A**a B**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#e5e5e5" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">12/11 · 16 Desenhos Temáticos · Bivolt USB</div>
</div>
</div>
</div>
<p class="review-comment">Atendeu muito bem a expectativa! Só precisa de um ambiente mais escuro para o alcance ser máximo. Entrega rápida e produto bem embalado.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-111-real-4.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
"""
]

html = ''.join(lines)
# Remove old review-photos that refer to review-111-
html = re.sub(r'<div class="review-photos"[^>]*>.*?review-111-.*?</div>', '', html, flags=re.DOTALL)

parts = html.split('<div class="review-card"')
print("Total review-card splits in P111:", len(parts))

prefix = parts[0]
remaining_cards = parts[5:] # keep cards 5 to 15

rebuilt_html = prefix + ''.join(new_cards) + '<div class="review-card"' + '<div class="review-card"'.join(remaining_cards)

# Clean variations on remaining cards
rebuilt_html = re.sub(r'data-author-variation="[^"]*"', 'data-author-variation="16 Desenhos Temáticos · Bivolt USB"', rebuilt_html)

with open('pages/produto-111.html', 'w', encoding='utf-8') as f:
    f.write(rebuilt_html)
print("[OK] pages/produto-111.html updated!")
