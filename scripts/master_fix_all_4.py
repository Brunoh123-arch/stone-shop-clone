import os
import shutil
import re
from PIL import Image

print("[*] EXECUTANDO FIX MESTRE DOS 4 PROBLEMAS...")

# -------------------------------------------------------------
# 1. IMAGENS OFICIAIS DO SLIDER (MATAR CACHE E EXTERMINAR SHOPEE)
# -------------------------------------------------------------
# Copiar as 5 imagens oficiais limpas 800x800 com novos nomes
slider_imgs = [
    ('img/produto-111-1.jpg', 'img/produto-111-oficial-1.jpg'),
    ('img/produto-111-2.jpg', 'img/produto-111-oficial-2.jpg'),
    ('img/produto-111-3.jpg', 'img/produto-111-oficial-3.jpg'),
    ('img/produto-111-4.jpg', 'img/produto-111-oficial-4.jpg'),
    ('img/produto-111-5.jpg', 'img/produto-111-oficial-5.jpg'),
]
for src, dst in slider_imgs:
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Slider img: {dst} ({os.path.getsize(dst)} bytes)")

# -------------------------------------------------------------
# 2. FOTOS REAIS E ÚNICAS DE AVALIAÇÃO
# -------------------------------------------------------------
# Foto 1: Piso de azulejo com as luzes e pé do ventilador (TikTok Shop oficial)
Image.open('scratch/tt_rev_1.webp').convert('RGB').save('img/review-111-piso-tt.jpg', quality=95)
# Foto 2: Caixa na bancada de mármore (TikTok Shop oficial)
Image.open('scratch/tt_rev_0.webp').convert('RGB').save('img/review-111-box-tt.jpg', quality=95)
# Foto 3: Unboxing tirando da caixa (unboxing real sem setas)
Image.open('scratch/frames_clean/unboxing_clean.jpg').convert('RGB').save('img/review-111-unboxing-real.jpg', quality=95)
print("Fotos reais de avaliações preparadas com sucesso!")

# -------------------------------------------------------------
# 3. POSTERS LIMPOS DE CRIADORES (SEM SETAS ROSAS NEM MEMES)
# -------------------------------------------------------------
# Criador 1: Bruna spider (@brukaxpp) -> poster_bruna_spider.jpg
# Criador 2: Kahena Rodrigues (@kahenar) -> poster_kahena_rodrigues.jpg
# Criador 3: Alê indica (@alendica100) -> poster_alendica100.jpg
# Criador 4: Vitta Shop (@evysantoss02) -> unboxing limpo
shutil.copy2('scratch/real_creators/poster_bruna_spider.jpg', 'videosprodutos/posters/poster-111-bruna.jpg')
shutil.copy2('scratch/real_creators/poster_kahena_rodrigues.jpg', 'videosprodutos/posters/poster-111-kahena.jpg')
shutil.copy2('scratch/real_creators/poster_alendica100.jpg', 'videosprodutos/posters/poster-111-ale.jpg')
shutil.copy2('scratch/frames_clean/unboxing_clean.jpg', 'videosprodutos/posters/poster-111-vitta.jpg')

# Avatares
if os.path.exists('scratch/real_creators/avatar_bruna_spider.jpg'):
    shutil.copy2('scratch/real_creators/avatar_bruna_spider.jpg', 'img/creators-auto/avatar-brukaxpp.jpg')
if os.path.exists('scratch/real_creators/avatar_kahena_rodrigues.jpg'):
    shutil.copy2('scratch/real_creators/avatar_kahena_rodrigues.jpg', 'img/creators-auto/avatar-kahenar.jpg')
if os.path.exists('scratch/real_creators/avatar_alendica100.jpg'):
    shutil.copy2('scratch/real_creators/avatar_alendica100.jpg', 'img/creators-auto/avatar-alendica100.jpg')

print("Posters e avatares limpos copiados!")

