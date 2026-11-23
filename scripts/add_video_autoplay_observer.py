import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Encontrar o bloco de inicialização dos vídeos
search_target = "// === DINÂMICA OFICIAL TIKTOK SHOP: TEMPO PASSANDO EM TEMPO REAL & PLAY/PAUSE INTERATIVO ==="
idx = code.find(search_target)
if idx == -1:
    print("ERRO: search_target não encontrado!")
    exit(1)

# Encontrar o fechamento da função renderRelacionados
idx_end = code.find('\n}\n\n// ===== ABAS DE NAVEGAÇÃO DO PRODUTO =====', idx)
if idx_end == -1:
    idx_end = code.find('\n}\n', idx)

print(f"Substituindo lógica de vídeo de {idx} até {idx_end}")

new_video_logic = """// === DINÂMICA OFICIAL TIKTOK SHOP: TEMPO PASSANDO EM TEMPO REAL & PLAY/PAUSE INTERATIVO ===
  const videoCards = grid.querySelectorAll('.related-card');
  
  // IntersectionObserver para Autoplay automático quando o vídeo entrar na tela (Padrão TikTok)
  const videoObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const vid = entry.target.querySelector('.related-card-video');
      if (!vid) return;
      if (entry.isIntersecting) {
        vid.muted = true;
        vid.play().catch(() => {});
      } else {
        vid.pause();
      }
    });
  }, { threshold: 0.25 });

  videoCards.forEach(card => {
    const video = card.querySelector('.related-card-video');
    const badge = card.querySelector('.tt-feed-video-badge');
    const timeSpan = card.querySelector('.tt-feed-video-time');
    const iconSpan = card.querySelector('.tt-feed-video-icon');

    if (!video || !badge || !timeSpan) return;

    // Observa o card para iniciar reprodução assim que entrar na tela
    videoObserver.observe(card);

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

    // O tempo passa rigorosamente conforme o vídeo avança em tempo real
    video.addEventListener('timeupdate', () => {
      timeSpan.textContent = formatTime(video.currentTime);
      updateBadgeState();
    });

    video.addEventListener('play', () => {
      updateBadgeState();
    });

    video.addEventListener('pause', () => {
      updateBadgeState();
    });

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
  });"""

new_code = code[:idx] + new_video_logic + code[idx_end:]
with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("✅ IntersectionObserver e dynamic timeupdate instalados com sucesso!")
