with open('pages/produto-105.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_cards = [
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg" data-author-comment="Eu não sou muito de avaliar os produtos mas esse merece, produto muito robusto, imagem incrível inclusive durante o dia, material resistente. Se você veio ver os comentários como eu fiz, pode comprar sem medo nenhum, vai se surpreender!" data-author-date="18/11" data-author-name="M**o S**a" data-author-stars="5" data-author-variation="Branco Smart Android 11 4K">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="M**o S**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">M**o S**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">18/11 · Branco Smart Android 11 4K</div>
</div>
</div>
</div>
<p class="review-comment">Eu não sou muito de avaliar os produtos mas esse merece, produto muito robusto, imagem incrível inclusive durante o dia, material resistente. Se você veio ver os comentários como eu fiz, pode comprar sem medo nenhum, vai se surpreender!</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real do comprador" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-105-real-1.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_51.jpg" data-author-comment="O projetor é muito bom! Nessa foto meu quarto estava meio claro por que minha janela entra um pouco de luz, mas ainda assim dá pra enxergar perfeitamente na parede. Roda YouTube e apps super liso." data-author-date="16/11" data-author-name="R**o G**s" data-author-stars="4" data-author-variation="Branco Smart Android 11 4K">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="R**o G**s" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_51.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">R**o G**s</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#e5e5e5" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">16/11 · Branco Smart Android 11 4K</div>
</div>
</div>
</div>
<p class="review-comment">O projetor é muito bom! Nessa foto meu quarto estava meio claro por que minha janela entra um pouco de luz, mas ainda assim dá pra enxergar perfeitamente na parede. Roda YouTube e apps super liso.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real do comprador" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-105-real-2.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg" data-author-comment="Ótimo custo benefício. Fácil de mexer, já tem 8GB de memória interna e sistema Android integrado. Conectei caixa Bluetooth externa e virou uma sala de cinema completa!" data-author-date="14/11" data-author-name="C**a P**o" data-author-stars="5" data-author-variation="Branco Smart Android 11 4K">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="C**a P**o" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">C**a P**o</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">14/11 · Branco Smart Android 11 4K</div>
</div>
</div>
</div>
<p class="review-comment">Ótimo custo benefício. Fácil de mexer, já tem 8GB de memória interna e sistema Android integrado. Conectei caixa Bluetooth externa e virou uma sala de cinema completa!</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real do comprador" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-105-real-3.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
""",
"""<div class="review-card" data-author-avatar="../img/reviews-avatars/tiktok_real/tt_avatar_53.jpg" data-author-comment="Para mim quebrou um galho enorme! Não tinha TV no quarto, o giro de 180 graus pra projetar no teto deitado na cama é sensacional. Imagem limpa e foco rápido." data-author-date="12/11" data-author-name="J**n S**a" data-author-stars="5" data-author-variation="Branco Smart Android 11 4K">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="J**n S**a" decoding="async" loading="lazy" src="../img/reviews-avatars/tiktok_real/tt_avatar_53.jpg"/>
</div>
<div class="review-user-info">
<div class="review-user-name">J**n S**a</div>
<div class="review-user-stars"><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
<div class="review-date">12/11 · Branco Smart Android 11 4K</div>
</div>
</div>
</div>
<p class="review-comment">Para mim quebrou um galho enorme! Não tinha TV no quarto, o giro de 180 graus pra projetar no teto deitado na cama é sensacional. Imagem limpa e foco rápido.</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real do comprador" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="../img/review-105-real-4.jpg" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
"""
]

# Lines 265 to 329 are 0-indexed 265 to 329.
# Let's verify line 265 is </div> and line 266 is review-card
print("Start line 265:", repr(lines[265]))
print("End line 329:", repr(lines[329]))

new_lines = lines[:265] + ['\n'.join(new_cards)] + lines[329:]
with open('pages/produto-105.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Successfully replaced lines 265-329 in pages/produto-105.html!")
