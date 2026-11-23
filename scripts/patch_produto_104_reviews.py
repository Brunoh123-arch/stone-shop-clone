import re

with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Atualizar contagem no topo da vitrine de (101) para (3)
html = re.sub(
    r'<span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document\.querySelector\(\'\.reviews-section\'\)\?\.scrollIntoView\(\{behavior:\'smooth\'\}\)">\(\d+\)</span>',
    '<span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document.querySelector(\'.reviews-section\')?.scrollIntoView({behavior:\'smooth\'})">(3)</span>',
    html
)

# 2. Atualizar header de avaliacoes e os 3 cards com as fotos e comentarios oficiais
old_reviews_pattern = r'<div class="reviews-section">[\s\S]*?</div>\s*(?=\s*<style id="tt-sobre-produto-style">)'

new_reviews_markup = """<div class="reviews-section">
        <h3 class="reviews-header">Avaliações dos clientes (3)</h3>
        <div class="reviews-summary">
          <span class="review-avg">4.8</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          </div>
        </div>

        <!-- Avaliação 1 Oficial TikTok Shop: S**a M. (BRANCO, 37/38) com 5 fotos reais -->
        <div class="review-card" data-author-name="S**a M." data-author-avatar="../img/reviews-avatars/review-user-104-vanessa.jpg?v=1794225" data-author-stars="5" data-author-comment="Simplesmente perfeito. Veio do tamanho certo, brilha demais, chegou rápido. Melhor compra que fiz aqui!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-104-vanessa.jpg?v=1794225" alt="S**a M.">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">S**a M.</div>
                <div class="review-user-stars"><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
                <div class="review-date">Há 2 semanas · BRANCO, 37/38</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Simplesmente perfeito. Veio do tamanho certo, brilha demais, chegou rápido. Melhor compra que fiz aqui!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c1-1.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c1-2.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c1-3.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c1-4.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c1-5.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 2 Oficial TikTok Shop: J**a C. (CARAMELO, 37/38) com 5 fotos reais -->
        <div class="review-card" data-author-name="J**a C." data-author-avatar="../img/reviews-avatars/review-user-104-juliana.jpg?v=1794225" data-author-stars="5" data-author-comment="Forma e tamanho: Pedi a 37/38 ficou perfeita no meu pé, muito confortável. E sem contar que é linda demais!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-104-juliana.jpg?v=1794225" alt="J**a C.">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">J**a C.</div>
                <div class="review-user-stars"><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
                <div class="review-date">Há 2 semanas · CARAMELO, 37/38</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Forma e tamanho: Pedi a 37/38 ficou perfeita no meu pé, muito confortável. E sem contar que é linda demais!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c2-1.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c2-2.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c2-3.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c2-4.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c2-5.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 3 Oficial TikTok Shop: R**y S. (PRETO, 35/36) com 5 fotos reais -->
        <div class="review-card" data-author-name="R**y S." data-author-avatar="../img/reviews-avatars/review-user-104-renata.jpg?v=1794225" data-author-stars="5" data-author-comment="Chegou tudo certinho ela é linda, super macia e o brilho dos strass é maravilhoso. Muito confortável!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-104-renata.jpg?v=1794225" alt="R**y S.">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">R**y S.</div>
                <div class="review-user-stars"><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
                <div class="review-date">Há 1 mês · PRETO, 35/36</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Chegou tudo certinho ela é linda, super macia e o brilho dos strass é maravilhoso. Muito confortável!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c3-1.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c3-2.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c3-3.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c3-4.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-104-c3-5.jpg?v=3" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">
          </div>
        </div>
      </div>"""

new_html, count = re.subn(old_reviews_pattern, new_reviews_markup, html)
print(f"Replacements made: {count}")

# Validar profundidade do DOM
app_idx = new_html.find('class="app-container"')
sub = new_html[app_idx:]
open_divs = len(re.findall(r'<div[\s>]', sub, re.IGNORECASE))
close_divs = len(re.findall(r'</div>', sub, re.IGNORECASE))
diff = open_divs - close_divs
print(f"Tag depth diff: {diff} (open: {open_divs}, close: {close_divs})")

if count == 1 and diff == 0:
    with open('pages/produto-104.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("pages/produto-104.html updated successfully with zero errors!")
else:
    print("Error during update - diff was not zero or count != 1")
