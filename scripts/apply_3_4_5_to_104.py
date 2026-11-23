import re

file_path = 'pages/produto-104.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update/Add the CSS styles
css_block = '''<style id="tt-sobre-produto-style">
.about-product-section {
  margin-top: 14px;
  padding: 0 16px;
  background: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}
.about-section-title {
  font-size: 16px;
  font-weight: 700;
  color: #161823;
  margin: 0 0 14px 0;
  line-height: 1.3;
}
.about-subtitle {
  font-size: 14px;
  font-weight: 600;
  color: #161823;
  margin: 16px 0 10px 0;
  line-height: 1.3;
}
.details-attributes-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.detail-row {
  display: flex;
  align-items: flex-start;
  font-size: 13px;
  line-height: 19px;
}
.detail-label {
  width: 130px;
  min-width: 130px;
  flex-shrink: 0;
  color: #73747b;
  font-weight: 400;
}
.detail-value {
  flex: 1;
  color: #161823;
  font-weight: 400;
  word-break: break-word;
}

/* BOTÕES VER MAIS / VER MENOS 100% CENTRALIZADOS */
.btn-toggle-centered {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin: 12px auto 6px auto;
  background: none;
  border: none;
  font-size: 13.5px;
  font-weight: 600;
  color: #161823;
  cursor: pointer;
  gap: 4px;
  outline: none;
  -webkit-tap-highlight-color: transparent;
  padding: 6px 0;
}
.btn-toggle-centered .toggle-icon-centered {
  stroke: #161823;
  transition: transform 0.2s ease;
  width: 14px;
  height: 14px;
}
.btn-toggle-centered.is-expanded .toggle-icon-centered,
.btn-toggle-centered .toggle-icon-centered.rotated-up {
  transform: rotate(180deg);
}

/* ITEM 3: PLAYER DE VÍDEO OFICIAL TIKTOK COM CONTROLES */
.tiktok-video-card {
  position: relative;
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
  aspect-ratio: 9 / 16;
  max-height: 480px;
  background: #000000;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.tiktok-video-card video {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}
.tt-video-center-play {
  position: absolute;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.45);
  border: 2px solid #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  transition: opacity 0.2s ease, transform 0.2s ease;
  pointer-events: none;
}
.tt-video-center-play svg {
  margin-left: 3px;
}
.tiktok-video-card.is-playing .tt-video-center-play {
  opacity: 0;
  transform: scale(0.8);
}
.tt-video-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 38px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.85));
  display: flex;
  align-items: center;
  padding: 0 10px;
  gap: 8px;
  z-index: 3;
}
.tt-video-btn-play, .tt-video-btn-fs {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  outline: none;
  -webkit-tap-highlight-color: transparent;
}
.tt-video-time {
  font-size: 11.5px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  color: #ffffff;
  font-weight: 500;
  letter-spacing: 0.3px;
  min-width: 32px;
}
.tt-video-progress-bg {
  flex: 1;
  height: 3px;
  background: rgba(255, 255, 255, 0.35);
  border-radius: 2px;
  cursor: pointer;
  position: relative;
  display: flex;
  align-items: center;
}
.tt-video-progress-fill {
  height: 100%;
  width: 0%;
  background: #ffffff;
  border-radius: 2px;
  transition: width 0.1s linear;
}

/* ITEM 4: GUIA DE TAMANHOS OFICIAL TIKTOK SHOP */
.size-guide-card-tt {
  background: #f8f9fa;
  border: 1px solid #edf0f2;
  border-radius: 8px;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-top: 6px;
}
.size-guide-tag {
  background: #e6eef5;
  color: #1e293b;
  font-family: "Courier New", Courier, monospace, -apple-system, sans-serif;
  font-size: 13.5px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  letter-spacing: -0.2px;
}
.size-guide-pills-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
  max-width: 270px;
}
.size-pill-item {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  padding: 8px 14px;
  font-family: "Courier New", Courier, monospace, -apple-system, sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
  text-align: center;
  letter-spacing: 0.5px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

/* ITEM 5: DESCRIÇÃO REFINADA & FAIXA DIVISORA */
.description-text {
  font-size: 13.5px;
  line-height: 20px;
  color: #161823;
  word-break: break-word;
}
.description-text p {
  margin: 0 0 10px 0;
}
.tt-section-divider-thick {
  height: 8px;
  background: #f5f5f5;
  width: calc(100% + 32px);
  margin: 18px -16px 14px -16px;
  border: none;
}

#scroll-to-top-btn {
  position: fixed;
  right: 14px;
  bottom: 74px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #ffffff;
  border: 1px solid #ebebeb;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.14);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 990;
  opacity: 0;
  pointer-events: none;
  transform: translateY(10px);
  transition: opacity 0.25s ease, transform 0.25s ease;
  outline: none;
  -webkit-tap-highlight-color: transparent;
}
#scroll-to-top-btn.visible {
  opacity: 1 !important;
  pointer-events: auto !important;
  transform: translateY(0) !important;
}
</style>'''

