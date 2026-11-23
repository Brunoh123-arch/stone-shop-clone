import re

with open('pages/produto-14.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Purgar todo e qualquer vestígio de Shopee URLs
html = html.replace('https://down-br.img.susercontent.com/file/sg-11134201-7rdwx-lzpm7626yvg7c9', '../img/produto-14-1.jpg')
html = html.replace('https://down-br.img.susercontent.com/file/sg-11134201-7rdx3-lzpm762qy23wb0', '../img/produto-14-2.jpg')
html = html.replace('https://down-br.img.susercontent.com/file/sg-11134201-7rdyx-lzpm7733ia3ue2', '../img/produto-14-3.jpg')
html = html.replace('https://down-br.img.susercontent.com/file/sg-11134201-7rdwz-lzpm76gmdrp06a', '../img/produto-14-4.jpg')

# SVG Star Ouro
star_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
stars_5 = star_svg * 5

new_reviews_section = f'''      <!-- AVALIAÇÕES (Padrão Canônico Ouro 104) -->
      <div class="reviews-section" id="avaliacoes">
        <h3 class="reviews-header">Avaliações dos clientes (842)</h3>
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

        <!-- Avaliação 1 Oficial: R**e G**i -->
        <div class="review-card" data-author-name="R**e G**i" data-author-avatar="../img/reviews-avatars/review-user-1.jpg" data-author-stars="5" data-author-variation="220V - Inox 5 Espetos" data-author-date="12/10" data-author-comment="Simplesmente fantástica! Moro em apartamento no 8º andar e o churrasco saiu perfeito sem uma fumaça na sala. Os 5 espetos giram macio e assam a picanha por igual. A gaveta de gordura com água embaixo não deixa queimar e é super fácil de lavar. Chegou super rápido pela Stone Shop!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-1.jpg" alt="R**e G**i">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">R**e G**i</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">12/10 · 220V - Inox 5 Espetos</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Simplesmente fantástica! Moro em apartamento no 8º andar e o churrasco saiu perfeito sem uma fumaça na sala. Os 5 espetos giram macio e assam a picanha por igual. A gaveta de gordura com água embaixo não deixa queimar e é super fácil de lavar. Chegou super rápido pela Stone Shop!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-14-c1-1.jpg" alt="Unboxing Churrasqueira Arke" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 2 Oficial: L**s M**s -->
        <div class="review-card" data-author-name="L**s M**s" data-author-avatar="../img/reviews-avatars/review-user-2.jpg" data-author-stars="5" data-author-variation="110V - Inox 5 Espetos" data-author-date="08/10" data-author-comment="A marca Arke dispensa apresentações! Acabamento em epóxi impecável e o vidro curvo é lindo demais. Fiz costela e queijo coalho no domingo, os cabos de madeira não esquentam nada. Melhor compra de Black Friday com certeza!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-2.jpg" alt="L**s M**s">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">L**s M**s</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">08/10 · 110V - Inox 5 Espetos</div>
              </div>
            </div>
          </div>
          <p class="review-comment">A marca Arke dispensa apresentações! Acabamento em epóxi impecável e o vidro curvo é lindo demais. Fiz costela e queijo coalho no domingo, os cabos de madeira não esquentam nada. Melhor compra de Black Friday com certeza!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-14-c2-1.jpg" alt="Churrasqueira Arke na bancada" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 3 Oficial: C**s N**s -->
        <div class="review-card" data-author-name="C**s N**s" data-author-avatar="../img/reviews-avatars/review-user-3.jpg" data-author-stars="5" data-author-variation="220V - Inox 5 Espetos" data-author-date="02/10" data-author-comment="Motor silencioso, assa por igual e muito econômica. Pensei que fosse gastar muita luz, mas o termostato mantém o calor com facilidade. Recomendo de olhos fechados!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-3.jpg" alt="C**s N**s">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">C**s N**s</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">02/10 · 220V - Inox 5 Espetos</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Motor silencioso, assa por igual e muito econômica. Pensei que fosse gastar muita luz, mas o termostato mantém o calor com facilidade. Recomendo de olhos fechados!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-14-c3-1.jpg" alt="Churrasqueira Arke montada" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 4 Oficial: M**a S. -->
        <div class="review-card" data-author-name="M**a S." data-author-avatar="../img/reviews-avatars/review-user-4.jpg" data-author-stars="5" data-author-variation="220V - Inox 5 Espetos" data-author-date="28/09" data-author-comment="Chegou tudo lacrado, com manual e nota fiscal. A carne fica dourada por fora e extremamente suculenta por dentro. Meus vizinhos nem sentem cheiro no corredor do prédio.">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-4.jpg" alt="M**a S.">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">M**a S.</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">28/09 · 220V - Inox 5 Espetos</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Chegou tudo lacrado, com manual e nota fiscal. A carne fica dourada por fora e extremamente suculenta por dentro. Meus vizinhos nem sentem cheiro no corredor do prédio.</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-14-c4-1.jpg" alt="Churrasco no espeto giratório" onclick="openPhotoModal(this.src)">
          </div>
        </div>
      </div>'''

# Localiza a section inteira de reviews
start_idx = html.find('<section class="reviews-section"')
end_idx = html.find('</section>', start_idx) + len('</section>')

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_reviews_section + html[end_idx:]
    print("Section de reviews substituída com sucesso pelo padrão canônico 104!")
else:
    print("Erro ao localizar section de reviews!")

# Purgar qualquer "· Padrão" residual
html = html.replace('· Padrão', '· 220V - Inox 5 Espetos')
html = html.replace('>Padrão<', '>220V - Inox 5 Espetos<')

with open('pages/produto-14.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("pages/produto-14.html 100% blindado!")
