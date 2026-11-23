import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Atualizar buildCardHtml para ter classes específicas no badge e no tempo
old_badge = """            <!-- BADGE DE PLAY/PAUSE E TEMPO 1:1 TIKTOK SHOP OFICIAL -->
            <div class="tt-feed-video-badge" style="position:absolute; top:8px; left:8px; background:rgba(0,0,0,0.45); color:#fff; font-size:11px; font-weight:600; padding:2px 7.5px; border-radius:12px; display:inline-flex; align-items:center; gap:4.5px; backdrop-filter:blur(4px); -webkit-backdrop-filter:blur(4px); z-index:3; font-family:-apple-system,BlinkMacSystemFont,'Plus Jakarta Sans',sans-serif; letter-spacing:0.2px;">
              <!-- Ícone de Pause ❚❚ oficial (indicando reprodução contínua) -->
              <span style="display:inline-flex; align-items:center; gap:2px; height:9px;">
                <span style="width:2.5px; height:9px; background:#ffffff; border-radius:0.8px;"></span>
                <span style="width:2.5px; height:9px; background:#ffffff; border-radius:0.8px;"></span>
              </span>
              <span>${item.duracao || '00:28'}</span>
            </div>"""

new_badge = """            <!-- BADGE DE PLAY/PAUSE E TEMPO 1:1 TIKTOK SHOP OFICIAL -->
            <div class="tt-feed-video-badge" style="position:absolute; top:8px; left:8px; background:rgba(0,0,0,0.45); color:#fff; font-size:11px; font-weight:600; padding:2.5px 8px; border-radius:12px; display:inline-flex; align-items:center; gap:4.5px; backdrop-filter:blur(4px); -webkit-backdrop-filter:blur(4px); z-index:4; font-family:-apple-system,BlinkMacSystemFont,'Plus Jakarta Sans',sans-serif; letter-spacing:0.2px; cursor:pointer; user-select:none;">
              <!-- Ícone dinâmico: Pause ❚❚ quando tocando / Play ▶ quando pausado -->
              <span class="tt-feed-video-icon" style="display:inline-flex; align-items:center; height:9px;">
                <span style="display:inline-flex; align-items:center; gap:2px; height:9px;">
                  <span style="width:2.5px; height:9px; background:#ffffff; border-radius:0.8px;"></span>
                  <span style="width:2.5px; height:9px; background:#ffffff; border-radius:0.8px;"></span>
                </span>
              </span>
              <span class="tt-feed-video-time">00:00</span>
            </div>"""

if old_badge in code:
    code = code.replace(old_badge, new_badge)
    print("✓ Badge HTML atualizado com classes para timeupdate e play/pause")
else:
    print("AVISO: old_badge não bateu exato, vamos verificar se precisa de regex")

# 2. Adicionar o listener dinâmico de timeupdate após grid.innerHTML
old_grid_end = """  grid.innerHTML = `
    <div class="masonry-column" style="display:flex; flex-direction:column; flex:1; min-width:0;">
      ${colLeft.join('')}
    </div>
    <div class="masonry-column" style="display:flex; flex-direction:column; flex:1; min-width:0;">
      ${colRight.join('')}
    </div>
  `;
}"""

new_grid_end = """  grid.innerHTML = `
    <div class="masonry-column" style="display:flex; flex-direction:column; flex:1; min-width:0;">
      ${colLeft.join('')}
    </div>
    <div class="masonry-column" style="display:flex; flex-direction:column; flex:1; min-width:0;">
      ${colRight.join('')}
    </div>
  `;

  // === DINÂMICA OFICIAL TIKTOK SHOP: TEMPO PASSANDO EM TEMPO REAL & PLAY/PAUSE INTERATIVO ===
  grid.querySelectorAll('.related-card').forEach(card => {
    const video = card.querySelector('.related-card-video');
    const badge = card.querySelector('.tt-feed-video-badge');
    const timeSpan = card.querySelector('.tt-feed-video-time');
    const iconSpan = card.querySelector('.tt-feed-video-icon');

    if (!video || !badge || !timeSpan) return;

    function formatTime(sec) {
      if (!isFinite(sec) || sec < 0) return '00:00';
      const m = String(Math.floor(sec / 60)).padStart(2, '0');
      const s = String(Math.floor(sec % 60)).padStart(2, '0');
      return `${m}:${s}`;
    }

    function updateBadgeState() {
      if (video.paused) {
        // Ícone de Play ▶ quando pausado
        if (iconSpan) {
          iconSpan.innerHTML = `<svg width="8" height="9" viewBox="0 0 24 24" fill="#ffffff" style="display:block; margin-right:1px;"><polygon points="5 3 19 12 5 21 5 3"/></svg>`;
        }
      } else {
        // Ícone de Pause ❚❚ quando tocando
        if (iconSpan) {
          iconSpan.innerHTML = `<span style="display:inline-flex; align-items:center; gap:2px; height:9px;"><span style="width:2.5px; height:9px; background:#ffffff; border-radius:0.8px;"></span><span style="width:2.5px; height:9px; background:#ffffff; border-radius:0.8px;"></span></span>`;
        }
      }
    }

    // O tempo passa conforme o vídeo avança em tempo real
    video.addEventListener('timeupdate', () => {
      timeSpan.textContent = formatTime(video.currentTime);
      updateBadgeState();
    });

    video.addEventListener('play', updateBadgeState);
    video.addEventListener('pause', updateBadgeState);

    // Permite pausar/despausar ao clicar no badge do vídeo sem redirecionar
    badge.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (video.paused) {
        video.play().catch(() => {});
      } else {
        video.pause();
      }
      updateBadgeState();
    });
  });
}"""

if old_grid_end in code:
    code = code.replace(old_grid_end, new_grid_end)
    print("✓ Listener dinâmico de timeupdate e play/pause injetado com sucesso!")
else:
    print("ERRO: old_grid_end não encontrado!")
    exit(1)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ js/app.js atualizado com vídeo timer dinâmico 1:1!")