# Replace old style block
content = re.sub(r'<style id="tt-sobre-produto-style">.*?</style>', css_block, content, flags=re.DOTALL)

# 2. Build the updated HTML for about-product-section
new_section = '''      <!-- SEÇÃO OFICIAL: SOBRE ESTE PRODUTO -->
      <div class="about-product-section" id="sobre-este-produto">
        <h2 class="about-section-title">Sobre este produto</h2>

        <!-- DETALHES -->
        <div class="product-details-block">
          <h3 class="about-subtitle">Detalhes</h3>
          <div class="details-attributes-grid">
            <div class="detail-row">
              <span class="detail-label">largura do sapato</span>
              <span class="detail-value">Médio</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Recurso</span>
              <span class="detail-value">Leve,Anti-derrapante,Respirável,À prova d'água</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Tipo de tira</span>
              <span class="detail-value">Tira no dedo do pé</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Altura do salto</span>
              <span class="detail-value">Salto plano (1 cm ou menos)</span>
            </div>
            <div class="detail-row is-hidden toggleable-row" style="display: none !important;">
              <span class="detail-label">Enfeite</span>
              <span class="detail-value">Strass,Nó</span>
            </div>
            <div class="detail-row is-hidden toggleable-row" style="display: none !important;">
              <span class="detail-label">Estilo</span>
              <span class="detail-value">Rua,Básico,Elegante,Festa</span>
            </div>
            <div class="detail-row is-hidden toggleable-row" style="display: none !important;">
              <span class="detail-label">Temporada</span>
              <span class="detail-value">Todas as estações</span>
            </div>
            <div class="detail-row is-hidden toggleable-row" style="display: none !important;">
              <span class="detail-label">Ocasião</span>
              <span class="detail-value">Casual</span>
            </div>
            <div class="detail-row is-hidden toggleable-row" style="display: none !important;">
              <span class="detail-label">Quantidade por embalagem</span>
              <span class="detail-value">1</span>
            </div>
            <div class="detail-row is-hidden toggleable-row" style="display: none !important;">
              <span class="detail-label">Padrão</span>
              <span class="detail-value">Nó</span>
            </div>
            <div class="detail-row is-hidden toggleable-row" style="display: none !important;">
              <span class="detail-label">Materiais</span>
              <span class="detail-value">Borracha</span>
            </div>
          </div>
          <button type="button" class="btn-toggle-centered" onclick="toggleProductDetails(this)">
            <span>Ver mais</span>
            <svg class="toggle-icon-centered" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
        </div>

        <!-- ITEM 3: VÍDEO OFICIAL DO PRODUTO (CONTROLES TIKTOK SHOP) -->
        <div class="product-video-block">
          <h3 class="about-subtitle">Vídeo</h3>
          <div class="tiktok-video-card" id="tt-product-video-wrapper" onclick="toggleTTVideo(event)">
            <video id="tt-product-video" src="../img/video-chinelo-oficial.mp4" poster="../img/poster-chinelo-oficial.jpg" playsinline preload="metadata"></video>
            <div class="tt-video-center-play" id="tt-center-play">
              <svg viewBox="0 0 24 24" width="28" height="28" fill="#ffffff"><polygon points="6 4 20 12 6 20 6 4"></polygon></svg>
            </div>
            <div class="tt-video-bar">
              <button type="button" class="tt-video-btn-play" id="tt-btn-play" onclick="event.stopPropagation(); toggleTTVideo();" aria-label="Play/Pause">
                <svg id="tt-icon-play" viewBox="0 0 24 24" width="14" height="14" fill="#ffffff"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                <svg id="tt-icon-pause" viewBox="0 0 24 24" width="14" height="14" fill="#ffffff" style="display:none;"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
              </button>
              <span class="tt-video-time" id="tt-cur-time">00:00</span>
              <div class="tt-video-progress-bg" id="tt-progress-bg" onclick="seekTTVideo(event)">
                <div class="tt-video-progress-fill" id="tt-progress-fill"></div>
              </div>
              <span class="tt-video-time" id="tt-dur-time">0:19</span>
              <button type="button" class="tt-video-btn-fs" id="tt-btn-fs" onclick="event.stopPropagation(); toggleTTFullscreen();" aria-label="Tela cheia">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <polyline points="9 21 3 21 3 15"></polyline>
                  <line x1="21" y1="3" x2="14" y2="10"></line>
                  <line x1="3" y1="21" x2="10" y2="14"></line>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- ITEM 4: GUIA DE TAMANHOS OFICIAL TIKTOK SHOP -->
        <div class="size-guide-block">
          <h3 class="about-subtitle">Guia de tamanhos</h3>
          <div class="size-guide-card-tt">
            <div class="size-guide-tag">
              <span>📐</span>
              <span>Tabela de Medidas – Calçados</span>
            </div>
            <div class="size-guide-pills-list">
              <div class="size-pill-item">33/34 — 23 cm</div>
              <div class="size-pill-item">35/36 — 24 cm</div>
              <div class="size-pill-item">37/38 — 25 cm</div>
              <div class="size-pill-item">39/40 — 26 cm</div>
            </div>
          </div>
          <button type="button" class="btn-toggle-centered" onclick="toggleSizeGuidePills(this)">
            <span>Ver mais</span>
            <svg class="toggle-icon-centered" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
        </div>

        <!-- ITEM 5: DESCRIÇÃO REFINADA OFICIAL TIKTOK SHOP -->
        <div class="description-section">
          <h3 class="about-subtitle">Descrição</h3>
          <div class="description-text">
            <p><strong>Descrição:</strong></p>
            <p>✨ <strong>Elegância em cada passo</strong> ✨</p>
            <p>Este chinelo feminino é perfeito para quem busca conforto e estilo. Com strass brilhante, ele adiciona um toque de luxo a qualquer look. A textura macia e leve garante um uso agradável o dia todo. Ideal para ocasiões que exigem um toque especial.</p>
            <p>• <strong>Características principais:</strong> • Strass brilhante • Textura macia • Peso leve</p>
            <p>Este chinelo combina perfeitamente com qualquer roupa, oferecendo estilo e conforto. Experimente e sinta a diferença!</p>
          </div>
          <button type="button" class="btn-toggle-centered" onclick="toggleDescriptionText(this)">
            <span>Ver menos</span>
            <svg class="toggle-icon-centered rotated-up" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
        </div>

        <!-- FAIXA DIVISORA CINZA GROSSA (8PX) OFICIAL TIKTOK -->
        <div class="tt-section-divider-thick"></div>

      </div><!-- fim about-product-section -->'''

