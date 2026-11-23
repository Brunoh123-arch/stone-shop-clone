import re

with open('pages/produto-35.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Vamos localizar os primeiros 5 review-card de P35 e colocar fotos reais de unboxing da JBL
p35_real_reviews_html = """        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar"><img loading="lazy" decoding="async" src="../img/reviews-avatars/tiktok_real/tt_avatar_4.jpg" alt="E**a" onerror="this.outerHTML='<div class=\\'review-avatar-placeholder\\'>E</div>'"></div>
              <div class="review-user-info">
                <div class="review-user-name">E**a</div>
                <div class="review-user-stars">★★★★★</div>
                <div class="review-date">2026-01-17 10:51 · Padrão</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Chegou super rápido e muito bem embalada! A caixa é monstruosa, acabamento impecável e os graves tremem a casa toda. Super recomendo a loja!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/reviews-unboxing/p35/jbl_1.jpg" alt="JBL Boombox 4 na caixa" onclick="openPhotoModal(this.src)">
          </div>
        </div>
        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar"><img loading="lazy" decoding="async" src="../img/reviews-avatars/tiktok_real/tt_avatar_12.jpg" alt="R**o J**r" onerror="this.outerHTML='<div class=\\'review-avatar-placeholder\\'>R</div>'"></div>
              <div class="review-user-info">
                <div class="review-user-name">R**o J**r</div>
                <div class="review-user-stars">★★★★★</div>
                <div class="review-date">2026-01-16 22:05 · Padrão</div>
              </div>
            </div>
          </div>
          <p class="review-comment">A Braba tem nome.... JBL BOOMBOX 4 😍✨ Postagem da Loja perfeita... E o melhor, entrega relâmpago, sem avarias..intacta! Parabéns 😍✨</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/reviews-unboxing/p35/jbl_2.jpg" alt="JBL Boombox 4 unboxing" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/reviews-unboxing/p35/jbl_3.jpg" alt="JBL Boombox 4 detalhe" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/reviews-unboxing/p35/jbl_4.jpg" alt="JBL Boombox 4 traseira" onclick="openPhotoModal(this.src)">
          </div>
        </div>
        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar"><img loading="lazy" decoding="async" src="../img/reviews-avatars/tiktok_real/tt_avatar_20.jpg" alt="G**o B." onerror="this.outerHTML='<div class=\\'review-avatar-placeholder\\'>G</div>'"></div>
              <div class="review-user-info">
                <div class="review-user-name">G**o B.</div>
                <div class="review-user-stars">★★★★★</div>
                <div class="review-date">2026-01-16 11:04 · Padrão</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Som espetacular! Uso na área externa no churrasco do final de semana e não precisa nem colocar no máximo. Bateria surreal de boa.</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/reviews-unboxing/p35/jbl_5.jpg" alt="JBL Boombox 4 lateral" onclick="openPhotoModal(this.src)">
          </div>
        </div>
        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar"><img loading="lazy" decoding="async" src="../img/reviews-avatars/tiktok_real/tt_avatar_25.jpg" alt="C**o L." onerror="this.outerHTML='<div class=\\'review-avatar-placeholder\\'>C</div>'"></div>
              <div class="review-user-info">
                <div class="review-user-name">C**o L.</div>
                <div class="review-user-stars">★★★★★</div>
                <div class="review-date">2026-01-15 19:40 · Padrão</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Potência absurda, grave macio e limpo sem distorção. Vale cada centavo investido. Entrega antes do prazo!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/reviews-unboxing/p35/jbl_6.jpg" alt="JBL Boombox 4 alça" onclick="openPhotoModal(this.src)">
          </div>
        </div>"""

# Substitui os primeiros 4 cards de review em P35
# Encontrar onde começam os review-card
card_start = html.find('<div class="review-card">')
# Encontrar o 5º card
pos = card_start
for _ in range(4):
    pos = html.find('<div class="review-card">', pos + 1)

if card_start != -1 and pos != -1:
    html = html[:card_start] + p35_real_reviews_html + "\n        " + html[pos:]
    with open('pages/produto-35.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Sucesso: Primeiras 4 avaliações de P35 atualizadas com fotos reais de unboxing da JBL e avatares do TikTok!")
else:
    print("Erro ao localizar limites dos cards em P35")
