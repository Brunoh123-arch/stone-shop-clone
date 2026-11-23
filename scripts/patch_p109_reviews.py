import urllib.request
import io
import re
from PIL import Image

# 1. Download & Crop
jobs = [
    ("https://http2.mlstatic.com/D_NQ_NP_976316-MLA71561804222_092023-F.jpg", "img/review-109-real-1.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_835998-MLA83472582776_042025-F.jpg", "img/review-109-real-2.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_911080-MLA72996788266_112023-F.jpg", "img/review-109-real-3.jpg"),
    ("https://http2.mlstatic.com/D_NQ_NP_768622-MLA73306802866_122023-F.jpg", "img/review-109-real-4.jpg"),
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

# 2. Patch pages/produto-109.html
with open('pages/produto-109.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_cards = [
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg" data-author-comment="Amei, estou apaixonada! Fiz o teste nas pontas de tarde e de noite ainda estavam intactas, cachos perfeitos e sem esforço nenhum." data-author-date="18/11" data-author-name="J**a S**a" data-author-stars="5" data-author-variation="Cinza e Roxo">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="J**a S**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">J**a S**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">18/11 · Cinza e Roxo</div>
</div>
</div>
</div>
<p class="review-comment">Amei, estou apaixonada! Fiz o teste nas pontas de tarde e de noite ainda estavam intactas, cachos perfeitos e sem esforço nenhum.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-109-real-1.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg" data-author-comment="Eu estou apaixonada, tenho outros modeladores e esse automático sem fio é muito prático. Puxa a mecha suavemente e não enrosca no cabelo." data-author-date="16/11" data-author-name="M**a C**o" data-author-stars="5" data-author-variation="Branco e Dourado">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="M**a C**o" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">M**a C**o</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">16/11 · Branco e Dourado</div>
</div>
</div>
</div>
<p class="review-comment">Eu estou apaixonada, tenho outros modeladores e esse automático sem fio é muito prático. Puxa a mecha suavemente e não enrosca no cabelo.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-109-real-2.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_96.jpg" data-author-comment="Acho que foi uma das melhores compras que fiz, ele é simplesmente perfeito em tudo! Esquenta rápido e levo na bolsa para retocar quando preciso." data-author-date="14/11" data-author-name="B**a F**a" data-author-stars="5" data-author-variation="Cinza e Roxo">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="B**a F**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_96.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">B**a F**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">14/11 · Cinza e Roxo</div>
</div>
</div>
</div>
<p class="review-comment">Acho que foi uma das melhores compras que fiz, ele é simplesmente perfeito em tudo! Esquenta rápido e levo na bolsa para retocar quando preciso.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-109-real-3.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_98.jpg" data-author-comment="Forma um cacho bem definido e dura bastante. Recomendo pegar mechas finas para o cacho ficar mais marcado." data-author-date="12/11" data-author-name="L**a R**s" data-author-stars="4" data-author-variation="Cinza e Roxo">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="L**a R**s" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_98.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">L**a R**s</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#e5e5e5" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">12/11 · Cinza e Roxo</div>
</div>
</div>
</div>
<p class="review-comment">Forma um cacho bem definido e dura bastante. Recomendo pegar mechas finas para o cacho ficar mais marcado.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-109-real-4.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
"""
]

html = ''.join(lines)
# Remove old review-photos that refer to review-109-
html = re.sub(r'<div class="review-photos"[^>]*>.*?review-109-.*?</div>', '', html, flags=re.DOTALL)

parts = html.split('<div class="review-card"')
print("Total review-card splits in P109:", len(parts))

prefix = parts[0]
remaining_cards = parts[5:] # keep cards 5 to 15

rebuilt_html = prefix + ''.join(new_cards) + '<div class="review-card"' + '<div class="review-card"'.join(remaining_cards)

# Clean variations on remaining cards
rebuilt_html = re.sub(r'data-author-variation="[^"]*"', 'data-author-variation="Cinza e Roxo"', rebuilt_html)

with open('pages/produto-109.html', 'w', encoding='utf-8') as f:
    f.write(rebuilt_html)
print("[OK] pages/produto-109.html updated!")
