import re

with open('pages/produto-111.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Substituir a seção de avaliações com os compradores oficiais do TikTok Shop
old_rev_pattern = r'<!-- AVALIAÇÕES -->[\s\S]*?<!-- DESCRIÇÃO DO PRODUTO -->'
new_rev_html = """<!-- AVALIAÇÕES -->
      <div class="reviews-section">
        <h3 class="reviews-header">Avaliações dos clientes (5)</h3>
        <div class="reviews-summary">
          <span class="review-avg">4.9</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          </div>
        </div>
        <!-- Avaliação 1 (Com 2 fotos -> Badge +2 no bloco 70x70) -->
        <div class="review-card" data-author-name="D**y" data-author-avatar="../img/reviews-avatars/default-avatar.svg" data-author-stars="5" data-author-comment="Características: Ótimo · Instalação: Fácil · Desempenho: Excelente! As projeções no piso e na parede parecem filme de Natal! As crianças adoraram vendo o Papai Noel e as renas girando. Super prático!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/default-avatar.svg" alt="D**y">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">D**y</div>
                <div class="review-user-stars"><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
                <div class="review-date">Há 2 dias · Preto Clássico / USB Bivolt</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Características: Ótimo · Instalação: Fácil · Desempenho: Excelente! As projeções no piso e na parede parecem filme de Natal! As crianças adoraram vendo o Papai Noel e as renas girando. Super prático!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-111-real-1.jpg" alt="Foto do comprador TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-111-real-2.jpg" alt="Foto da embalagem TikTok Shop" onclick="openPhotoModal(this.src)">
          </div>
        </div>
        <!-- Avaliação 2 (Com 1 foto -> Bloco 70x70 sem badge) -->
        <div class="review-card" data-author-name="I**a G**a" data-author-avatar="../img/reviews-avatars/default-avatar.svg" data-author-stars="5" data-author-comment="Chegou super rápido aqui em SP. Testei na sala à noite com tudo apagado e a nitidez dos 16 desenhos é impressionante! Cores fortes e motor gira silencioso.">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/default-avatar.svg" alt="I**a G**a">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">I**a G**a</div>
                <div class="review-user-stars"><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
                <div class="review-date">Há 3 dias · Branco Neve / USB Bivolt</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Chegou super rápido aqui em SP. Testei na sala à noite com tudo apagado e a nitidez dos 16 desenhos é impressionante! Cores fortes e motor gira silencioso.</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-111-real-1.jpg" alt="Foto da cliente" onclick="openPhotoModal(this.src)">
          </div>
        </div>
        <!-- Avaliação 3 (Zero fotos -> Text-only total) -->
        <div class="review-card" data-author-name="d**e" data-author-avatar="../img/reviews-avatars/default-avatar.svg" data-author-stars="5" data-author-comment="Gostei muito, é linda! Comprei para a festa de Natal da família e todo mundo elogiou. O alcance é ótimo, cobre a parede inteira da sala.">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/default-avatar.svg" alt="d**e">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">d**e</div>
                <div class="review-user-stars"><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
                <div class="review-date">Há 4 dias · Preto Clássico / USB Bivolt</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Gostei muito, é linda! Comprei para a festa de Natal da família e todo mundo elogiou. O alcance é ótimo, cobre a parede inteira da sala.</p>
        </div>
      </div>

      <!-- DESCRIÇÃO DO PRODUTO -->"""

html = re.sub(old_rev_pattern, new_rev_html, html, count=1)

with open('pages/produto-111.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("[OK] Avaliações com paridade TikTok Shop atualizadas com sucesso!")
