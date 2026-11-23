import re
import os

print("[*] Atualizando js/videos-criadores.js...")
with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Substituir PROJETOR_111_VIDEOS_MAP com dados 100% reais dos criadores do TikTok
old_proj_map_pattern = r'const PROJETOR_111_VIDEOS_MAP = \[[\s\S]*?\];'
new_proj_map = """const PROJETOR_111_VIDEOS_MAP = [
    {
      name: "Bruna spider",
      username: "brukaxpp",
      avatar: "../img/creators-auto/avatar-brukaxpp.jpg",
      poster: "../videosprodutos/posters/poster-produto-111.jpg",
      video: "../videosprodutos/video-produto-111.mp4",
      startTime: 0.2,
      desc: "Projetor Natalino Led Natal 16 desenhos em alta definição para parede e teto #tiktokshopbr #projetornatalino #natal"
    },
    {
      name: "MiPim",
      username: "marceloknesh",
      avatar: "../img/creators-auto/avatar-marceloknesh.jpg",
      poster: "../videosprodutos/posters/poster-produto-111-criadora2.jpg",
      video: "../videosprodutos/video-produto-111-criadora2.mp4",
      startTime: 0.2,
      desc: "Projetor natalino com 16 desenhos e alcance de projeção de até 8 metros 🎅❄️✨ #natal #decoracaodenatal #tiktokshop"
    },
    {
      name: "Alê indica",
      username: "alendica100",
      avatar: "../img/creators-auto/avatar-alendica100.jpg",
      poster: "../videosprodutos/posters/poster-produto-111-criadora3.jpg",
      video: "../videosprodutos/video-produto-111-criadora3.mp4",
      startTime: 0.2,
      desc: "Projetor Natalino Refletor Luzes de Natal Com 16 Desenhos 3D Laser Bivolt Portátil #projetornatalino #tiktokshop1111"
    },
    {
      name: "Kahena Rodrigues",
      username: "kahenar",
      avatar: "../img/creators-auto/avatar-kahenar.jpg",
      poster: "../videosprodutos/posters/poster-produto-111-criadora4.jpg",
      video: "../videosprodutos/video-produto-111-criadora4.mp4",
      startTime: 0.2,
      desc: "Esse projetor natalino transforma o ambiente em segundos e já deixa a casa com clima de Natal com 16 padrões #TikTokShopBR"
    }
  ];"""

js_content = re.sub(old_proj_map_pattern, new_proj_map, js_content, count=1)

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
print("[OK] js/videos-criadores.js atualizado!")

