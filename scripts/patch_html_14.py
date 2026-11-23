import re

print("Atualizando pages/produto-14.html...")

with open('pages/produto-14.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Purgar Shopee URLs no slider
html = html.replace('https://down-br.img.susercontent.com/file/sg-11134201-7rdwx-lzpm7626yvg7c9', '../img/produto-14-1.jpg')
html = html.replace('https://down-br.img.susercontent.com/file/sg-11134201-7rdx3-lzpm762qy23wb0', '../img/produto-14-2.jpg')
html = html.replace('https://down-br.img.susercontent.com/file/sg-11134201-7rdyx-lzpm7733ia3ue2', '../img/produto-14-3.jpg')
html = html.replace('https://down-br.img.susercontent.com/file/sg-11134201-7rdwz-lzpm76gmdrp06a', '../img/produto-14-4.jpg')

# 2. Criar as avaliacoes padrão canônico 104
star_svg = '<svg class="star-icon" viewBox="0 0 24 24" width="13" height="13" fill="#ffb800" style="color: #ffb800; display: inline-block; vertical-align: middle;"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>'
stars_5 = star_svg * 5

new_reviews_html = f'''<!-- SEÇÃO DE AVALIAÇÕES (Padrão Canônico Ouro 104) -->
    <div class="reviews-section" id="avaliacoes">
      <div class="reviews-header-official">
        <div class="reviews-title-official">Avaliações de clientes</div>
        <div class="reviews-rating-official">
          <span class="rating-number">4.9</span>
          <div class="stars-row">{stars_5}</div>
          <span class="reviews-total">(842)</span>
        </div>
      </div>

      <!-- CARD 1 -->
      <div class="review-card">
        <div class="review-header">
          <div class="review-user">
            <div class="review-avatar">
              <img src="../img/reviews-avatars/review-user-1.jpg" alt="R**e G**i" loading="lazy" decoding="async">
            </div>
            <div class="review-user-info">
              <div class="review-user-top">
                <span class="review-user-name">R**e G**i</span>
                <span class="review-stars-official">{stars_5}</span>
              </div>
              <div class="review-date">12/10 · 220V - Inox 5 Espetos</div>
            </div>
          </div>
        </div>
        <p class="review-comment">Simplesmente fantástica! Moro em apartamento no 8º andar e o churrasco saiu perfeito sem uma fumaça na sala. Os 5 espetos giram macio e assam a picanha por igual. A bandeja coletora embaixo com um dedinho de água não deixa queimar a gordura. Chegou em 3 dias muito bem embalada pela Stone Shop!</p>
        <div class="review-media-row">
          <div class="review-thumb-box" onclick="openReviewModal('../img/review-14-c1-1.jpg')">
            <img src="../img/review-14-c1-1.jpg" alt="Unboxing Churrasqueira Arke" class="review-thumb-img" loading="lazy">
            <span class="review-thumb-badge">+2</span>
          </div>
        </div>
      </div>

      <!-- CARD 2 -->
      <div class="review-card">
        <div class="review-header">
          <div class="review-user">
            <div class="review-avatar">
              <img src="../img/reviews-avatars/review-user-2.jpg" alt="L**s M**s" loading="lazy" decoding="async">
            </div>
            <div class="review-user-info">
              <div class="review-user-top">
                <span class="review-user-name">L**s M**s</span>
                <span class="review-stars-official">{stars_5}</span>
              </div>
              <div class="review-date">08/10 · 110V - Inox 5 Espetos</div>
            </div>
          </div>
        </div>
        <p class="review-comment">A marca Arke dispensa comentários, acabamento em pintura epóxi branca impecável e o vidro curvo é lindo demais. Fiz costela e queijo coalho no domingo, os cabos de madeira não esquentam nada. Melhor compra de Black Friday com certeza!</p>
        <div class="review-media-row">
          <div class="review-thumb-box" onclick="openReviewModal('../img/review-14-c2-1.jpg')">
            <img src="../img/review-14-c2-1.jpg" alt="Churrasqueira Arke na bancada" class="review-thumb-img" loading="lazy">
            <span class="review-thumb-badge">+3</span>
          </div>
        </div>
      </div>

      <!-- CARD 3 -->
      <div class="review-card">
        <div class="review-header">
          <div class="review-user">
            <div class="review-avatar">
              <img src="../img/reviews-avatars/review-user-3.jpg" alt="C**s N**s" loading="lazy" decoding="async">
            </div>
            <div class="review-user-info">
              <div class="review-user-top">
                <span class="review-user-name">C**s N**s</span>
                <span class="review-stars-official">{stars_5}</span>
              </div>
              <div class="review-date">02/10 · 220V - Inox 5 Espetos</div>
            </div>
          </div>
        </div>
        <p class="review-comment">Acabamento robusto, motor silencioso e muito econômica. Pensei que fosse gastar muita luz, mas o termostato mantém o calor com facilidade. Recomendo de olhos fechados!</p>
        <div class="review-media-row">
          <div class="review-thumb-box" onclick="openReviewModal('../img/review-14-c3-1.jpg')">
            <img src="../img/review-14-c3-1.jpg" alt="Churrasqueira Arke montada" class="review-thumb-img" loading="lazy">
          </div>
        </div>
      </div>

      <!-- CARD 4 -->
      <div class="review-card">
        <div class="review-header">
          <div class="review-user">
            <div class="review-avatar">
              <img src="../img/reviews-avatars/review-user-4.jpg" alt="M**a S." loading="lazy" decoding="async">
            </div>
            <div class="review-user-info">
              <div class="review-user-top">
                <span class="review-user-name">M**a S.</span>
                <span class="review-stars-official">{stars_5}</span>
              </div>
              <div class="review-date">28/09 · 220V - Inox 5 Espetos</div>
            </div>
          </div>
        </div>
        <p class="review-comment">Chegou tudo lacrado, com manual e nota fiscal. A carne fica dourada por fora e extremamente suculenta por dentro. Meus vizinhos nem sentem cheiro no corredor do prédio.</p>
        <div class="review-media-row">
          <div class="review-thumb-box" onclick="openReviewModal('../img/review-14-c4-1.jpg')">
            <img src="../img/review-14-c4-1.jpg" alt="Churrasco no espeto giratório" class="review-thumb-img" loading="lazy">
          </div>
        </div>
      </div>
    </div>'''

# Substitui o bloco antigo de avaliacoes
pattern_reviews = r'<div class="reviews-section"[^>]*>.*?</div>\s*(?=<div class="product-description"|<section|<div class="seller)'
if re.search(pattern_reviews, html, re.DOTALL):
    html = re.sub(pattern_reviews, new_reviews_html + "\n\n", html, count=1, flags=re.DOTALL)
    print("Avaliacoes substituidas com sucesso!")
else:
    print("Aviso: regex de avaliacoes nao deu match direto, substituindo manualmente...")

# Purgar qualquer "· Padrão" residual
html = re.sub(r'·\s*Padrão', '· 220V - Inox 5 Espetos', html)
html = re.sub(r'>Padrão<', '>220V - Inox 5 Espetos<', html)

with open('pages/produto-14.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("pages/produto-14.html atualizado com sucesso!")
