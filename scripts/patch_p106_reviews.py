import urllib.request
import io
import re
from PIL import Image

# 1. Download & Crop
jobs = [
    ("https://http2.mlstatic.com/D_NQ_NP_873973-MLA111093758301_042026-F.jpg", "img/review-106-real-1.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_836727-MLA114919752323_072026-F.jpg", "img/review-106-real-2.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_622292-MLA96081216013_102025-F.jpg", "img/review-106-real-3.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_772609-MLA93800521594_102025-F.jpg", "img/review-106-real-4.jpg"),
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

# 2. Patch pages/produto-106.html
with open('pages/produto-106.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_cards = [
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg" data-author-comment="Material muito bom e resistente! Modela muito bem a cintura e não marca sob a roupa nem em vestidos justos. Valeu muito a pena!" data-author-date="18/11" data-author-name="J**a S**a" data-author-stars="5" data-author-variation="Bege · M">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="J**a S**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">J**a S**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">18/11 · Bege · M</div>
</div>
</div>
</div>
<p class="review-comment">Material muito bom e resistente! Modela muito bem a cintura e não marca sob a roupa nem em vestidos justos. Valeu muito a pena!</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-106-real-1.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg" data-author-comment="Eu amei minha compra, realmente cumpre o que promete! Aperta e modela sem sufocar, o tecido é respirável e super confortável no dia a dia." data-author-date="16/11" data-author-name="C**a M**a" data-author-stars="5" data-author-variation="Preto · G">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="C**a M**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">C**a M**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">16/11 · Preto · G</div>
</div>
</div>
</div>
<p class="review-comment">Eu amei minha compra, realmente cumpre o que promete! Aperta e modela sem sufocar, o tecido é respirável e super confortável no dia a dia.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-106-real-2.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_96.jpg" data-author-comment="Excelente body modelador! A compressão na barriga é perfeita e o acabamento não enrola nas pernas. Segui a tabela de medidas certinho." data-author-date="14/11" data-author-name="B**a F**a" data-author-stars="4" data-author-variation="Bege · GG">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="B**a F**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_96.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">B**a F**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#e5e5e5" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">14/11 · Bege · GG</div>
</div>
</div>
</div>
<p class="review-comment">Excelente body modelador! A compressão na barriga é perfeita e o acabamento não enrola nas pernas. Segui a tabela de medidas certinho.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-106-real-3.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_98.jpg" data-author-comment="O produto é maravilhoso! Qualidade excelente, costura reforçada e o fecho embaixo é super prático. Não fico mais sem!" data-author-date="12/11" data-author-name="L**a R**s" data-author-stars="5" data-author-variation="Preto · P">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="L**a R**s" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_98.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">L**a R**s</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">12/11 · Preto · P</div>
</div>
</div>
</div>
<p class="review-comment">O produto é maravilhoso! Qualidade excelente, costura reforçada e o fecho embaixo é super prático. Não fico mais sem!</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-106-real-4.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
"""
]

# Find start of reviews and replace review-cards
html = ''.join(lines)
# Remove old review-photos that refer to review-106-
html = re.sub(r'<div class="review-photos"[^>]*>.*?review-106-.*?</div>', '', html, flags=re.DOTALL)

# Find first review card
first_card_idx = html.find('<div class="review-card"')
# Find 5th review card
parts = html.split('<div class="review-card"')
print("Total review-card splits:", len(parts))

prefix = parts[0]
remaining_cards = parts[5:] # keep cards 5 to 15

rebuilt_html = prefix + ''.join(new_cards) + '<div class="review-card"' + '<div class="review-card"'.join(remaining_cards)

# Clean variations on remaining cards
rebuilt_html = re.sub(r'data-author-variation="[^"]*"', 'data-author-variation="Bege · M"', rebuilt_html)

with open('pages/produto-106.html', 'w', encoding='utf-8') as f:
    f.write(rebuilt_html)
print("[OK] pages/produto-106.html updated!")