print("[*] Atualizando pages/produto-111.html...")
with open('pages/produto-111.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 1. Atualizar o HTML pré-renderizado do #creators-section
old_creators_pattern = r'<div id="creators-section" class="creators-section">[\s\S]*?</div>\s*</div>\s*</div>'
new_creators_html = """<div id="creators-section" class="creators-section">
        <h3 class="creators-title">Vídeos de criadores (4)</h3>
        <div class="creators-carousel" id="creators-carousel-list">
        <div class="creator-card" data-video-id="0">
          <img src="../videosprodutos/posters/poster-produto-111.jpg" alt="" loading="eager" fetchpriority="high" decoding="async" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 40%, rgba(0,0,0,0.75) 100%);"></div>
          <div style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2;">
            <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 6px; display: flex; align-items: center; gap: 5px; z-index: 2; box-sizing: border-box;">
            <img loading="lazy" decoding="async" src="../img/creators-auto/avatar-brukaxpp.jpg" alt="" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;" onerror="this.src='../img/creators-avatars/creator-1.jpg'">
            <span style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">Bruna spider</span>
          </div>
        </div>
        <div class="creator-card" data-video-id="1">
          <img src="../videosprodutos/posters/poster-produto-111-criadora2.jpg" alt="" loading="eager" decoding="async" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 40%, rgba(0,0,0,0.75) 100%);"></div>
          <div style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2;">
            <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 6px; display: flex; align-items: center; gap: 5px; z-index: 2; box-sizing: border-box;">
            <img loading="lazy" decoding="async" src="../img/creators-auto/avatar-marceloknesh.jpg" alt="" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;" onerror="this.src='../img/creators-avatars/creator-1.jpg'">
            <span style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">MiPim</span>
          </div>
        </div>
        <div class="creator-card" data-video-id="2">
          <img src="../videosprodutos/posters/poster-produto-111-criadora3.jpg" alt="" loading="lazy" decoding="async" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 40%, rgba(0,0,0,0.75) 100%);"></div>
          <div style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2;">
            <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 6px; display: flex; align-items: center; gap: 5px; z-index: 2; box-sizing: border-box;">
            <img loading="lazy" decoding="async" src="../img/creators-auto/avatar-alendica100.jpg" alt="" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;" onerror="this.src='../img/creators-avatars/creator-1.jpg'">
            <span style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">Alê indica</span>
          </div>
        </div>
        <div class="creator-card" data-video-id="3">
          <img src="../videosprodutos/posters/poster-produto-111-criadora4.jpg" alt="" loading="lazy" decoding="async" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 40%, rgba(0,0,0,0.75) 100%);"></div>
          <div style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2;">
            <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 6px; display: flex; align-items: center; gap: 5px; z-index: 2; box-sizing: border-box;">
            <img loading="lazy" decoding="async" src="../img/creators-auto/avatar-kahenar.jpg" alt="" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;" onerror="this.src='../img/creators-avatars/creator-1.jpg'">
            <span style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">Kahena Rodrigues</span>
          </div>
        </div>
        </div>
      </div>"""

html_content = re.sub(old_creators_pattern, new_creators_html, html_content, count=1)

# 2. Adicionar fotos reais nas avaliações
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
        <!-- Avaliação 1 -->
        <div class="review-card" data-author-name="Luciana F." data-author-avatar="../img/reviews-avatars/review-user-4.jpg" data-author-stars="5" data-author-comment="Gente, que coisa mais linda! As projeções na parede e no teto parecem filme de Natal! As crianças ficaram encantadas vendo o Papai Noel e os flocos girando. Super fácil de ligar no carregador do celular ou power bank.">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-4.jpg" alt="Luciana Ferraz">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">Luciana F.</div>
                <div class="review-user-stars"><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
                <div class="review-date">Ontem às 19:15 · Preto Clássico / USB Bivolt</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Gente, que coisa mais linda! As projeções na parede e no teto parecem filme de Natal! As crianças ficaram encantadas vendo o Papai Noel e os flocos girando. Super fácil de ligar no carregador do celular ou power bank.</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-111-real-1.jpg" alt="Foto da cliente" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-111-real-2.jpg" alt="Foto da cliente" onclick="openPhotoModal(this.src)">
          </div>
        </div>
        <!-- Avaliação 2 -->
        <div class="review-card" data-author-name="Patricia A." data-author-avatar="../img/reviews-avatars/review-user-5.jpg" data-author-stars="5" data-author-comment="Chegou muito antes do prazo e muito bem embalado. Testei assim que chegou na sala com as luzes apagadas e a resolução dos 16 desenhos é perfeita, cores vivas e o motorzinho gira suave sem fazer barulho!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-5.jpg" alt="Patricia Albuquerque">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">Patricia A.</div>
                <div class="review-user-stars"><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
                <div class="review-date">Há 2 dias · Branco Neve / USB Bivolt</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Chegou muito antes do prazo e muito bem embalado. Testei assim que chegou na sala com as luzes apagadas e a resolução dos 16 desenhos é perfeita, cores vivas e o motorzinho gira suave sem fazer barulho!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-111-real-1.jpg" alt="Foto da cliente" onclick="openPhotoModal(this.src)">
          </div>
        </div>
        <!-- Avaliação 3 -->
        <div class="review-card" data-author-name="Camila R." data-author-avatar="../img/reviews-avatars/review-user-6.jpg" data-author-stars="5" data-author-comment="Comprei para a festa de Natal da família e todo mundo elogiou. O alcance é ótimo, cobre a parede inteira da sala. Melhor compra de decoração que já fiz!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-6.jpg" alt="Camila Rocha">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">Camila R.</div>
                <div class="review-user-stars"><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
                <div class="review-date">Há 3 dias · Preto Clássico / USB Bivolt</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Comprei para a festa de Natal da família e todo mundo elogiou. O alcance é ótimo, cobre a parede inteira da sala. Melhor compra de decoração que já fiz!</p>
        </div>
      </div>

      <!-- DESCRIÇÃO DO PRODUTO -->"""

html_content = re.sub(old_rev_pattern, new_rev_html, html_content, count=1)

with open('pages/produto-111.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print("[OK] pages/produto-111.html atualizado!")
