import re

html_path = 'pages/produto-103.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update top rating count to (3)
content = re.sub(
    r'(<span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document\.querySelector\(\'\.reviews-section\'\)\?\.scrollIntoView\(\{behavior:\'smooth\'\}\)">)\(\d+\)(</span>)',
    r'\g<1>(3)\g<2>',
    content
)

# 2. Update reviews-header to (3)
content = re.sub(
    r'<h3 class="reviews-header">Avaliações dos clientes \(\d+\)</h3>',
    r'<h3 class="reviews-header">Avaliações dos clientes (3)</h3>',
    content
)

star_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
five_stars = star_svg * 5

header_star_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
five_header_stars = header_star_svg * 5

new_reviews_html = f"""      <!-- AVALIAÇÕES -->
      <div class="reviews-section">
        <h3 class="reviews-header">Avaliações dos clientes (3)</h3>
        <div class="reviews-summary">
          <span class="review-avg">4.8</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            {five_header_stars}
          </div>
        </div>

        <!-- Avaliação 1 Oficial TikTok Shop: p**a r**a p**s d**o (Vinho Tinto, Tamanho Único) com 3 fotos reais -->
        <div class="review-card" data-author-name="p**a r**a p**s d**o" data-author-avatar="../img/reviews-avatars/review-user-103-c1.jpg?v=3" data-author-stars="5" data-author-variation="Vinho Tinto, Tamanho Único" data-author-date="05/09" data-author-comment="Chegou no prazo, corresponde com o que é apresentado. Por ser tamanho único serviu muito bem! Corresponde a cor perfeitamente, o caimento é impecável.">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-103-c1.jpg?v=3" alt="p**a r**a p**s d**o">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">p**a r**a p**s d**o</div>
                <div class="review-user-stars">{five_stars}</div>
                <div class="review-date">05/09 · Vinho Tinto, Tamanho Único</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Chegou no prazo, corresponde com o que é apresentado. Por ser tamanho único serviu muito bem! Corresponde a cor perfeitamente, o caimento é impecável.</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-103-c1-1.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-103-c1-2.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-103-c1-3.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 2 Oficial TikTok Shop: A**3 (Vinho Tinto, Tamanho Único) com 3 fotos reais -->
        <div class="review-card" data-author-name="A**3" data-author-avatar="../img/reviews-avatars/review-user-103-c2.jpg?v=3" data-author-stars="5" data-author-variation="Vinho Tinto, Tamanho Único" data-author-date="20/08" data-author-comment="Perfeito. Igualzinho a modelo! Em si, o vestido é lindo🥰 tamanho perfeito. Tenho 1,63 de altura peso 61 quilos. Valoriza muito as silhuetas. Sem marcar muito. Nada a reclamar. Qualidade perfeita. Nada de transparente. Impecável. Super recomendo 🥰🥰🥰">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-103-c2.jpg?v=3" alt="A**3">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">A**3</div>
                <div class="review-user-stars">{five_stars}</div>
                <div class="review-date">20/08 · Vinho Tinto, Tamanho Único</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Perfeito. Igualzinho a modelo! Em si, o vestido é lindo🥰 tamanho perfeito. Tenho 1,63 de altura peso 61 quilos. Valoriza muito as silhuetas. Sem marcar muito. Nada a reclamar. Qualidade perfeita. Nada de transparente. Impecável. Super recomendo 🥰🥰🥰</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-103-c2-1.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-103-c2-2.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-103-c2-3.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 3 Oficial TikTok Shop: C****a (Vermelho, Tamanho Único) com 1 foto real -->
        <div class="review-card" data-author-name="C****a" data-author-avatar="../img/reviews-avatars/review-user-103-c3.jpg?v=3" data-author-stars="5" data-author-variation="Vermelho, Tamanho Único" data-author-date="18/09" data-author-comment="Meninas comprem sem medo! O tecido tem um caimento absurdo, não fica transparente de jeito nenhum. Fui numa festa de formatura e todo mundo elogiou as costas abertas!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-103-c3.jpg?v=3" alt="C****a">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">C****a</div>
                <div class="review-user-stars">{five_stars}</div>
                <div class="review-date">18/09 · Vermelho, Tamanho Único</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Meninas comprem sem medo! O tecido tem um caimento absurdo, não fica transparente de jeito nenhum. Fui numa festa de formatura e todo mundo elogiou as costas abertas!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-103-c3-1.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
          </div>
        </div>

      </div>"""

# Replace the old reviews block
content = re.sub(
    r'<!-- AVALIAÇÕES -->.*?</div>\s*(?=<!-- PRODUTOS RELACIONADOS -->)',
    new_reviews_html + '\n\n      ',
    content,
    flags=re.DOTALL
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] pages/produto-103.html updated successfully with 3 authentic reviews!")