section_pattern = r'<!-- SEÇÃO OFICIAL: SOBRE ESTE PRODUTO -->.*?</div><!-- fim about-product-section -->'
content = re.sub(section_pattern, new_section, content, flags=re.DOTALL)

# 3. Add JS functions for TikTok Video player, Centered buttons & scroll
js_helpers = '''<script>
// --- ITEM 3: CONTROLES DO PLAYER DE VÍDEO OFICIAL TIKTOK ---
function toggleTTVideo(e) {
  if (e && e.target && e.target.closest('.tt-video-bar')) return;
  var card = document.getElementById('tt-product-video-wrapper');
  var video = document.getElementById('tt-product-video');
  var iconPlay = document.getElementById('tt-icon-play');
  var iconPause = document.getElementById('tt-icon-pause');
  if (!video) return;

  if (video.paused) {
    video.play();
    if (card) card.classList.add('is-playing');
    if (iconPlay) iconPlay.style.display = 'none';
    if (iconPause) iconPause.style.display = 'block';
  } else {
    video.pause();
    if (card) card.classList.remove('is-playing');
    if (iconPlay) iconPlay.style.display = 'block';
    if (iconPause) iconPause.style.display = 'none';
  }
}

function seekTTVideo(e) {
  e.stopPropagation();
  var video = document.getElementById('tt-product-video');
  var bar = document.getElementById('tt-progress-bg');
  if (!video || !bar) return;
  var rect = bar.getBoundingClientRect();
  var pos = (e.clientX - rect.left) / rect.width;
  if (isFinite(video.duration) && video.duration > 0) {
    video.currentTime = pos * video.duration;
  }
}

function toggleTTFullscreen() {
  var card = document.getElementById('tt-product-video-wrapper');
  var video = document.getElementById('tt-product-video');
  var target = card || video;
  if (!target) return;
  if (!document.fullscreenElement) {
    if (target.requestFullscreen) target.requestFullscreen();
    else if (video.webkitEnterFullscreen) video.webkitEnterFullscreen();
  } else {
    if (document.exitFullscreen) document.exitFullscreen();
  }
}

(function initTTVideoEvents() {
  document.addEventListener('DOMContentLoaded', function() {
    var video = document.getElementById('tt-product-video');
    var curTime = document.getElementById('tt-cur-time');
    var durTime = document.getElementById('tt-dur-time');
    var fill = document.getElementById('tt-progress-fill');
    var card = document.getElementById('tt-product-video-wrapper');
    var iconPlay = document.getElementById('tt-icon-play');
    var iconPause = document.getElementById('tt-icon-pause');

    if (!video) return;

    function formatTime(s) {
      if (isNaN(s)) return '00:00';
      var m = Math.floor(s / 60);
      var sec = Math.floor(s % 60);
      return (m < 10 ? '0' : '') + m + ':' + (sec < 10 ? '0' : '') + sec;
    }

    video.addEventListener('timeupdate', function() {
      if (curTime) curTime.textContent = formatTime(video.currentTime);
      if (isFinite(video.duration) && video.duration > 0) {
        var pct = (video.currentTime / video.duration) * 100;
        if (fill) fill.style.width = pct + '%';
      }
    });

    video.addEventListener('loadedmetadata', function() {
      if (durTime && isFinite(video.duration)) {
        var m = Math.floor(video.duration / 60);
        var sec = Math.floor(video.duration % 60);
        durTime.textContent = m + ':' + (sec < 10 ? '0' : '') + sec;
      }
    });

    video.addEventListener('ended', function() {
      if (card) card.classList.remove('is-playing');
      if (iconPlay) iconPlay.style.display = 'block';
      if (iconPause) iconPause.style.display = 'none';
      if (fill) fill.style.width = '0%';
    });
  });
})();

// --- ITENS 4 & 5: TOGGLES CENTRALIZADOS ---
window.toggleProductDetails = function(btn) {
  if (!btn) return;
  var container = btn.closest('.product-details-block') || btn.parentElement;
  if (!container) return;
  var hiddenRows = container.querySelectorAll('.detail-row.toggleable-row');
  var isExpanded = btn.classList.contains('is-expanded');

  if (isExpanded) {
    hiddenRows.forEach(function(r) {
      r.classList.add('is-hidden');
      r.style.setProperty('display', 'none', 'important');
    });
    btn.classList.remove('is-expanded');
    var span = btn.querySelector('span');
    if (span) span.textContent = 'Ver mais';
    var icon = btn.querySelector('.toggle-icon-centered');
    if (icon) icon.classList.remove('rotated-up');
  } else {
    hiddenRows.forEach(function(r) {
      r.classList.remove('is-hidden');
      r.style.setProperty('display', 'flex', 'important');
    });
    btn.classList.add('is-expanded');
    var span = btn.querySelector('span');
    if (span) span.textContent = 'Ver menos';
    var icon = btn.querySelector('.toggle-icon-centered');
    if (icon) icon.classList.add('rotated-up');
  }
};

window.toggleSizeGuidePills = function(btn) {
  if (!btn) return;
  var isExpanded = btn.classList.contains('is-expanded');
  var span = btn.querySelector('span');
  var icon = btn.querySelector('.toggle-icon-centered');
  if (isExpanded) {
    btn.classList.remove('is-expanded');
    if (span) span.textContent = 'Ver mais';
    if (icon) icon.classList.remove('rotated-up');
  } else {
    btn.classList.add('is-expanded');
    if (span) span.textContent = 'Ver menos';
    if (icon) icon.classList.add('rotated-up');
  }
};

window.toggleDescriptionText = function(btn) {
  if (!btn) return;
  var desc = document.querySelector('.description-text');
  var isExpanded = btn.classList.contains('is-expanded');
  var span = btn.querySelector('span');
  var icon = btn.querySelector('.toggle-icon-centered');

  if (isExpanded) {
    btn.classList.remove('is-expanded');
    if (span) span.textContent = 'Ver mais';
    if (icon) icon.classList.remove('rotated-up');
    if (desc) desc.style.display = 'none';
  } else {
    btn.classList.add('is-expanded');
    if (span) span.textContent = 'Ver menos';
    if (icon) icon.classList.add('rotated-up');
    if (desc) desc.style.display = 'block';
  }
};

window.scrollToTop = function() {
  var sc = document.querySelector('.page-content');
  if (sc) sc.scrollTo({ top: 0, behavior: 'smooth' });
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

(function initScrollBtn() {
  function checkScrollBtn() {
    var btn = document.getElementById('scroll-to-top-btn');
    if (!btn) return;
    var sc = document.querySelector('.page-content');
    var sy = (sc && sc.scrollTop) ? sc.scrollTop : (window.scrollY || document.documentElement.scrollTop || 0);
    if (sy > 200) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }
  window.addEventListener('scroll', checkScrollBtn, { passive: true });
  document.addEventListener('DOMContentLoaded', function() {
    var sc = document.querySelector('.page-content');
    if (sc) sc.addEventListener('scroll', checkScrollBtn, { passive: true });
  });
})();
</script>'''

# Replace the script block before </body>
content = re.sub(r'<script>\s*window\.toggleProductDetails\s*=.*?</script>\s*</body>', js_helpers + '\n</body>', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied Items 3, 4, 5 to produto-104.html successfully!")

# Verify tag depth
app_idx = content.find('class="app-container"')
sub = content[app_idx:]
open_divs = len(re.findall(r'<div[\s>]', sub, re.IGNORECASE))
close_divs = len(re.findall(r'</div>', sub, re.IGNORECASE))
diff = open_divs - close_divs
print(f"Tag depth audit for produto-104.html: open = {open_divs}, close = {close_divs}, diff = {diff}")
