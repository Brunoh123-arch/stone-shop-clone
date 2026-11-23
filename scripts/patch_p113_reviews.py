import urllib.request
import io
import re
from PIL import Image

# 1. Download & Crop
jobs = [
    ("https://http2.mlstatic.com/D_NQ_NP_801035-MLA84290762429_052025-F.jpg", "img/review-113-real-1.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_917515-MLA82545348785_022025-F.jpg", "img/review-113-real-2.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_774777-MLA84519735382_052025-F.jpg", "img/review-113-real-3.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_681306-MLA75751350960_042024-F.jpg", "img/review-113-real-4.jpg"),
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

# 2. Patch pages/produto-113.html
with open('pages/produto-113.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_cards = [
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg" data-author-comment="O pote duplo é muito lindo e moderno! As tigelas são removíveis e super fáceis de lavar. A inclinação de 15 graus ajudou muito na digestão dos meus gatos." data-author-date="18/11" data-author-name="J**a S**a" data-author-stars="5" data-author-variation="Tigela Dupla Transparente">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="J**a S**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">J**a S**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">18/11 · Tigela Dupla Transparente</div>
</div>
</div>
</div>
<p class="review-comment">O pote duplo é muito lindo e moderno! As tigelas são removíveis e super fáceis de lavar. A inclinação de 15 graus ajudou muito na digestão dos meus gatos.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-113-real-1.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg" data-author-comment="Os potinhos são muito lindos, deram um charme na cozinha! Tenho gatos e a ração não se espalha mais pelo chão. Chegou bem embalado." data-author-date="16/11" data-author-name="M**a C**o" data-author-stars="5" data-author-variation="Tigela Dupla Transparente">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="M**a C**o" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">M**a C**o</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">16/11 · Tigela Dupla Transparente</div>
</div>
</div>
</div>
<p class="review-comment">Os potinhos são muito lindos, deram um charme na cozinha! Tenho gatos e a ração não se espalha mais pelo chão. Chegou bem embalado.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-113-real-2.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_51.jpg" data-author-comment="Achei super prático e higiênico! A altura é perfeita para o conforto da coluna do pet. Material acrílico resistente e firme no chão." data-author-date="14/11" data-author-name="R**o G**s" data-author-stars="5" data-author-variation="Tigela Dupla Transparente">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="R**o G**s" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_51.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">R**o G**s</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">14/11 · Tigela Dupla Transparente</div>
</div>
</div>
</div>
<p class="review-comment">Achei super prático e higiênico! A altura é perfeita para o conforto da coluna do pet. Material acrílico resistente e firme no chão.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real do comprador" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-113-real-3.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_96.jpg" data-author-comment="O produto é muito bonito e bem acabado! Para quem tem gatos ou cachorros pequenos atende 100%. Recomendo!" data-author-date="12/11" data-author-name="B**a F**a" data-author-stars="4" data-author-variation="Tigela Dupla Transparente">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="B**a F**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_96.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">B**a F**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#e5e5e5" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">12/11 · Tigela Dupla Transparente</div>
</div>
</div>
</div>
<p class="review-comment">O produto é muito bonito e bem acabado! Para quem tem gatos ou cachorros pequenos atende 100%. Recomendo!</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-113-real-4.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
"""
]

html = ''.join(lines)
# Remove old review-photos that refer to review-113-
html = re.sub(r'<div class="review-photos"[^>]*>.*?review-113-.*?</div>', '', html, flags=re.DOTALL)

parts = html.split('<div class="review-card"')
print("Total review-card splits in P113:", len(parts))

prefix = parts[0]
remaining_cards = parts[5:] # keep cards 5 to 15

rebuilt_html = prefix + ''.join(new_cards) + '<div class="review-card"' + '<div class="review-card"'.join(remaining_cards)

# Clean variations on remaining cards
rebuilt_html = re.sub(r'data-author-variation="[^"]*"', 'data-author-variation="Tigela Dupla Transparente"', rebuilt_html)

with open('pages/produto-113.html', 'w', encoding='utf-8') as f:
    f.write(rebuilt_html)
print("[OK] pages/produto-113.html updated!")