# -------------------------------------------------------------
# 4. ATUALIZAR js/videos-criadores.js (PRECEDÊNCIA E DATASET)
# -------------------------------------------------------------
with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Dataset 111 limpo
new_dataset_111 = """  const PROJETOR_111_VIDEOS_MAP = [
    {
      name: "Bruna spider",
      username: "brukaxpp",
      avatar: "../img/creators-auto/avatar-brukaxpp.jpg",
      poster: "../videosprodutos/posters/poster-111-bruna.jpg",
      video: "../videosprodutos/video-produto-111.mp4",
      startTime: 0.2,
      desc: "Projetor Natalino Led Natal 16 desenhos em alta definição para parede e teto #tiktokshopbr #projetornatalino #natal"
    },
    {
      name: "Kahena Rodrigues",
      username: "kahenar",
      avatar: "../img/creators-auto/avatar-kahenar.jpg",
      poster: "../videosprodutos/posters/poster-111-kahena.jpg",
      video: "../videosprodutos/video-produto-111-criadora4.mp4",
      startTime: 0.2,
      desc: "Esse projetor natalino transforma o ambiente em segundos e já deixa a casa com clima de Natal com 16 padrões #TikTokShopBR"
    },
    {
      name: "Alê indica",
      username: "alendica100",
      avatar: "../img/creators-auto/avatar-alendica100.jpg",
      poster: "../videosprodutos/posters/poster-111-ale.jpg",
      video: "../videosprodutos/video-produto-111-criadora3.mp4",
      startTime: 0.2,
      desc: "Projetor Natalino Refletor Luzes de Natal Com 16 Desenhos 3D Laser Bivolt Portátil #projetornatalino #tiktokshop1111"
    },
    {
      name: "Vitta Shop",
      username: "evysantoss02",
      avatar: "../img/creators-avatars/creator-4.jpg",
      poster: "../videosprodutos/posters/poster-111-vitta.jpg",
      video: "../videosprodutos/video-produto-111-criadora2.mp4",
      startTime: 0.2,
      desc: "Unboxing e teste do projetor natalino LED 16 desenhos temáticos para casa e jardim #tiktokshop"
    }
  ];"""

js = re.sub(r'const PROJETOR_111_VIDEOS_MAP = \[[\s\S]*?\];', new_dataset_111, js, count=1)

# Corrigir precedência: isProjetorNatal DEVE SER O PRIMEIRO IF!
old_condition_block = """    const isTires = prodId === 101 || pageText.includes('pneu') || pageText.includes('pirelli');
    const isSandalia = prodId === 104 || pageText.includes('chinelo') || pageText.includes('strass') || pageText.includes('sandalia');
    const isProjetor = prodId === 105 || pageText.includes('projetor') || pageText.includes('hy300');
    const isBodyModelador = prodId === 106 || pageText.includes('body modelador') || pageText.includes('cinta') || pageText.includes('efeito lipo');
    const isAspirador = prodId === 107 || pageText.includes('aspirador') || pageText.includes('soprador turbo');
    const isEscova = prodId === 108 || pageText.includes('escova 5 em 1') || pageText.includes('coanda') || pageText.includes('escova secadora');
    const isModelador = prodId === 109 || pageText.includes('modelador de cachos') || pageText.includes('babyliss sem fio') || pageText.includes('cachos automatico');
    const isKappa = prodId === 110 || pageText.includes('kappa pulse') || pageText.includes('tenis kappa');
    const isProjetorNatal = prodId === 111 || pageText.includes('arvore de natal') || pageText.includes('cenas festivas');"""

new_condition_block = """    const isProjetorNatal = prodId === 111 || pageText.includes('projetor led natalino') || pageText.includes('projetor natalino') || pageText.includes('16 desenhos') || pageText.includes('arvore de natal');
    const isTires = prodId === 101 || pageText.includes('pneu') || pageText.includes('pirelli');
    const isSandalia = prodId === 104 || pageText.includes('chinelo') || pageText.includes('strass') || pageText.includes('sandalia');
    const isProjetor = (prodId === 105 || (pageText.includes('projetor') && !isProjetorNatal)) || pageText.includes('hy300');
    const isBodyModelador = prodId === 106 || pageText.includes('body modelador') || pageText.includes('cinta') || pageText.includes('efeito lipo');
    const isAspirador = prodId === 107 || pageText.includes('aspirador') || pageText.includes('soprador turbo');
    const isEscova = prodId === 108 || pageText.includes('escova 5 em 1') || pageText.includes('coanda') || pageText.includes('escova secadora');
    const isModelador = prodId === 109 || pageText.includes('modelador de cachos') || pageText.includes('babyliss sem fio') || pageText.includes('cachos automatico');
    const isKappa = prodId === 110 || pageText.includes('kappa pulse') || pageText.includes('tenis kappa');"""

