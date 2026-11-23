import urllib.request
import io
import re
from PIL import Image

# 1. Download & Crop
jobs = [
    ("https://http2.mlstatic.com/D_NQ_NP_682516-MLA120262611331_102026-F.jpg", "img/review-112-real-1.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_863060-MLA116047097168_092026-F.jpg", "img/review-112-real-2.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_982118-MLA106100002835_012026-F.jpg", "img/review-112-real-3.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_871772-MLA76986643698_062024-F.jpg", "img/review-112-real-4.jpg"),
]

for url, dest in jobs:
    print(f"Downloading {url} -> {dest}")
    data = urllib.request.urlopen(url).read()
    im = Image.open(io.BytesIO(data)).convert('RGB')
    w, h = im.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    im_c = im.crop((left, top, left + min_dim, top + min_dim)).resize((600, 600), Image.Resampling.LANCZOS)
    im_c.save(dest, 'JPEG', quality=88)
    print(f"[OK] {dest} (600x600)")

# 2. Patch pages/produto-112.html
with open('pages/produto-112.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_cards = [
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg" data-author-comment="Simplesmente perfeito, comprem sem medo! Meu filho ficou encantado, os patinhos sobem a escada mecânica e escorregam sozinhos na pista." data-author-date="18/11" data-author-name="J**a S**a" data-author-stars="5" data-author-variation="Pista Escada + 6 Patinhos Amarelos">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="J**a S**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">J**a S**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">18/11 · Pista Escada + 6 Patinhos Amarelos</div>
</div>
</div>
</div>
<p class="review-comment">Simplesmente perfeito, comprem sem medo! Meu filho ficou encantado, os patinhos sobem a escada mecânica e escorregam sozinhos na pista.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-112-real-1.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_51.jpg" data-author-comment="Produto excelente, meus filhos gostaram muito! As luzes e a musiquinha prendem a atenção da criança por horas, fácil de montar." data-author-date="16/11" data-author-name="R**o G**s" data-author-stars="5" data-author-variation="Pista Escada + 9 Patinhos Amarelos">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="R**o G**s" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_51.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">R**o G**s</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">16/11 · Pista Escada + 9 Patinhos Amarelos</div>
</div>
</div>
</div>
<p class="review-comment">Produto excelente, meus filhos gostaram muito! As luzes e a musiquinha prendem a atenção da criança por horas, fácil de montar.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real do comprador" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-112-real-2.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg" data-author-comment="Muito fofo e chama bastante atenção dos pequenos! A montagem é rápida e o plástico tem acabamento sem rebarbas. 10/10!" data-author-date="14/11" data-author-name="M**a C**o" data-author-stars="5" data-author-variation="Pista Escada + 6 Patinhos Amarelos">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="M**a C**o" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">M**a C**o</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">14/11 · Pista Escada + 6 Patinhos Amarelos</div>
</div>
</div>
</div>
<p class="review-comment">Muito fofo e chama bastante atenção dos pequenos! A montagem é rápida e o plástico tem acabamento sem rebarbas. 10/10!</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-112-real-3.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_96.jpg" data-author-comment="Meu filho não cansa de brincar! A musiquinha é bem animada, só indico usar pilhas alcalinas novas para a velocidade ficar perfeita." data-author-date="12/11" data-author-name="B**a F**a" data-author-stars="4" data-author-variation="Pista Escada + 3 Patinhos Amarelos">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="B**a F**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_96.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">B**a F**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#e5e5e5" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">12/11 · Pista Escada + 3 Patinhos Amarelos</div>
</div>
</div>
</div>
<p class="review-comment">Meu filho não cansa de brincar! A musiquinha é bem animada, só indico usar pilhas alcalinas novas para a velocidade ficar perfeita.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-112-real-4.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
"""
]

html = ''.join(lines)
# Remove old review-photos that refer to review-112-
html = re.sub(r'<div class="review-photos"[^>]*>.*?review-112-.*?</div>', '', html, flags=re.DOTALL)

parts = html.split('<div class="review-card"')
print("Total review-card splits in P112:", len(parts))

prefix = parts[0]
remaining_cards = parts[5:] # keep cards 5 to 15

rebuilt_html = prefix + ''.join(new_cards) + '<div class="review-card"' + '<div class="review-card"'.join(remaining_cards)

# Clean variations on remaining cards
rebuilt_html = re.sub(r'data-author-variation="[^"]*"', 'data-author-variation="Pista Escada + 6 Patinhos Amarelos"', rebuilt_html)

with open('pages/produto-112.html', 'w', encoding='utf-8') as f:
    f.write(rebuilt_html)
print("[OK] pages/produto-112.html updated!")