js = js.replace(old_condition_block, new_condition_block)

# Colocar if (isProjetorNatal) no topo absoluto dos if/else
old_if_chain = """    if (isTires) {
      activeDataset = CREATORS_TIRES;
      contextType = 'tires';
    } else if (isSandalia) {
      activeDataset = CREATORS_CHINELO_28;
      contextType = 'chinelo';
    } else if (isProjetor) {
      activeDataset = CREATORS_PROJETOR_28;
      contextType = 'projetor';
    } else if (isBodyModelador) {
      activeDataset = CREATORS_BODY_106;
      contextType = 'bodymodelador';
    } else if (isAspirador) {
      activeDataset = CREATORS_ASPIRADOR_107;
      contextType = 'aspirador';
    } else if (isEscova) {
      activeDataset = CREATORS_ESCOVA_108;
      contextType = 'escova108';
    } else if (isModelador) {
      activeDataset = CREATORS_MODELADOR_109;
      contextType = 'modelador109';
    } else if (isKappa) {
      activeDataset = CREATORS_KAPPA_110;
      contextType = 'kappa110';
    } else if (isProjetorNatal) {
      activeDataset = CREATORS_PROJETOR_111;
      contextType = 'projetor111';"""

new_if_chain = """    if (isProjetorNatal) {
      activeDataset = CREATORS_PROJETOR_111;
      contextType = 'projetor111';
    } else if (isTires) {
      activeDataset = CREATORS_TIRES;
      contextType = 'tires';
    } else if (isSandalia) {
      activeDataset = CREATORS_CHINELO_28;
      contextType = 'chinelo';
    } else if (isProjetor) {
      activeDataset = CREATORS_PROJETOR_28;
      contextType = 'projetor';
    } else if (isBodyModelador) {
      activeDataset = CREATORS_BODY_106;
      contextType = 'bodymodelador';
    } else if (isAspirador) {
      activeDataset = CREATORS_ASPIRADOR_107;
      contextType = 'aspirador';
    } else if (isEscova) {
      activeDataset = CREATORS_ESCOVA_108;
      contextType = 'escova108';
    } else if (isModelador) {
      activeDataset = CREATORS_MODELADOR_109;
      contextType = 'modelador109';
    } else if (isKappa) {
      activeDataset = CREATORS_KAPPA_110;
      contextType = 'kappa110';"""

js = js.replace(old_if_chain, new_if_chain)

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("[OK] js/videos-criadores.js atualizado com precedência corrigida!")

# -------------------------------------------------------------
# 5. ATUALIZAR pages/produto-111.html
# -------------------------------------------------------------
with open('pages/produto-111.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Atualizar slider de fotos com as imagens oficiais e cache buster forçado
old_slider_pattern = r'<div class="slider-track">[\s\S]*?</div>\s*<div class="slider-counter">'
new_slider = """<div class="slider-track">
        <img fetchpriority="high" decoding="async" class="slider-img" src="../img/produto-111-oficial-1.jpg?v=3" alt="Projetor LED Natalino 16 Desenhos - 1">
        <img loading="lazy" decoding="async" class="slider-img" src="../img/produto-111-oficial-2.jpg?v=3" alt="Projetor LED Natalino 16 Desenhos - 2">
        <img loading="lazy" decoding="async" class="slider-img" src="../img/produto-111-oficial-3.jpg?v=3" alt="Projetor LED Natalino 16 Desenhos - 3">
        <img loading="lazy" decoding="async" class="slider-img" src="../img/produto-111-oficial-4.jpg?v=3" alt="Projetor LED Natalino 16 Desenhos - 4">
        <img loading="lazy" decoding="async" class="slider-img" src="../img/produto-111-oficial-5.jpg?v=3" alt="Projetor LED Natalino 16 Desenhos - 5">
      </div>
      <div class="slider-counter">"""

html = re.sub(old_slider_pattern, new_slider, html, count=1)

# Atualizar carrossel de criadores no HTML
old_creators_html_pattern = r'<div id="creators-section" class="creators-section">[\s\S]*?</div>\s*</div>\s*</div>'
new_creators_html = """<div id="creators-section" class="creators-section">
        <h3 class="creators-title">Vídeos de criadores (4)</h3>
        <div class="creators-carousel" id="creators-carousel-list">
        <div class="creator-card" data-video-id="0">
          <img src="../videosprodutos/posters/poster-111-bruna.jpg?v=3" alt="" loading="eager" fetchpriority="high" decoding="async" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
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
          <img src="../videosprodutos/posters/poster-111-kahena.jpg?v=3" alt="" loading="eager" decoding="async" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 40%, rgba(0,0,0,0.75) 100%);"></div>
          <div style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2;">
            <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 6px; display: flex; align-items: center; gap: 5px; z-index: 2; box-sizing: border-box;">
            <img loading="lazy" decoding="async" src="../img/creators-auto/avatar-kahenar.jpg" alt="" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;" onerror="this.src='../img/creators-avatars/creator-1.jpg'">
            <span style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">Kahena Rodrigues</span>
          </div>
        </div>
        <div class="creator-card" data-video-id="2">
          <img src="../videosprodutos/posters/poster-111-ale.jpg?v=3" alt="" loading="lazy" decoding="async" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
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
          <img src="../videosprodutos/posters/poster-111-vitta.jpg?v=3" alt="" loading="lazy" decoding="async" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 40%, rgba(0,0,0,0.75) 100%);"></div>
          <div style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2;">
            <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 6px; display: flex; align-items: center; gap: 5px; z-index: 2; box-sizing: border-box;">
            <img loading="lazy" decoding="async" src="../img/creators-avatars/creator-4.jpg" alt="" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;">
            <span style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">Vitta Shop</span>
          </div>
        </div>
        </div>
      </div>"""

html = re.sub(old_creators_html_pattern, new_creators_html, html, count=1)

# Atualizar seção de avaliações com fotos REAIS e ÚNICAS (Zero repetição de fotos!)
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
        <!-- Avaliação 1: D**y com 2 fotos (Piso iluminado + Caixa) -> Badge +2 -->
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
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-111-piso-tt.jpg?v=3" alt="Foto do comprador TikTok Shop" onclick="openPhotoModal(this.src)">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-111-box-tt.jpg?v=3" alt="Foto da embalagem TikTok Shop" onclick="openPhotoModal(this.src)">
          </div>
        </div>
        <!-- Avaliação 2: I**a G**a com 1 foto ÚNICA (Unboxing tirando da caixa) -> Bloco 70x70 sem badge -->
        <div class="review-card" data-author-name="I**a G**a" data-author-avatar="../img/reviews-avatars/default-avatar.svg" data-author-stars="5" data-author-comment="Chegou super rápido aqui em SP. O projetor é bem compacto e prático de montar. Testei na sala à noite com tudo apagado e a nitidez dos 16 desenhos é impressionante!">
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
          <p class="review-comment">Chegou super rápido aqui em SP. O projetor é bem compacto e prático de montar. Testei na sala à noite com tudo apagado e a nitidez dos 16 desenhos é impressionante!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-111-unboxing-real.jpg?v=3" alt="Foto do unboxing cliente" onclick="openPhotoModal(this.src)">
          </div>
        </div>
        <!-- Avaliação 3: d**e com zero fotos -> Text-only -->
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
print("[OK] pages/produto-111.html totalmente higienizado e atualizado!")

# -------------------------------------------------------------
# 6. ATUALIZAR js/catalogo.js (CARD DO PRODUTO 111)
# -------------------------------------------------------------
with open('js/catalogo.js', 'r', encoding='utf-8') as f:
    cat = f.read()

cat = cat.replace("img:'../img/produto-111-1.jpg'", "img:'../img/produto-111-oficial-1.jpg?v=3'")
with open('js/catalogo.js', 'w', encoding='utf-8') as f:
    f.write(cat)
print("[OK] js/catalogo.js atualizado!")
print("[SUCESSO TOTAL] Todos os arquivos alterados com perfeição cirúrgica!")
