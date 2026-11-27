// PLAYER MODULAR LEVE DE VÍDEOS DE CRIADORES (SINGLE SOURCE OF TRUTH POR PRODUTO)
// Lê window.PRODUTO_CRIADORES injetado pelo SSR — reduz ~320KB de JS por página!
(function() {
  // Avatares FEMININOS reais mapeados do diretório FOTOSDEPERFIL
  const isPagesDir = typeof window !== 'undefined' && window.location.pathname.includes('/pages/');
  const avatarBase = isPagesDir ? '../img/creators-avatars/' : 'img/creators-avatars/';

  // 28 Fotos de Perfil Reais do TikTok de Pessoas Reais (sem fotos genéricas ou fakes)
  const AVATARS_FEMININOS = Array.from({ length: 28 }, (_, i) => `${avatarBase}creator-${i + 1}.jpg`);

  const avatarBodyBase = isPagesDir ? '../img/creators-body/' : 'img/creators-body/';
  const AVATARS_BODY = Array.from({ length: 28 }, (_, i) => `${avatarBodyBase}creator-${i + 1}.jpg`);

  const avatarAspiradorBase = isPagesDir ? '../img/creators-aspirador/' : 'img/creators-aspirador/';
  const AVATARS_ASPIRADOR = Array.from({ length: 28 }, (_, i) => `${avatarAspiradorBase}creator-${i + 1}.jpg`);

  const avatarTechBase = isPagesDir ? '../img/creators-tech/' : 'img/creators-tech/';
  const AVATARS_TECH = Array.from({ length: 28 }, (_, i) => `${avatarTechBase}creator-${i + 1}.jpg`);

  const avatarAutoBase = isPagesDir ? '../img/creators-auto/' : 'img/creators-auto/';
  const AVATARS_AUTO = Array.from({ length: 28 }, (_, i) => `${avatarAutoBase}creator-${i + 1}.jpg`);

  // Elementos globais do modal TikTok
  let ttModal = null;
  let ttVideo = null;
  let currentVideoIndex = 0;
  let videoList = [];

  function parseStatNumber(val, fallback) {
    if (typeof val === 'number' && !isNaN(val) && val > 0) return Math.round(val);
    if (typeof val === 'string' && val.trim()) {
      const s = val.trim();
      const km = s.match(/^(\d+(?:[.,]\d+)?)\s*(k|mil)\b/i);
      if (km) return Math.round(parseFloat(km[1].replace(',', '.')) * 1000);
      const mm = s.match(/^(\d+(?:[.,]\d+)?)\s*m\b/i);
      if (mm) return Math.round(parseFloat(mm[1].replace(',', '.')) * 1000000);
      const digits = s.replace(/[^\d]/g, '');
      if (digits) return parseInt(digits, 10);
    }
    return fallback || 0;
  }

  function formatNumber(num) {
    const n = parseStatNumber(num, 0);
    if (!n || n <= 0) return '0';
    return n.toLocaleString('pt-BR');
  }

  function getCreatorPostDate(idx) {
    const d = new Date();
    d.setDate(d.getDate() - (3 + ((idx * 5) % 24)));
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${mm}-${dd}`;
  }

  // Injeta estilos CSS necessários
  function injectStyles() {
    if (document.getElementById('tt-styles')) return;
    const style = document.createElement('style');
    style.id = 'tt-styles';
    style.innerHTML = `
      .creators-section:empty,
      .creators-section[style*="display: none"] {
        display: none !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        height: 0 !important;
        min-height: 0 !important;
      }
      .creators-section {
        padding: 14px 0 14px 14px !important;
        background: #ffffff !important;
        margin-bottom: 8px !important;
        border-bottom: 8px solid #f5f5f5 !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "TikTok Sans", "Plus Jakarta Sans", sans-serif !important;
      }
      .creators-title {
        font-size: 16px;
        font-weight: 700;
        color: #161823;
        margin-bottom: 12px;
        letter-spacing: -0.2px;
      }
      .creators-carousel {
        display: flex !important;
        gap: 8px !important;
        overflow-x: auto !important;
        padding: 0 14px 4px 0 !important;
        scroll-behavior: smooth !important;
        -webkit-overflow-scrolling: touch !important;
        scrollbar-width: none !important;
      }
      .creators-carousel::-webkit-scrollbar {
        display: none;
      }
      .creator-card {
        flex: 0 0 104px !important;
        width: 104px !important;
        height: 148px !important;
        border-radius: 8px !important;
        position: relative !important;
        overflow: hidden !important;
        cursor: pointer !important;
        background: #111 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08) !important;
        -webkit-tap-highlight-color: transparent !important;
      }
      .tt-modal {
        display: none;
        position: fixed !important;
        inset: 0 !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100vw !important;
        width: 100% !important;
        height: 100dvh !important;
        height: 100vh !important;
        height: -webkit-fill-available !important;
        max-height: 100dvh !important;
        background: #000 !important;
        z-index: 999999 !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        touch-action: none !important;
        user-select: none !important;
        -webkit-user-select: none !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
      }
      .tt-container {
        position: relative !important;
        width: 100% !important;
        max-width: 480px !important;
        height: 100% !important;
        max-height: 100% !important;
        background: #000 !important;
        display: flex !important;
        flex-direction: column !important;
        overflow: hidden !important;
        touch-action: none !important;
        box-sizing: border-box !important;
      }
      .tt-play-icon-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.95);
        width: 68px;
        height: 68px;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
        border-radius: 50%;
        display: none;
        align-items: center;
        justify-content: center;
        pointer-events: none;
        z-index: 15;
        transition: transform 0.15s, opacity 0.15s;
      }
      @keyframes ttDiscSpin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
      .tt-modal,
      .tt-modal button,
      .tt-modal input,
      .tt-modal span,
      .tt-modal div {
        font-family: 'TTProUI', 'BFOnlyNumbers', -apple-system, BlinkMacSystemFont, "TikTok Sans", sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
      }
      .tt-top-bar {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        padding: 14px 16px !important;
        padding-top: max(16px, calc(10px + env(safe-area-inset-top))) !important;
        display: flex !important;
        align-items: center !important;
        z-index: 16 !important;
        box-sizing: border-box !important;
        background: linear-gradient(180deg, rgba(0,0,0,0.38) 0%, rgba(0,0,0,0) 100%) !important;
        pointer-events: none !important;
      }
      .tt-back-btn {
        background: none !important;
        border: none !important;
        color: #ffffff !important;
        cursor: pointer !important;
        padding: 4px !important;
        margin-left: -4px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        pointer-events: auto !important;
        filter: drop-shadow(0 1px 3px rgba(0,0,0,0.45)) !important;
        -webkit-tap-highlight-color: transparent !important;
      }
      .tt-video-wrapper {
        position: relative !important;
        width: 100% !important;
        flex: 1 1 auto !important;
        min-height: 0 !important;
        display: flex !important;
        align-items: flex-start !important;
        justify-content: center !important;
        background: #000000 !important;
        overflow: hidden !important;
        touch-action: none !important;
        cursor: pointer !important;
        will-change: transform, opacity !important;
        box-sizing: border-box !important;
      }
      .tt-video-wrapper::after {
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        height: 230px !important;
        background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.52) 48%, rgba(0,0,0,0.94) 82%, #000000 100%) !important;
        pointer-events: none !important;
        z-index: 4 !important;
      }
      .tt-video {
        width: 100% !important;
        height: calc(100% - 76px) !important;
        object-fit: cover !important;
        background: #000000 !important;
        pointer-events: none !important;
        display: block !important;
      }
      .tt-right-actions {
        position: absolute !important;
        right: 10px !important;
        bottom: 12px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 15px !important;
        z-index: 12 !important;
        pointer-events: auto !important;
      }
      .tt-creator-wrapper {
        position: relative !important;
        margin-bottom: 8px !important;
        width: 47px !important;
        height: 47px !important;
      }
      .tt-creator-avatar {
        width: 47px !important;
        height: 47px !important;
        border-radius: 50% !important;
        border: 1.5px solid rgba(255, 255, 255, 0.95) !important;
        object-fit: cover !important;
        display: block !important;
        background: #1a1a1a !important;
        box-sizing: border-box !important;
      }
      .tt-follow-btn {
        position: absolute !important;
        bottom: -9px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 21px !important;
        height: 21px !important;
        background: #f7355a !important;
        color: #ffffff !important;
        border-radius: 50% !important;
        border: none !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.35) !important;
      }
      .tt-action-btn {
        background: none !important;
        border: none !important;
        color: #ffffff !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 3px !important;
        cursor: pointer !important;
        padding: 0 !important;
        -webkit-tap-highlight-color: transparent !important;
      }
      .tt-action-btn svg {
        filter: drop-shadow(0 1px 3px rgba(0,0,0,0.38)) !important;
      }
      .tt-action-label {
        font-size: 12.5px !important;
        font-weight: 500 !important;
        color: #ffffff !important;
        line-height: 1.15 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.65) !important;
      }
      .tt-music-disc {
        width: 38px !important;
        height: 38px !important;
        border-radius: 50% !important;
        overflow: hidden !important;
        margin-top: 4px !important;
        border: 1.5px solid rgba(255,255,255,0.22) !important;
        background: #1a1a1a !important;
        flex-shrink: 0 !important;
        animation: ttDiscSpin 7s linear infinite !important;
      }
      .tt-music-disc img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        display: block !important;
      }
      .tt-left-info {
        position: absolute !important;
        left: 14px !important;
        right: 74px !important;
        bottom: 12px !important;
        color: #ffffff !important;
        z-index: 12 !important;
        pointer-events: auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
      }
      .tt-product-anchor {
        display: inline-flex !important;
        align-items: center !important;
        gap: 9px !important;
        background: rgba(38, 38, 42, 0.56) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 7.5px 12px 7.5px 9px !important;
        margin: 0 0 10px 0 !important;
        cursor: pointer !important;
        color: #ffffff !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        transition: transform 0.15s ease !important;
      }
      .tt-product-anchor:active {
        transform: scale(0.97) !important;
      }
      .tt-anchor-cart-badge {
        width: 23px !important;
        height: 23px !important;
        border-radius: 5.5px !important;
        background: #ff6221 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
      }
      .tt-anchor-lines {
        display: flex !important;
        flex-direction: column !important;
        gap: 1.5px !important;
        min-width: 0 !important;
        flex: 1 !important;
      }
      .tt-anchor-line1 {
        font-size: 13px !important;
        line-height: 1.22 !important;
        color: #ffffff !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
      }
      .tt-anchor-title {
        color: #ffffff !important;
        font-weight: 600 !important;
      }
      .tt-anchor-line2 {
        font-size: 11.5px !important;
        font-weight: 400 !important;
        line-height: 1.2 !important;
        color: rgba(255, 255, 255, 0.86) !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
      }
      .tt-username-row {
        display: flex !important;
        align-items: baseline !important;
        gap: 5px !important;
        margin: 0 0 6px 0 !important;
        max-width: 100% !important;
      }
      .tt-username {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        margin: 0 !important;
        line-height: 1.25 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.6) !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
      }
      .tt-post-date {
        font-size: 14.5px !important;
        font-weight: 500 !important;
        color: rgba(255, 255, 255, 0.72) !important;
        line-height: 1.25 !important;
        flex-shrink: 0 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5) !important;
      }
      .tt-desc {
        font-size: 14px !important;
        font-weight: 400 !important;
        color: rgba(255, 255, 255, 0.95) !important;
        line-height: 1.35 !important;
        margin: 0 0 8px 0 !important;
        display: -webkit-box !important;
        -webkit-line-clamp: 2 !important;
        -webkit-box-orient: vertical !important;
        overflow: hidden !important;
        word-break: break-word !important;
        width: 100% !important;
      }
      .tt-desc.is-expanded {
        -webkit-line-clamp: 8 !important;
      }
      .tt-music-row {
        display: flex !important;
        align-items: center !important;
        gap: 7px !important;
        max-width: 100% !important;
      }
      .tt-music-text {
        font-size: 13.5px !important;
        font-weight: 400 !important;
        color: #ffffff !important;
        line-height: 1.25 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        max-width: 250px !important;
      }
      .tt-bottom-bar-comment {
        width: 100% !important;
        background: #000000 !important;
        padding: 8px 14px calc(10px + env(safe-area-inset-bottom, 0px)) 14px !important;
        box-sizing: border-box !important;
        flex-shrink: 0 !important;
        z-index: 15 !important;
      }
      .tt-bottom-comment-pill {
        width: 100% !important;
        height: 44px !important;
        background: #333333 !important;
        border-radius: 999px !important;
        padding: 0 16px !important;
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
        box-sizing: border-box !important;
        cursor: pointer !important;
      }
      .tt-bottom-comment-placeholder {
        flex: 1 !important;
        font-size: 14.5px !important;
        font-weight: 400 !important;
        color: rgba(255, 255, 255, 0.62) !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
      }
      .tt-bottom-comment-icons {
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
        flex-shrink: 0 !important;
        color: rgba(255, 255, 255, 0.82) !important;
      }
      /* Modo Comentários Aberto: Vídeo encolhe no topo preto (35.7%) + Gaveta branca 64.3% 1:1 */
      .tt-modal.comments-open .tt-top-bar,
      .tt-modal.comments-open .tt-right-actions,
      .tt-modal.comments-open .tt-left-info,
      .tt-modal.comments-open .tt-bottom-bar-comment,
      .tt-modal.comments-open .tt-video-wrapper::after {
        opacity: 0 !important;
        visibility: hidden !important;
        pointer-events: none !important;
      }
      .tt-modal.comments-open .tt-video-wrapper {
        flex: 0 0 35.7% !important;
        height: 35.7% !important;
        align-items: center !important;
        justify-content: center !important;
        background: #000000 !important;
        transition: height 0.26s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
      }
      .tt-modal.comments-open .tt-video {
        width: auto !important;
        height: 100% !important;
        max-width: 100% !important;
        aspect-ratio: 9 / 16 !important;
        object-fit: cover !important;
      }
      .tt-comments-drawer {
        position: absolute !important;
        bottom: -100% !important;
        left: 0 !important;
        width: 100% !important;
        height: 64.3% !important;
        background: #ffffff !important;
        border-radius: 14px 14px 0 0 !important;
        z-index: 30 !important;
        transition: bottom 0.28s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
        display: flex !important;
        flex-direction: column !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
      }
      .tt-comments-drawer.open {
        bottom: 0 !important;
      }
      .tt-drawer-shop-bar {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 10px !important;
        padding: 12px 14px 6px 14px !important;
        background: #ffffff !important;
        flex-shrink: 0 !important;
      }
      .tt-drawer-shop-left {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        min-width: 0 !important;
        flex: 1 !important;
        cursor: pointer !important;
      }
      .tt-drawer-shop-cart {
        width: 28px !important;
        height: 28px !important;
        border-radius: 6px !important;
        background: #ff6221 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
      }
      .tt-drawer-shop-texts {
        display: flex !important;
        flex-direction: column !important;
        min-width: 0 !important;
        flex: 1 !important;
        gap: 1px !important;
      }
      .tt-drawer-shop-name {
        font-size: 13.5px !important;
        font-weight: 600 !important;
        color: #161823 !important;
        line-height: 1.25 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
      }
      .tt-drawer-shop-sold {
        font-size: 12px !important;
        font-weight: 400 !important;
        color: #8a8b91 !important;
        line-height: 1.2 !important;
      }
      .tt-drawer-close {
        width: 28px !important;
        height: 28px !important;
        border-radius: 50% !important;
        background: #f5f5f6 !important;
        border: none !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        color: #52545c !important;
        flex-shrink: 0 !important;
        padding: 0 !important;
      }
      .tt-drawer-count-row {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 5px !important;
        padding: 6px 16px 10px 16px !important;
        flex-shrink: 0 !important;
      }
      .tt-drawer-title {
        font-size: 13.5px !important;
        font-weight: 600 !important;
        color: #161823 !important;
        line-height: 1.2 !important;
      }
      .tt-drawer-list {
        flex: 1 1 auto !important;
        overflow-y: auto !important;
        padding: 8px 16px 12px 16px !important;
        -webkit-overflow-scrolling: touch !important;
      }
      .tt-comment-item {
        display: flex !important;
        align-items: flex-start !important;
        gap: 11px !important;
        margin-bottom: 18px !important;
      }
      .tt-comment-avatar {
        width: 36px !important;
        height: 36px !important;
        border-radius: 50% !important;
        object-fit: cover !important;
        flex-shrink: 0 !important;
        background: #f0f0f0 !important;
      }
      .tt-comment-user {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #8a8b91 !important;
        line-height: 1.25 !important;
      }
      .tt-comment-text {
        font-size: 14.5px !important;
        font-weight: 400 !important;
        color: #161823 !important;
        line-height: 1.35 !important;
        margin-top: 2px !important;
      }
      .tt-comment-first-badge {
        display: inline-block !important;
        background: #f3f3f4 !important;
        color: #73747b !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        padding: 2px 7px !important;
        border-radius: 4px !important;
        margin-top: 5px !important;
      }
      .tt-comment-footer {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        margin-top: 6px !important;
      }
      .tt-comment-meta-left {
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
      }
      .tt-comment-date {
        font-size: 12.5px !important;
        color: #9a9ba1 !important;
        font-weight: 400 !important;
      }
      .tt-comment-reply {
        font-size: 12.5px !important;
        color: #73747b !important;
        font-weight: 500 !important;
        cursor: pointer !important;
      }
      .tt-comment-actions-right {
        display: flex !important;
        align-items: center !important;
        gap: 18px !important;
        color: #73747b !important;
      }
      .tt-comment-like-box,
      .tt-comment-dislike-box {
        display: inline-flex !important;
        align-items: center !important;
        gap: 4px !important;
        color: #73747b !important;
        font-size: 12.5px !important;
        cursor: pointer !important;
        padding: 2px !important;
        -webkit-tap-highlight-color: transparent !important;
      }
      .tt-comment-input-bar {
        display: flex !important;
        align-items: center !important;
        padding: 8px 14px calc(10px + env(safe-area-inset-bottom, 0px)) 14px !important;
        border-top: 1px solid #f0f0f2 !important;
        background: #ffffff !important;
        box-sizing: border-box !important;
        flex-shrink: 0 !important;
      }
      .tt-comment-input-pill-wrap {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        height: 42px !important;
        background: #f1f1f2 !important;
        border-radius: 999px !important;
        padding: 0 14px !important;
        gap: 12px !important;
        box-sizing: border-box !important;
      }
      .tt-comment-input {
        flex: 1 !important;
        height: 100% !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        font-size: 14.5px !important;
        font-weight: 400 !important;
        color: #161823 !important;
        outline: none !important;
        min-width: 0 !important;
      }
      .tt-comment-input::placeholder {
        color: #9a9ba1 !important;
      }
      .tt-drawer-pill-icons {
        display: flex !important;
        align-items: center !important;
        gap: 13px !important;
        color: #161823 !important;
        flex-shrink: 0 !important;
      }
      .tt-comment-submit-btn {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #fe2c55;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        flex-shrink: 0;
        transition: transform 0.15s, opacity 0.15s;
        box-shadow: 0 2px 8px rgba(254, 44, 85, 0.3);
      }
      .tt-comment-submit-btn:active {
        transform: scale(0.92);
      }
      .tt-toast {
        position: absolute;
        top: 75px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(22, 24, 35, 0.92);
        color: #fff;
        padding: 10px 20px;
        border-radius: 24px;
        font-size: 13px;
        font-weight: 600;
        z-index: 99999;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.25s ease, transform 0.25s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        white-space: nowrap;
      }
      .tt-toast.show {
        opacity: 1;
        transform: translateX(-50%) translateY(8px);
      }
    `;
    document.head.appendChild(style);
  }


  function initCarousel() {
    const targetContainer = document.getElementById('creators-section');
    if (!targetContainer) return;

    let activeDataset = Array.isArray(window.PRODUTO_CRIADORES) ? window.PRODUTO_CRIADORES.slice() : [];
    let contextType = window.PRODUTO_CRIADORES_CTX || 'general';
    const isModelador = contextType === 'modelador109';
    const isEscova = contextType === 'escova108';

    const descVidEl = document.querySelector('#tt-product-video, .product-video-player, #product-desc-video');
    const descVidBase = descVidEl ? (descVidEl.getAttribute('src') || '').split('#')[0].trim() : '';
    if (descVidBase && activeDataset.length > 0) {
      const filtered = activeDataset.filter(item => {
        const itemBase = ((item.video || item.localVideo || '').split('#')[0]).trim();
        return itemBase && itemBase !== descVidBase;
      });
      if (filtered.length > 0) activeDataset = filtered;
    }

    const seen = new Set();
    activeDataset = activeDataset.filter(item => {
      const b = ((item.video || '').split('#')[0]).trim();
      if (!b || seen.has(b)) return false;
      seen.add(b);
      return true;
    });

    if (!activeDataset || activeDataset.length === 0) {
      targetContainer.innerHTML = '';
      targetContainer.style.setProperty('display', 'none', 'important');
      return;
    }

    const totalVideosCount = activeDataset.length;
    const countBadge = totalVideosCount >= 30 ? '30+' : (totalVideosCount >= 20 ? (totalVideosCount + '+') : totalVideosCount);

    // Popula a lista oficial de vídeos em memória com metadados e comentários realistas
    videoList = [];
    for (let i = 0; i < totalVideosCount; i++) {
      const originalItem = activeDataset[i];
      const videoId = i;
      
      const likes = parseStatNumber(originalItem.likes, 2840 + ((i * 1741) % 6400));
      const comments = parseStatNumber(originalItem.commentsCount || originalItem.comments, 42 + ((i * 23) % 160));
      const saves = parseStatNumber(originalItem.saves, Math.max(95, Math.floor(likes * 0.135)));
      const shares = parseStatNumber(originalItem.shares, Math.max(48, Math.floor(likes * 0.145)));

      const item = {
        id: videoId,
        name: originalItem.name || originalItem.username || 'Criador',
        username: originalItem.username || String(originalItem.name || 'criador').toLowerCase().replace(/\s+/g, '_'),
        avatar: originalItem.avatar,
        poster: originalItem.poster,
        video: originalItem.video,
        postDate: originalItem.postDate || getCreatorPostDate(i),
        startTime: originalItem.startTime || 0.2,
        likes: likes,
        commentsCount: comments,
        saves: saves,
        shares: shares,
        description: originalItem.description || originalItem.desc || originalItem.title || '',
        liked: false,
        saved: false,
        followed: false,
        commentsList: (function() {
          if (contextType === 'modelador109' || (typeof isModelador !== 'undefined' && isModelador)) {
            return [
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_1.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_1.jpg',
                user: 'mari.cachos',
                text: 'Menina do céu, esquenta rápido? Meu cabelo é grosso e difícil de pegar cacho!',
                date: 'Há 18 min',
                likes: 42,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/creators-cabelo/creator-109-5.jpg' : 'img/creators-cabelo/creator-109-5.jpg',
                user: 'maryonlive',
                isCreator: true,
                text: 'Esquenta em 30s amiga! Uso em 180°C e o cacho dura o dia todo sem precisar de laquê 😍✨',
                date: 'Há 15 min',
                likes: 89,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_2.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_2.jpg',
                user: 'bia_closet',
                text: 'Esse modelador sem fio me salvou no casamento! Retoquei no carro em 5 minutos ✨',
                date: 'Há 1 hora',
                likes: 29,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_3.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_3.jpg',
                user: 'camila_looks',
                text: 'Tinha pavor de queimar o dedo ou a orelha com babyliss comum, esse isolamento térmico é perfeito!',
                date: 'Há 3 horas',
                likes: 18,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_4.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_4.jpg',
                user: 'ju_costa',
                text: 'Comprei pelo carrinho laranja e chegou em 3 dias aqui em Curitiba! Amei muito ❤️',
                date: 'Ontem',
                likes: 15,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_5.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_5.jpg',
                user: 'larissa.silva',
                text: 'A bateria dura pra fazer a cabeça inteira duas vezes tranquilamente. Muito prático!',
                date: 'Há 1 dia',
                likes: 11,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_6.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_6.jpg',
                user: 'gabi_couto',
                text: 'Pega em cabelo curto/chanel ou só em cabelo comprido?',
                date: 'Há 1 dia',
                likes: 7,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/creators-cabelo/creator-109-5.jpg' : 'img/creators-cabelo/creator-109-5.jpg',
                user: 'maryonlive',
                isCreator: true,
                text: 'Pega super bem em curto também amiga! É só colocar a mecha mais perto da ponta que ele puxa suave 🥰',
                date: 'Há 1 dia',
                likes: 34,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_7.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_7.jpg',
                user: 'tami.albuquerque',
                text: 'Vem com o cabo pra carregar? É USB normal?',
                date: 'Há 2 dias',
                likes: 5,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_8.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_8.jpg',
                user: 'carol_rezende',
                text: 'Vem sim com o cabo USB-C e os dois pentes e clipes de mecha, caixinha completa!',
                date: 'Há 2 dias',
                likes: 21,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_9.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_9.jpg',
                user: 'renatinha_moda',
                text: 'Comprei na promoção relâmpago de ontem, já enviaram código de rastreio!',
                date: 'Há 3 dias',
                likes: 14,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_10.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_10.jpg',
                user: 'biancaprado.fit',
                text: 'Amei que dá pra escolher o lado do cacho (L ou R), fica com acabamento de salão.',
                date: 'Há 4 dias',
                likes: 19,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_11.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_11.jpg',
                user: 'paty.coimbra',
                text: 'Gente, o preço tá muito barato pelo que entrega, na gringa custa mais de 50 dólares.',
                date: 'Há 5 dias',
                likes: 27,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_12.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_12.jpg',
                user: 'isabella_style',
                text: 'O meu chegou hoje cedo! Já testei e aprovei com louvor 😍👏',
                date: 'Há 6 dias',
                likes: 9,
                liked: false
              }
            ];
          } else if (contextType === 'escova108' || (typeof isEscova !== 'undefined' && isEscova)) {
            return [
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_6.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_6.jpg',
                user: 'aninha_hair',
                text: 'Gente essa escova 5 em 1 seca e modela ao mesmo tempo? Fica com brilho de salão?',
                date: 'Há 25 min',
                likes: 38,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_7.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_7.jpg',
                user: 'paty_style',
                text: 'O efeito Coanda de sugar a mecha é real, não queima nada o cabelo!',
                date: 'Há 2 horas',
                likes: 24,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_8.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_8.jpg',
                user: 'carol.dicas',
                text: 'Chegou em 3 dias aqui em SP, bem embalada com todas as 5 ponteiras. Apaixonada!',
                date: 'Ontem',
                likes: 19,
                liked: false
              }
            ];
          } else if (contextType === 'churrasqueira_14') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Galera, recomendo colocar um pouquinho de água na bandeja antes de ligar. Não faz fumaça e a gordura sai na água fácil de lavar! 🥩👏',
                date: 'Há 2 horas',
                likes: 56,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-churras/creator-fernando.jpg' : 'img/avatars-churras/creator-fernando.jpg',
                user: 'churras_em_familia',
                text: 'Realmente zero fumaça no apartamento! Coloquei água na bandeja coletora e assou a picanha perfeitamente 🔥',
                date: 'Há 1 hora',
                likes: 38,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-churras/creator-rodrigo.jpg' : 'img/avatars-churras/creator-rodrigo.jpg',
                user: 'gustavo_ape12',
                text: 'Os 5 espetos rotativos giram super macio. Melhor investimento de churrasco da vida!',
                date: 'Há 3 horas',
                likes: 24,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-churras/creator-patricia.jpg' : 'img/avatars-churras/creator-patricia.jpg',
                user: 'paty_gourmet',
                text: 'Cabe uma peça de maminha inteira nos espetos centrais? Fica bem dourada?',
                date: 'Há 4 horas',
                likes: 19,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-churras/creator-lucas.jpg' : 'img/avatars-churras/creator-lucas.jpg',
                user: 'rodrigo_moura',
                text: 'Chegou em 2 dias aqui pela Stone Shop, caixa lacrada com todos os 5 espetos e manual.',
                date: 'Ontem',
                likes: 17,
                liked: false
              }
            ];
          } else if (contextType === 'churrasqueira_15') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Galera, o cooler com entrada USB/pilhas acende a brasa em 3 minutos sem sofrer! Fica zero fumaça na varanda 🔥🥩',
                date: 'Há 2 horas',
                likes: 62,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-biscuitt/creator-carlos.jpg' : 'img/avatars-biscuitt/creator-carlos.jpg',
                user: 'marcelo_bbq',
                text: 'O cooler com regulador USB acelera o acendimento em 3 minutos, não precisa ficar abanando! 👏',
                date: 'Há 1 hora',
                likes: 38,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-biscuitt/creator-renata.jpg' : 'img/avatars-biscuitt/creator-renata.jpg',
                user: 'paty_varandinha',
                text: 'Fiz picanha e queijo coalho na varanda ontem, zero fumaça no apê! Meus vizinhos nem sentiram cheiro ❤️',
                date: 'Há 3 horas',
                likes: 27,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-biscuitt/creator-thiago.jpg' : 'img/avatars-biscuitt/creator-thiago.jpg',
                user: 'thiago_brasa',
                text: 'Gasta um punhado minúsculo de carvão. Uma bag de 2kg de carvão dura semanas!',
                date: 'Há 4 horas',
                likes: 21,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-biscuitt/creator-gabi.jpg' : 'img/avatars-biscuitt/creator-gabi.jpg',
                user: 'carol_ape12',
                text: 'Chegou em 2 dias aqui pela Stone Shop, a bag térmica é linda e a grelha limpa na pia sem esforço.',
                date: 'Ontem',
                likes: 15,
                liked: false
              }
            ];
          } else if (contextType === 'mesa118' || contextType === 'mesa_118') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Gente, a mesa é maravilhosa e o acabamento chanfrado com as cadeiras em suede é super confortável! Vale cada centavo ✨🪑',
                date: 'Há 2 horas',
                likes: 47,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_6.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_6.jpg',
                user: 'larissa_home',
                text: 'As cadeiras em suede são muito confortáveis e a espuma D26 não afunda. Entrega da Stone Shop foi super rápida!',
                date: 'Há 1 hora',
                likes: 31,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_3.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_3.jpg',
                user: 'felipe_moraes',
                text: 'Comprei o modelo Freijó com Off White, mesa muito estável e firme, não balança nada. Amei demais!',
                date: 'Há 3 horas',
                likes: 22,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_8.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_8.jpg',
                user: 'camila_ape54',
                text: 'Coube perfeitamente na minha sala de jantar compacta. Recomendo de olhos fechados!',
                date: 'Há 4 horas',
                likes: 18,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_10.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_10.jpg',
                user: 'renata_design',
                text: 'Chegou tudo muito bem embalado com proteção reforçada nas quinas do tampo. Nota 10!',
                date: 'Ontem',
                likes: 14,
                liked: false
              }
            ];
          } else if (contextType === 'kitmondial136') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Gente, esse kit da Mondial com liquidificador 550W + batedeira 400W + copo medidor + espátula por R$ 99,90 na Black Friday é loucura! Corre antes de acabar 🔥🖤', date: 'Há 1 hora', likes: 134, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_44.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_44.jpg', user: 'claudia_cozinha', text: 'Comprei ontem no PIX e já despacharam! Só a batedeira no shopping tá 140 reais 😍', date: 'Há 30 min', likes: 52, liked: false }
            ];
          } else if (contextType === 'cortinaled138') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Olha o brilho desses 300 LEDs 3x3m! Já vem com ganchinhos pra pendurar no varão, controle remoto e liga direto no USB ✨🎄', date: 'Há 1 hora', likes: 118, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_45.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_45.jpg', user: 'ju_decoracoes', text: 'Coloquei a branco quente na sala e ficou igual foto de revista! Recomendo demais 💛', date: 'Há 24 min', likes: 44, liked: false }
            ];
          } else if (contextType === 'vestido139') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Meninas, o tecido suplex desse vestido drapeado é super encorpado, não fica transparente e a faixa lateral deixa a silhueta perfeita pro Réveillon! 🥂✨', date: 'Há 1 hora', likes: 129, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_46.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_46.jpg', user: 'amanda.style', text: 'Peguei o branco pro Ano Novo e o preto pro Natal! Chegou em 4 dias e vestiu perfeito 😍', date: 'Há 19 min', likes: 48, liked: false }
            ];
          } else if (contextType === 'smartwatch135') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Mano, esse Série 10 W99+ Pro tem tela Super AMOLED, NFC pra fechadura, ChatGPT e faz ligação direto no pulso! Por R$ 89,90 no PIX é surreal 🔥⌚',
                date: 'Há 1 hora',
                likes: 142,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_cdn_real/tt_cdn_6.jpg' : 'img/reviews-avatars/tiktok_cdn_real/tt_cdn_6.jpg',
                user: 'lucas.techsp',
                text: 'Peguei o Preto semana passada, conectou de primeira no meu iPhone e a bateria tá durando 4 dias tranquilo!',
                date: 'Há 32 min',
                likes: 64,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_9.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_9.jpg',
                user: 'camila_rocha',
                text: 'Comprei o Rosê pra mim e o Preto pro meu namorado de presente de Natal, chegaram super rápido 😍⌚',
                date: 'Há 14 min',
                likes: 38,
                liked: false
              }
            ];
          } else if (contextType === 'cinta132') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Meninas, os 6 níveis de colchetes dessa cinta M+ seguram muito firme sem enrolar quando senta! O tecido furadinho é super fresquinho 💕✨',
                date: 'Há 1 hora',
                likes: 88,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_3.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_3.jpg',
                user: 'camila.fit22',
                text: 'Peguei a preta e a bege! Uso a bege embaixo de vestido justo e não marca absolutamente nada 😍',
                date: 'Há 35 min',
                likes: 41,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_4.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_4.jpg',
                user: 'fer_oliveira91',
                text: 'Chegou em 4 dias aqui! Compressão maravilhosa e ajuda demais na postura na academia 💪',
                date: 'Há 18 min',
                likes: 29,
                liked: false
              }
            ];
          } else if (contextType === 'pisca133') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Gente, são 9 metros reais com 100 LEDs super brilhantes e fio transparente que some na árvore! Dá pra deixar fixo ou escolher entre os 8 modos 🎄✨',
                date: 'Há 1 hora',
                likes: 112,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_5.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_5.jpg',
                user: 'patricia_decor',
                text: 'Comprei 2 branco quente e 1 colorido pra minha árvore de 1,80m, ficou parecendo árvore de shopping 😍🎄',
                date: 'Há 42 min',
                likes: 54,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_6.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_6.jpg',
                user: 'amanda.costa',
                text: 'O melhor é que não esquenta nada, deixo ligado a noite inteira tranquila com meus cachorros em casa!',
                date: 'Há 20 min',
                likes: 33,
                liked: false
              }
            ];
          } else if (contextType === 'sobrancelha134') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Sério, essa canetinha com LED salva a vida! Limpa a sobrancelha e o buço em 1 minuto sem dor e sem ficar vermelho, e carrega no USB ✨💖',
                date: 'Há 1 hora',
                likes: 104,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_7.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_7.jpg',
                user: 'bia.makeup_',
                text: 'Comprei a Branco Pérola e já tô levando na bolsa! A luzinha LED mostra todos os pelinhos claros 😍',
                date: 'Há 38 min',
                likes: 49,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_8.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_8.jpg',
                user: 'juliana.santos',
                text: 'Chegou com o cabinho USB e a escovinha de limpeza, super prática e não irrita pele sensível!',
                date: 'Há 15 min',
                likes: 27,
                liked: false
              }
            ];
          } else if (contextType === 'bolsa155') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Meninas, vem o kit completinho na caixa: bolsa matelassê, carteira, relógio dourado e pulseira! 👜✨', date: 'Há 24 min', likes: 148, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_41.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_41.jpg', user: 'camila.looks', text: 'Comprei pra dar de presente de Natal e acabei ficando pra mim de tão linda kkkk 😍', date: 'Há 14 min', likes: 74, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_42.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_42.jpg', user: 'patricia_rj', text: 'O acabamento das ferragens douradas é impecável demais!', date: 'Há 6 min', likes: 49, liked: false }
            ];
          } else if (contextType === 'vestidos156') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'São 4 vestidos no mesmo kit e a malha canelada é super grossinha, zero transparência! 👗🔥', date: 'Há 24 min', likes: 162, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_44.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_44.jpg', user: 'ju.modaverao', text: 'Pedi o M e vestiu igual uma luva no corpo, modela muito sem apertar! 🥰', date: 'Há 14 min', likes: 83, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_45.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_45.jpg', user: 'leticia_santos', text: 'Já garanti meus looks pro verão inteiro de uma vez só 👏', date: 'Há 6 min', likes: 57, liked: false }
            ];
          } else if (contextType === 'camisetas157') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Malha 100% algodão fio 30.1 penteado de verdade, gola firme que não esgarça e super fresca! 👕⚡', date: 'Há 24 min', likes: 139, liked: false },
              { avatar: isPagesDir ? '../img/avatars-patinete/creator-lucas-andrade.jpg' : 'img/avatars-patinete/creator-lucas-andrade.jpg', user: 'lucas.treino', text: 'Peguei o kit sortido G e caíram perfeitas no ombro, qualidade de shopping!', date: 'Há 14 min', likes: 68, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_46.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_46.jpg', user: 'mari_esposa', text: 'Comprei pro meu marido trabalhar e já lavei várias vezes sem desbotar nada 👏', date: 'Há 6 min', likes: 44, liked: false }
            ];
          } else if (contextType === 'kitmasc158') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Já vem na caixa rígida executiva com relógio, carteira, cinto e óculos UV400 prontos pra presentear! 🎁⌚', date: 'Há 24 min', likes: 134, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_47.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_47.jpg', user: 'fernanda.presentes', text: 'Dei pro meu marido de presente e ele ficou apaixonado no relógio e no óculos! 😍', date: 'Há 14 min', likes: 71, liked: false },
              { avatar: isPagesDir ? '../img/avatars-patinete/creator-rafael-muniz.jpg' : 'img/avatars-patinete/creator-rafael-muniz.jpg', user: 'rafael_sp', text: 'Muito alinhado, todos os 4 itens combinam perfeitamente!', date: 'Há 6 min', likes: 46, liked: false }
            ];
          } else if (contextType === 'sandalias159') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Vêm os 2 pares de salto bloco super confortáveis + a bolsinha tiracolo coordenada! 👠✨', date: 'Há 24 min', likes: 154, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_48.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_48.jpg', user: 'bia.reveillon', text: 'Peguei Ouro + Prata pro Natal e Réveillon, dancei a festa toda sem cansar o pé! 🥰', date: 'Há 14 min', likes: 79, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_49.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_49.jpg', user: 'carol_festas', text: 'A numeração é certinha, pedi 36 e serviu perfeitamente!', date: 'Há 6 min', likes: 52, liked: false }
            ];
          } else if (contextType === 'jbl146') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Sim! São 100W RMS reais com Bass Boost e o LED sincroniza automático na batida da música 🔊🔥', date: 'Há 32 min', likes: 114, liked: false },
              { avatar: isPagesDir ? '../img/avatars-churras/review-homem-1.jpg' : 'img/avatars-churras/review-homem-1.jpg', user: 'marcelo_churrasco', text: 'Coloquei na área de churrasco aqui em casa e o grave tremeu tudo! Qualidade surreal 👏', date: 'Há 18 min', likes: 58, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_23.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_23.jpg', user: 'camila.festas', text: 'E ainda tem entrada pra microfone atrás pra fazer karaokê com a família no Natal! 😍🎤', date: 'Há 9 min', likes: 37, liked: false }
            ];
          } else if (contextType === 'triciclo147') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Ele gira 360° liso demais, tem 3 níveis de velocidade e toca música pelo Bluetooth do celular! 🛴⚡', date: 'Há 32 min', likes: 128, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_24.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_24.jpg', user: 'paula.maedopedro', text: 'Comprei de presente de Natal pro meu filho e já testei escondido kkkk muito forte e lindo!', date: 'Há 18 min', likes: 64, liked: false },
              { avatar: isPagesDir ? '../img/avatars-churras/creator-rodrigo.jpg' : 'img/avatars-churras/creator-rodrigo.jpg', user: 'rodrigo_condominio', text: 'Os LEDs acesos à noite chamam atenção da rua inteira, bateria dura bastante 👏', date: 'Há 9 min', likes: 41, liked: false }
            ];
          } else if (contextType === 'panelas148') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Meninas, é a linha Brinox Ceramic Life Smart Plus Vanilla de 8 peças! Não gruda nem ovo sem óleo 🍳✨', date: 'Há 32 min', likes: 142, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_25.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_25.jpg', user: 'lar_da_ju', text: 'Essa cor Vanilla deixou meu fogão um luxo! E pra lavar é só passar o lado amarelo da bucha 😍', date: 'Há 18 min', likes: 73, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_26.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_26.jpg', user: 'renata.cozinha', text: 'Os cabos soft-touch realmente não esquentam nada na mão, amei demais!', date: 'Há 9 min', likes: 49, liked: false }
            ];
          } else if (contextType === 'cortina149') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Ela já vem com os 10 ganchinhos prontos pra pendurar direto na cortina e controle remoto sem fio! ✨🎄', date: 'Há 32 min', likes: 135, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_27.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_27.jpg', user: 'bia.decoracao', text: 'Peguei a Branco Quente pra sala pro Natal e ficou parecendo casa de novela! 🥰', date: 'Há 18 min', likes: 69, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_28.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_28.jpg', user: 'fernanda_apto', text: 'Liguei num carregador USB atrás do sofá e não esquenta nadinha o tecido!', date: 'Há 9 min', likes: 42, liked: false }
            ];
          } else if (contextType === 'fogao150') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Acendimento automático super rápido na mesa e no forno, e os pés altos facilitam muito varrer embaixo! 🔥🍲', date: 'Há 32 min', likes: 96, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_29.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_29.jpg', user: 'dona.helena', text: 'A chama maior ferve a panela de pressão rapidinho! Excelente fogão Esmaltec 👏', date: 'Há 18 min', likes: 47, liked: false },
              { avatar: isPagesDir ? '../img/avatars-churras/review-homem-3.jpg' : 'img/avatars-churras/review-homem-3.jpg', user: 'carlos_familia', text: 'Chegou inteirinho sem nenhum amassado, forno limpa fácil funciona muito bem!', date: 'Há 9 min', likes: 31, liked: false }
            ];
          } else if (contextType === 'tv151') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'O sistema webOS da LG é muito rápido, já vem Netflix, Globoplay, YouTube e pega fone Bluetooth! 📺✨', date: 'Há 32 min', likes: 118, liked: false },
              { avatar: isPagesDir ? '../img/avatars-tv/creator-matheus.jpg' : 'img/avatars-tv/creator-matheus.jpg', user: 'lucas.quarto', text: 'Coloquei no suporte do quarto e ficou perfeita, imagem super viva com HDR!', date: 'Há 18 min', likes: 55, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_30.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_30.jpg', user: 'mariana_series', text: 'Espelho a tela do meu celular direto nela com um clique, amei demais 😍', date: 'Há 9 min', likes: 38, liked: false }
            ];
          } else if (contextType === 'galaxy152') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Tela Super AMOLED de 6,7 polegadas 90Hz, 128GB, 5G e NFC pra pagar aproximando na maquininha! 📱⚡', date: 'Há 32 min', likes: 131, liked: false },
              { avatar: isPagesDir ? '../img/avatars-churras/creator-marcos.jpg' : 'img/avatars-churras/creator-marcos.jpg', user: 'andre.silva', text: 'Comprei pro dia a dia e a bateria de 5000mAh sobra no fim da noite! Câmera ótima 👏', date: 'Há 18 min', likes: 62, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_32.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_32.jpg', user: 'juliana_sp', text: 'Chegou lacrado rapidinho, muito fino e bonito pessoalmente!', date: 'Há 9 min', likes: 44, liked: false }
            ];
          } else if (contextType === 'tabs10_153') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Sim! Já vem na caixa tanto a caneta S-Pen original quanto a capa magnética protetora! ✍️📚', date: 'Há 32 min', likes: 156, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_33.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_33.jpg', user: 'med.carol', text: 'Aposentei todos os cadernos da faculdade, escrever com a S-Pen no Samsung Notes é perfeito 😍', date: 'Há 18 min', likes: 81, liked: false },
              { avatar: isPagesDir ? '../img/avatars-patinete/creator-gabriel-souza.jpg' : 'img/avatars-patinete/creator-gabriel-souza.jpg', user: 'vitor_concursos', text: '8GB de RAM divide a tela com videoaula e PDF liso sem travar nada!', date: 'Há 9 min', likes: 52, liked: false }
            ];
          } else if (contextType === 'brastemp154') {
            return [
              { avatar: originalItem.avatar, user: originalItem.username, isCreator: true, text: 'Cesto 100% inox de 13kg que cabe até edredom e o ciclo Tira-Manchas tira sujeira pesada sozinho! 🫧👕', date: 'Há 32 min', likes: 124, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_34.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_34.jpg', user: 'paty.lavanderia', text: 'Silenciosa demais centrifugando! Brastemp é outro nível de durabilidade 👏', date: 'Há 18 min', likes: 66, liked: false },
              { avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_35.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_35.jpg', user: 'claudia_mae3', text: 'O ciclo antibolinhas salvou todas as camisetas aqui de casa, recomendo de olhos fechados!', date: 'Há 9 min', likes: 45, liked: false }
            ];
          } else if (contextType === 'camera144') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Gente, não usa tinta nenhuma! É impressão térmica instantânea e já vem com 3 bobinas na caixa pras crianças saírem fotografando tudo 📸✨',
                date: 'Há 35 min',
                likes: 94,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_14.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_14.jpg',
                user: 'camila_maedabela',
                text: 'Comprei a Rosa Gatinho pra minha filha de 6 anos e ela largou o tablet na hora! Imprime super rápido 😍',
                date: 'Há 20 min',
                likes: 51,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_15.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_15.jpg',
                user: 'paty.rodrigues',
                text: 'E ainda dá pras crianças pintarem as fotinhos impressas com canetinha! Melhor presente de Natal 👏🩷',
                date: 'Há 12 min',
                likes: 33,
                liked: false
              }
            ];
          } else if (contextType === 'drift127') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Galera, é só pingar água limpa com a bisnaguinha que vem na caixa e apertar o botão no controle que sai a fumaça iluminada! 🏎️💨',
                date: 'Há 40 min',
                likes: 108,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-churras/creator-lucas.jpg' : 'img/avatars-churras/creator-lucas.jpg',
                user: 'thiago_garage',
                text: 'Comprei pro meu filho mas quem mais brinca sou eu kkkk! Com os pneus lisos faz drift perfeito no piso!',
                date: 'Há 22 min',
                likes: 63,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_16.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_16.jpg',
                user: 'renata.maedoleo',
                text: 'Chegou super rápido com os 4 cones e os pneus extras. Os LEDs no escuro ficam lindos demais 🔥',
                date: 'Há 14 min',
                likes: 39,
                liked: false
              }
            ];
          } else if (contextType === 'escova129') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Meninas, o cabo alonga até 1,37m! Dá pra lavar o box inteiro, o rejunte do piso e até o alto do azulejo sem dobrar a coluna 🫧✨',
                date: 'Há 45 min',
                likes: 119,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_18.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_18.jpg',
                user: 'casa.da.lu',
                text: 'A ponteira fininha tirou todo o encardido dos cantos do banheiro em 2 minutos! Amei demais 👏',
                date: 'Há 28 min',
                likes: 57,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_19.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_19.jpg',
                user: 'marcia_organiza',
                text: 'Bateria dura a faxina inteira e carrega no mesmo cabo USB-C do celular. Praticidade pura!',
                date: 'Há 15 min',
                likes: 34,
                liked: false
              }
            ];
          } else if (contextType === 'mala145') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Sim! Ela tem as medidas exatas da ANAC pra levar até 10kg dentro do avião sem pagar despacho, e a frasqueira prende no puxador ✈️🧳',
                date: 'Há 50 min',
                likes: 102,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_20.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_20.jpg',
                user: 'bia.viaja',
                text: 'Peguei a Branco Off-White e pessoalmente é um luxo! As rodinhas 360 giram super macio 😍',
                date: 'Há 30 min',
                likes: 48,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_21.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_21.jpg',
                user: 'fernanda.costa',
                text: 'Chegou uma dentro da outra super bem embalada, o cadeado de senha embutido dá muita segurança!',
                date: 'Há 16 min',
                likes: 29,
                liked: false
              }
            ];
          } else if (contextType === 'mesa128') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Cabe de 6 a 8 pessoas sentadas tranquilamente! As travas de aço embaixo deixam ela super firme pra ceia e pro churrasco 🍽️✨',
                date: 'Há 55 min',
                likes: 87,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-churras/review-homem-1.jpg' : 'img/avatars-churras/review-homem-1.jpg',
                user: 'marcelo_churras',
                text: 'Comprei já pensando na ceia de Natal aqui em casa! Fechada vira maleta fininha e guardo atrás do guarda-roupa 👏',
                date: 'Há 32 min',
                likes: 44,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_22.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_22.jpg',
                user: 'kelly.familia',
                text: 'Material bem grosso e fácil de limpar, nem precisa de toalha se não quiser. Nota 10!',
                date: 'Há 19 min',
                likes: 28,
                liked: false
              }
            ];
          } else if (contextType === 'patinete126') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Gente, o patinete já vem pré-montado na caixa com carregador bivolt! As 3 rodas dão muita segurança pros pequenos e os LEDs acendem forte demais 🛴✨',
                date: 'Há 1 hora',
                likes: 93,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_1.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_1.jpg',
                user: 'ju_maedodavi',
                text: 'Comprei o Azul Turbo pro meu filho de 6 anos e ele não desce mais! A bateria dura o passeio inteiro na praça 💙',
                date: 'Há 40 min',
                likes: 47,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_2.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_2.jpg',
                user: 'carol.almeida88',
                text: 'Dobra mesmo pra caber no porta-malas? Quero levar na viagem de fim de ano!',
                date: 'Há 2 horas',
                likes: 19,
                liked: false
              },
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Dobra sim amiga! Destrava na base em 3 segundos e pesa só 4,5 kg, cabe em qualquer cantinho do porta-malas 🥰',
                date: 'Há 2 horas',
                likes: 64,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_3.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_3.jpg',
                user: 'patricia_melo',
                text: 'Por esse valor no Pix tá dado demais, no shopping vi igualzinho por quase 400 reais! Já garanti o de Natal da minha afilhada 🎄🎁',
                date: 'Há 4 horas',
                likes: 52,
                liked: false
              }
            ];
          } else if (contextType === 'arcade114') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Galera, recomendo fixar bem as 4 ventosas numa mesa de vidro ou madeira lisa! O manche 360 fica super firme e os combos saem perfeitos! 🕹️🔥',
                date: 'Há 1 hora',
                likes: 84,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_1.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_1.jpg',
                user: 'lucas_retrogamer',
                text: 'Mano, o clique dos microswitches é satisfatório demais! Zero delay no PS4 e no PC.',
                date: 'Há 45 min',
                likes: 42,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_3.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_3.jpg',
                user: 'thiago_kof',
                text: 'Testei no KOF 98 e no Street Fighter 6, os especiais e hadouken saem limpos sem engasgar!',
                date: 'Há 2 horas',
                likes: 31,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_5.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_5.jpg',
                user: 'marcos_arcade',
                text: 'Reconheceu no PC de primeira como X-Input sem instalar nenhum driver. Excelente custo-benefício!',
                date: 'Há 3 horas',
                likes: 27,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_7.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_7.jpg',
                user: 'felipe_gamers',
                text: 'Cabo USB de 2.5m bem reforçado, dá pra jogar do sofá com folga no Nintendo Switch.',
                date: 'Ontem',
                likes: 19,
                liked: false
              }
            ];
          } else {
            return [
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_1.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_1.jpg',
                user: 'mariasilva.ofc',
                text: 'Menina do céu, o meu chegou ontem e é simplesmente PERFEITO!',
                date: 'Há 2 horas',
                likes: 14,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_2.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_2.jpg',
                user: 'carol_looks',
                text: 'Super fácil de usar, amei o resultado 😍',
                date: 'Há 5 horas',
                likes: 8,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_3.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_3.jpg',
                user: 'amanda.santoss',
                text: 'Chegou rápido demais aqui em SP! Nota 10',
                date: 'Ontem',
                likes: 5,
                liked: false
              }
            ];
          }
        })()
      };
      videoList.push(item);
    }

    // Se já existirem cards pré-renderizados no HTML estático (Zero Delay):
    const existingList = document.getElementById('creators-carousel-list');
    const existingCards = existingList ? existingList.querySelectorAll('.creator-card') : [];

    if (!existingCards.length) {
      // Se a página não tiver pré-render estático, gera agora dinamicamente
      targetContainer.innerHTML = `
        <h3 class="creators-title">Vídeos de criadores (${countBadge})</h3>
        <div class="creators-carousel" id="creators-carousel-list"></div>
      `;

      const listElement = document.getElementById('creators-carousel-list');
      for (let i = 0; i < totalVideosCount; i++) {
        const item = videoList[i];
        const avatarLoading = i < 4 ? 'eager' : 'lazy';
        const cardHtml = `
          <div class="creator-card" data-video-id="${i}">
            <video class="creator-preview-vid" data-src="${item.video}" poster="${item.poster}" muted loop playsinline webkit-playsinline preload="none" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0; pointer-events: none;"></video>
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.15) 0%, transparent 40%, rgba(0,0,0,0.75) 100%); pointer-events: none;"></div>
            <div style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2; pointer-events: none;">
              <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
            </div>
            <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 6px; display: flex; align-items: center; gap: 5px; z-index: 2; box-sizing: border-box; pointer-events: none;">
              <img src="${item.avatar}" alt="" loading="${avatarLoading}" decoding="async" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;" onerror="this.src='../img/creators-avatars/creator-1.jpg'">
              <span style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">${item.name}</span>
            </div>
          </div>
        `;
        listElement.insertAdjacentHTML('beforeend', cardHtml);
      }
    }

    // Vincula o clique nos cards com PREVENÇÃO DE CLIQUE DUPLO e PLAY IMEDIATO
    const allCards = targetContainer.querySelectorAll('.creator-card');
    allCards.forEach((card, idx) => {
      card.onclick = function(e) {
        if (e) {
          e.preventDefault();
          e.stopPropagation();
        }
        const id = parseInt(this.getAttribute('data-video-id') !== null ? this.getAttribute('data-video-id') : idx, 10);
        const cardImg = this.querySelector('img');
        const cardVid = this.querySelector('video');
        const cardName = this.querySelector('span');
        if (videoList[id]) {
          if (cardImg && cardImg.getAttribute('src')) videoList[id].avatar = cardImg.getAttribute('src');
          if (cardVid && (cardVid.dataset.src || cardVid.getAttribute('src'))) {
            videoList[id].video = cardVid.dataset.src || cardVid.getAttribute('src');
          }
          if (cardName && cardName.textContent.trim()) videoList[id].name = cardName.textContent.trim();
        }
        openTikTokVideo(id);
      };
    });

    // Inicializa o modal em background para deixá-lo quente na memória (sem baixar vídeo até clicar)
    createTikTokModalMarkup();

    function hydrateAndPlayPreview(v) {
      if (!v) return;
      if (!v.getAttribute('src') && v.dataset.src) {
        v.preload = 'metadata';
        v.src = v.dataset.src;
      }
      v.muted = true;
      const p = v.play();
      if (p !== undefined) p.catch(() => {});
    }

    // Hidrata vídeos SOMENTE quando a seção de criadores entra perto da tela e após o carregamento crítico das imagens
    function bindLazyCreatorPreviews() {
      if ('IntersectionObserver' in window) {
        const vidObserver = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            const v = entry.target.querySelector('video.creator-preview-vid');
            if (!v) return;
            if (entry.isIntersecting) {
              hydrateAndPlayPreview(v);
            } else if (v.getAttribute('src')) {
              v.pause();
            }
          });
        }, { rootMargin: '180px 100px', threshold: 0.05 });

        allCards.forEach(card => vidObserver.observe(card));
      } else {
        allCards.forEach((card, idx) => {
          if (idx < 2) {
            hydrateAndPlayPreview(card.querySelector('video.creator-preview-vid'));
          }
        });
      }
    }

    if (document.readyState === 'complete') {
      setTimeout(bindLazyCreatorPreviews, 120);
    } else {
      window.addEventListener('load', () => setTimeout(bindLazyCreatorPreviews, 120), { once: true });
    }

  }

  // Cria ou vincula o Modal TikTok
  function createTikTokModalMarkup() {
    if (document.getElementById('tiktok-modal')) {
      ttModal = document.getElementById('tiktok-modal');
      ttVideo = document.getElementById('tt-modal-player');
      setupModalEventListeners();
      return;
    }

    ttModal = document.createElement('div');
    ttModal.className = 'tt-modal';
    ttModal.id = 'tiktok-modal';

    const initialAvatar = (videoList[0] && videoList[0].avatar) ? videoList[0].avatar : '';
    ttModal.innerHTML = `
      <div class="tt-container">
        <div class="tt-top-bar">
          <button class="tt-back-btn" id="tt-close-btn" type="button" aria-label="Voltar">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#ffffff" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">
              <line x1="19" y1="12" x2="5" y2="12"></line>
              <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
          </button>
        </div>

        <div class="tt-video-wrapper" id="tt-video-wrapper">
          <video class="tt-video" id="tt-modal-player" loop playsinline webkit-playsinline preload="none" style="background:#000;"></video>

          <div class="tt-play-icon-overlay" id="tt-play-overlay">
            <svg viewBox="0 0 24 24" width="34" height="34" fill="#fff"><path d="M8 5v14l11-7z"/></svg>
          </div>

          <div class="tt-right-actions">
            <div class="tt-creator-wrapper">
              <img class="tt-creator-avatar" id="tt-action-avatar" src="${initialAvatar}" alt="">
              <button class="tt-follow-btn" id="tt-action-follow" type="button" aria-label="Seguir">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              </button>
            </div>
            <button class="tt-action-btn" id="tt-action-like" type="button">
              <svg viewBox="0 0 24 24" width="34" height="34" fill="#ffffff"><path d="M16.5 3.2C14.6 3.2 12.95 4.18 12 5.66C11.05 4.18 9.4 3.2 7.5 3.2C4.42 3.2 2 5.68 2 8.82C2 13.15 6.45 16.82 10.78 20.42C11.49 21.01 12.51 21.01 13.22 20.42C17.55 16.82 22 13.15 22 8.82C22 5.68 19.58 3.2 16.5 3.2Z"/></svg>
              <span class="tt-action-label" id="tt-like-count">5.089</span>
            </button>
            <button class="tt-action-btn" id="tt-action-comment" type="button">
              <svg viewBox="0 0 24 24" width="32" height="32" fill="#ffffff" fill-rule="evenodd" clip-rule="evenodd"><path d="M12 2.5C6.48 2.5 2 6.42 2 11.25C2 13.78 3.23 16.06 5.2 17.66L4.38 20.72C4.24 21.24 4.76 21.69 5.25 21.46L8.78 19.8C9.8 20.06 10.88 20.2 12 20.2C17.52 20.2 22 16.28 22 11.35C22 6.42 17.52 2.5 12 2.5ZM8.1 12.6C7.33 12.6 6.7 11.97 6.7 11.2C6.7 10.43 7.33 9.8 8.1 9.8C8.87 9.8 9.5 10.43 9.5 11.2C9.5 11.97 8.87 12.6 8.1 12.6ZM12 12.6C11.23 12.6 10.6 11.97 10.6 11.2C10.6 10.43 11.23 9.8 12 9.8C12.77 9.8 13.4 10.43 13.4 11.2C13.4 11.97 12.77 12.6 12 12.6ZM15.9 12.6C15.13 12.6 14.5 11.97 14.5 11.2C14.5 10.43 15.13 9.8 15.9 9.8C16.67 9.8 17.3 10.43 17.3 11.2C17.3 11.97 16.67 12.6 15.9 12.6Z"/></svg>
              <span class="tt-action-label" id="tt-comment-count">94</span>
            </button>
            <button class="tt-action-btn" id="tt-action-save" type="button">
              <svg viewBox="0 0 24 24" width="30" height="30" fill="#ffffff"><path d="M6.5 3C5.4 3 4.5 3.9 4.5 5V19.95C4.5 20.78 5.42 21.27 6.11 20.81L12 16.88L17.89 20.81C18.58 21.27 19.5 20.78 19.5 19.95V5C19.5 3.9 18.6 3 17.5 3H6.5Z"/></svg>
              <span class="tt-action-label" id="tt-save-count">695</span>
            </button>
            <button class="tt-action-btn" id="tt-action-share" type="button">
              <svg viewBox="0 0 24 24" width="32" height="32" fill="#ffffff"><path d="M13.6 4.25C13.6 3.42 14.58 2.98 15.2 3.53L21.65 9.28C22.12 9.7 22.12 10.44 21.65 10.86L15.2 16.61C14.58 17.16 13.6 16.72 13.6 15.89V12.75C8.55 12.75 4.95 14.48 2.82 18.28C2.48 18.88 1.6 18.55 1.72 17.86C2.65 11.25 6.82 6.85 13.6 6.55V4.25Z"/></svg>
              <span class="tt-action-label" id="tt-share-count">753</span>
            </button>
            <div class="tt-music-disc" id="tt-music-disc">
              <img id="tt-music-avatar" src="${initialAvatar}" alt="">
            </div>
          </div>

          <div class="tt-left-info">
            <div class="tt-product-anchor" id="tt-product-anchor">
              <div class="tt-anchor-cart-badge">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#ffffff" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 4h2.2l1.9 9.5a1.5 1.5 0 0 0 1.48 1.2h7.9a1.5 1.5 0 0 0 1.46-1.15L19.8 6.8H6.1"></path>
                  <circle cx="9.2" cy="18.6" r="1.4" fill="#ffffff" stroke="none"></circle>
                  <circle cx="16.4" cy="18.6" r="1.4" fill="#ffffff" stroke="none"></circle>
                </svg>
              </div>
              <div class="tt-anchor-lines">
                <div class="tt-anchor-line1"><span class="tt-anchor-title" id="tt-anchor-title">Loja - Produto Oficial</span></div>
                <div class="tt-anchor-line2">Frete grátis · Devoluções gratuitas</div>
              </div>
            </div>
            <div class="tt-username-row">
              <div class="tt-username" id="tt-display-name">Criador</div>
              <span class="tt-post-date" id="tt-display-date">· 11-18</span>
            </div>
            <div class="tt-desc" id="tt-display-desc"></div>
            <div class="tt-music-row">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="#ffffff" style="flex-shrink:0;">
                <path d="M19 3v11.5a3.5 3.5 0 1 1-2-3.16V6.4l-8 1.8v8.3a3.5 3.5 0 1 1-2-3.16V6.6L19 3z"></path>
              </svg>
              <span class="tt-music-text" id="tt-display-music">som original - criador ...</span>
            </div>
          </div>

          </div>
        </div>

        <div class="tt-comments-drawer" id="tt-comments-drawer">
          <div class="tt-drawer-shop-bar">
            <div class="tt-drawer-shop-left" id="tt-drawer-shop-link">
              <div class="tt-drawer-shop-cart">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#ffffff" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 4h2.2l1.9 9.5a1.5 1.5 0 0 0 1.48 1.2h7.9a1.5 1.5 0 0 0 1.46-1.15L19.8 6.8H6.1"></path>
                  <circle cx="9.2" cy="18.6" r="1.4" fill="#ffffff" stroke="none"></circle>
                  <circle cx="16.4" cy="18.6" r="1.4" fill="#ffffff" stroke="none"></circle>
                </svg>
              </div>
              <div class="tt-drawer-shop-texts">
                <span class="tt-drawer-shop-name" id="tt-drawer-shop-name">Shop·Produto Oficial</span>
                <span class="tt-drawer-shop-sold" id="tt-drawer-shop-sold">3842 vendidos</span>
              </div>
            </div>
            <button class="tt-drawer-close" id="tt-drawer-close" type="button" aria-label="Fechar comentários">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
          </div>
          <div class="tt-drawer-count-row">
            <span class="tt-drawer-title" id="tt-drawer-title">94 comentários</span>
            <svg viewBox="0 0 14 14" width="12" height="12" fill="none" stroke="#161823" stroke-width="1.5" stroke-linecap="round">
              <line x1="1.5" y1="3.5" x2="12.5" y2="3.5"></line>
              <line x1="1.5" y1="7" x2="9.5" y2="7"></line>
              <line x1="1.5" y1="10.5" x2="6.2" y2="10.5"></line>
            </svg>
          </div>
          <div class="tt-drawer-list" id="tt-drawer-comments-list"></div>
          <div class="tt-comment-input-bar">
            <div class="tt-comment-input-pill-wrap">
              <input type="text" class="tt-comment-input" id="tt-comment-input-field" placeholder="Adicionar comentário...">
              <div class="tt-drawer-pill-icons">
                <svg onclick="document.getElementById('tt-comment-input-field')?.focus()" style="cursor:pointer;" viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3.5" y="3.5" width="17" height="17" rx="3"></rect>
                  <circle cx="15.5" cy="9" r="1.4" fill="currentColor" stroke="none"></circle>
                  <path d="M20.5 16.5L15.2 12L5.5 20.2"></path>
                </svg>
                <svg onclick="document.getElementById('tt-comment-input-field')?.focus()" style="cursor:pointer;" viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20.5 12A8.5 8.5 0 1 0 12 20.5C14.2 20.5 15.8 20.1 17.2 18.8L19.3 16.7C20.2 15.6 20.5 14 20.5 12Z"></path>
                  <path d="M14.8 20.1V16.6C14.8 15.6 15.6 14.8 16.6 14.8H20.1"></path>
                  <circle cx="9.2" cy="10" r="1.15" fill="currentColor" stroke="none"></circle>
                  <circle cx="14.8" cy="10" r="1.15" fill="currentColor" stroke="none"></circle>
                </svg>
                <svg onclick="document.getElementById('tt-comment-input-field')?.focus()" style="cursor:pointer;" viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="9" y="3" width="6" height="11" rx="3"></rect>
                  <path d="M5.5 11a6.5 6.5 0 0 0 13 0"></path>
                  <line x1="12" y1="17.5" x2="12" y2="21"></line>
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div class="tt-bottom-bar-comment" id="tt-bottom-bar-comment">
          <div class="tt-bottom-comment-pill" id="tt-open-comment-pill">
            <span class="tt-bottom-comment-placeholder">Adicionar comentário...</span>
            <div class="tt-bottom-comment-icons">
              <svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3.5" y="3.5" width="17" height="17" rx="3"></rect>
                <circle cx="8.8" cy="8.8" r="1.4" fill="currentColor" stroke="none"></circle>
                <path d="M20.5 15.8L16.2 11.6L7.5 20.5"></path>
              </svg>
              <svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20.5 12A8.5 8.5 0 1 0 12 20.5C14.2 20.5 15.8 20.1 17.2 18.8L19.3 16.7C20.2 15.6 20.5 14 20.5 12Z"></path>
                <path d="M14.8 20.1V16.6C14.8 15.6 15.6 14.8 16.6 14.8H20.1"></path>
                <circle cx="9.2" cy="10" r="1.1" fill="currentColor" stroke="none"></circle>
                <circle cx="14.8" cy="10" r="1.1" fill="currentColor" stroke="none"></circle>
                <path d="M8.8 14.2C9.6 15.1 10.7 15.5 12 15.5C12.8 15.5 13.5 15.3 14.1 14.9"></path>
              </svg>
              <svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round">
                <rect x="9" y="3" width="6" height="11" rx="3"></rect>
                <path d="M5.5 11a6.5 6.5 0 0 0 13 0"></path>
                <line x1="12" y1="17.5" x2="12" y2="21"></line>
                <line x1="9" y1="21" x2="15" y2="21"></line>
              </svg>
            </div>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(ttModal);
    ttVideo = document.getElementById('tt-modal-player');
    setupModalEventListeners();
  }

  // Alterna Play / Pause e Mute com Atualização de Ícones
  function updateSoundBadge() {
    const badge = document.getElementById('tt-sound-badge');
    if (!badge) return;
    if (ttVideo && ttVideo.muted) {
      badge.style.display = 'flex';
    } else {
      badge.style.display = 'none';
    }
  }

  function togglePlayPause() {
    if (!ttVideo) return;
    const playOverlay = document.getElementById('tt-play-overlay');

    // Se estiver tocando muted e o usuário tocar na tela, ativa o som primeiro!
    if (!ttVideo.paused && ttVideo.muted) {
      ttVideo.muted = false;
      updateSoundBadge();
      showTikTokToast('Som ativado 🔊');
      return;
    }

    if (ttVideo.paused) {
      const p = ttVideo.play();
      if (p !== undefined) {
        p.then(() => {
          if (playOverlay) playOverlay.style.display = 'none';
          updateSoundBadge();
        }).catch(() => {
          ttVideo.muted = true;
          ttVideo.play().then(() => {
            if (playOverlay) playOverlay.style.display = 'none';
            updateSoundBadge();
          }).catch(() => {
            if (playOverlay) playOverlay.style.display = 'flex';
          });
        });
      }
    } else {
      ttVideo.pause();
      if (playOverlay) playOverlay.style.display = 'flex';
    }
  }

  // Configura todos os eventos de clique, toque e swipe do Modal
  function setupModalEventListeners() {
    if (!ttModal || ttModal.getAttribute('data-events-bound') === 'true') return;
    ttModal.setAttribute('data-events-bound', 'true');

    const closeBtn = document.getElementById('tt-close-btn');
    if (closeBtn) closeBtn.onclick = closeTikTokModal;

    const soundBadge = document.getElementById('tt-sound-badge');
    if (soundBadge) {
      soundBadge.onclick = function(e) {
        e.stopPropagation();
        if (ttVideo) {
          ttVideo.muted = false;
          updateSoundBadge();
          showTikTokToast('Som ativado 🔊');
        }
      };
    }

    function openCommentsDrawer() {
      const drw = document.getElementById('tt-comments-drawer');
      if (drw) drw.classList.add('open');
      if (ttModal) ttModal.classList.add('comments-open');
    }

    function closeCommentsDrawer() {
      const drw = document.getElementById('tt-comments-drawer');
      if (drw) drw.classList.remove('open');
      if (ttModal) ttModal.classList.remove('comments-open');
    }

    const drawerClose = document.getElementById('tt-drawer-close');
    if (drawerClose) drawerClose.onclick = (e) => {
      e.stopPropagation();
      closeCommentsDrawer();
    };

    const actionComment = document.getElementById('tt-action-comment');
    if (actionComment) actionComment.onclick = (e) => {
      e.stopPropagation();
      const drw = document.getElementById('tt-comments-drawer');
      if (drw && drw.classList.contains('open')) closeCommentsDrawer();
      else openCommentsDrawer();
    };

    const bottomCommentPill = document.getElementById('tt-open-comment-pill');
    if (bottomCommentPill) bottomCommentPill.onclick = (e) => {
      e.stopPropagation();
      openCommentsDrawer();
      setTimeout(() => {
        const inp = document.getElementById('tt-comment-input-field');
        if (inp) inp.focus();
      }, 220);
    };

    const descBox = document.getElementById('tt-display-desc');
    if (descBox) descBox.onclick = (e) => {
      e.stopPropagation();
      descBox.classList.toggle('is-expanded');
    };

    // Teclado
    document.addEventListener('keydown', e => {
      if (!ttModal || ttModal.style.display !== 'flex') return;
      if (e.key === 'ArrowDown' || e.key === 'PageDown') nextTikTokVideo();
      if (e.key === 'ArrowUp' || e.key === 'PageUp') prevTikTokVideo();
      if (e.key === 'Escape') closeTikTokModal();
      if (e.key === ' ') {
        e.preventDefault();
        togglePlayPause();
      }
    });

    const wrapper = ttModal.querySelector('.tt-video-wrapper');
    const playOverlay = document.getElementById('tt-play-overlay');

    let touchStartY = 0;
    let touchStartX = 0;
    let touchCurrentY = 0;
    let touchStartTime = 0;
    let isTracking = false;
    let isVerticalSwipe = false;

    function handleStart(clientY, clientX, target) {
      if (isTransitioning) return;
      if (target.closest('#tt-comments-drawer') || 
          target.closest('#tt-bottom-bar-comment') ||
          target.closest('#tt-product-anchor') ||
          target.closest('.tt-right-actions') || 
          target.closest('.tt-top-bar') ||
          target.closest('#tt-sound-badge') ||
          target.closest('.tt-drawer-close')) {
        return;
      }
      touchStartY = clientY;
      touchStartX = clientX;
      touchCurrentY = clientY;
      touchStartTime = Date.now();
      isTracking = true;
      isVerticalSwipe = false;
      if (wrapper) wrapper.style.transition = 'none';
    }

    function handleMove(clientY, clientX, e) {
      if (!isTracking || isTransitioning) return;
      if (ttModal && ttModal.classList.contains('comments-open')) return;
      const deltaY = clientY - touchStartY;
      const deltaX = clientX - touchStartX;

      if (!isVerticalSwipe) {
        if (Math.abs(deltaY) > 25 && Math.abs(deltaY) > Math.abs(deltaX)) {
          isVerticalSwipe = true;
        } else if (Math.abs(deltaX) > 20) {
          isTracking = false;
          return;
        }
      }

      if (isVerticalSwipe) {
        if (e && e.cancelable) e.preventDefault();
        touchCurrentY = clientY;
        if (wrapper) wrapper.style.transform = `translateY(${deltaY * 0.7}px)`;
      }
    }

    function handleEnd() {
      if (!isTracking) return;
      isTracking = false;
      if (ttModal && ttModal.classList.contains('comments-open')) {
        closeCommentsDrawer();
        return;
      }

      const deltaY = touchCurrentY - touchStartY;
      const deltaTime = Date.now() - touchStartTime;
      const velocity = Math.abs(deltaY) / (deltaTime || 1);

      // TOQUE RÁPIDO (TAP): Menos de 20px de movimento e menos de 450ms -> TOGGLE PLAY / PAUSE / UNMUTE!
      if (!isVerticalSwipe && Math.abs(deltaY) < 20 && deltaTime < 450) {
        if (wrapper) wrapper.style.transform = '';
        togglePlayPause();
        return;
      }

      // Se passou o dedo para cima ou para baixo:
      if (Math.abs(deltaY) > 35 || (Math.abs(deltaY) > 20 && velocity > 0.3)) {
        if (deltaY < 0) {
          nextTikTokVideo();
        } else {
          prevTikTokVideo();
        }
      } else {
        if (wrapper) {
          wrapper.style.transition = 'transform 0.2s cubic-bezier(0.25, 1, 0.5, 1)';
          wrapper.style.transform = 'translateY(0)';
          setTimeout(() => {
            if (wrapper) {
              wrapper.style.transition = '';
              wrapper.style.transform = '';
            }
          }, 200);
        }
      }
    }

    // Touch events (Mobile)
    ttModal.addEventListener('touchstart', e => {
      if (e.touches && e.touches.length > 0) {
        handleStart(e.touches[0].clientY, e.touches[0].clientX, e.target);
      }
    }, { passive: true });

    ttModal.addEventListener('touchmove', e => {
      if (e.touches && e.touches.length > 0) {
        handleMove(e.touches[0].clientY, e.touches[0].clientX, e);
      }
    }, { passive: false });

    ttModal.addEventListener('touchend', () => { handleEnd(); }, { passive: true });
    ttModal.addEventListener('touchcancel', () => { handleEnd(); }, { passive: true });

    // Desktop Click no wrapper para dar play/pause (ou fechar gaveta de comentários se estiver aberta)
    if (wrapper) {
      wrapper.onclick = function(e) {
        if (ttModal && ttModal.classList.contains('comments-open')) {
          const drw = document.getElementById('tt-comments-drawer');
          if (drw) drw.classList.remove('open');
          ttModal.classList.remove('comments-open');
          return;
        }
        if (e.target.closest('#tt-comments-drawer') || 
            e.target.closest('#tt-bottom-bar-comment') ||
            e.target.closest('#tt-product-anchor') ||
            e.target.closest('.tt-right-actions') || 
            e.target.closest('.tt-top-bar') ||
            e.target.closest('#tt-sound-badge') ||
            e.target.closest('.tt-drawer-close')) {
          return;
        }
        togglePlayPause();
      };
    }

    if (playOverlay) {
      playOverlay.onclick = function(e) {
        e.stopPropagation();
        togglePlayPause();
      };
    }

    // Ações laterais (Likes, Seguir, Favoritar, Compartilhar)
    const likeBtn = document.getElementById('tt-action-like');
    if (likeBtn) likeBtn.onclick = function(e) {
      e.stopPropagation();
      const item = videoList[currentVideoIndex];
      if (!item) return;
      item.liked = !item.liked;
      this.querySelector('svg').style.fill = item.liked ? '#f7355a' : '#ffffff';
      item.likes += item.liked ? 1 : -1;
      document.getElementById('tt-like-count').textContent = formatNumber(item.likes);
    };

    const followBtn = document.getElementById('tt-action-follow');
    if (followBtn) followBtn.onclick = function(e) {
      e.stopPropagation();
      const item = videoList[currentVideoIndex];
      if (!item) return;
      item.followed = !item.followed;
      this.innerHTML = item.followed
        ? '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>'
        : '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>';
      this.style.background = item.followed ? '#25D366' : '#f7355a';
    };

    const saveBtn = document.getElementById('tt-action-save');
    if (saveBtn) saveBtn.onclick = function(e) {
      e.stopPropagation();
      const item = videoList[currentVideoIndex];
      if (!item) return;
      item.saved = !item.saved;
      this.querySelector('svg').style.fill = item.saved ? '#face15' : '#fff';
      item.saves += item.saved ? 1 : -1;
      document.getElementById('tt-save-count').textContent = formatNumber(item.saves);
      showTikTokToast(item.saved ? 'Salvo nos favoritos' : 'Removido dos favoritos');
    };

    const shareBtn = document.getElementById('tt-action-share');
    if (shareBtn) shareBtn.onclick = function(e) {
      e.stopPropagation();
      if (navigator.share) {
        navigator.share({
          title: document.title,
          url: window.location.href
        }).catch(() => {});
      } else {
        showTikTokToast('Link copiado!');
      }
    };

    const commentSend = document.getElementById('tt-comment-send-btn');
    if (commentSend) commentSend.onclick = handleSendComment;
    const commentInput = document.getElementById('tt-comment-input-field');
    if (commentInput) commentInput.onkeydown = e => {
      if (e.key === 'Enter') {
        e.preventDefault();
        handleSendComment();
      }
    };
  }

  // Envio de comentário simulado
  function handleSendComment() {
    const input = document.getElementById('tt-comment-input-field');
    if (!input) return;
    const val = input.value.trim();
    if (!val) return;
    input.value = '';
    input.blur();
    showTikTokToast('Comentário enviado para análise');
  }

  function showTikTokToast(msg) {
    let toast = document.getElementById('tt-toast-feedback');
    if (!toast && ttModal) {
      toast = document.createElement('div');
      toast.id = 'tt-toast-feedback';
      toast.className = 'tt-toast';
      const container = ttModal.querySelector('.tt-container');
      if (container) container.appendChild(toast);
    }
    if (toast) {
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => { toast.classList.remove('show'); }, 2300);
    }
  }

  // Abre o Modal e Toca o Vídeo Imediatamente
  function openTikTokVideo(id) {
    currentVideoIndex = id;
    const item = videoList[id];
    if (!item) return;

    if (!ttModal) {
      createTikTokModalMarkup();
    }

    ttModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Carrega e dá play NO MESMO FRAME DO CLIQUE
    loadVideoData(item);
  }

  let isTransitioning = false;

  function nextTikTokVideo() {
    if (!videoList || videoList.length <= 1 || isTransitioning) return;
    isTransitioning = true;
    const nextIndex = (currentVideoIndex + 1) % videoList.length;
    animateVideoSwitch(nextIndex, 'up');
  }

  function prevTikTokVideo() {
    if (!videoList || videoList.length <= 1 || isTransitioning) return;
    isTransitioning = true;
    const prevIndex = (currentVideoIndex - 1 + videoList.length) % videoList.length;
    animateVideoSwitch(prevIndex, 'down');
  }

  function animateVideoSwitch(newIndex, direction) {
    const wrapper = ttModal ? ttModal.querySelector('.tt-video-wrapper') : null;
    const playOverlay = document.getElementById('tt-play-overlay');
    if (playOverlay) playOverlay.style.display = 'none';

    if (wrapper) {
      const exitY = direction === 'up' ? '-100%' : '100%';
      const enterY = direction === 'up' ? '100%' : '-100%';

      wrapper.style.transition = 'transform 0.22s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.22s ease';
      wrapper.style.transform = `translateY(${exitY})`;
      wrapper.style.opacity = '0.5';

      setTimeout(() => {
        currentVideoIndex = newIndex;
        loadVideoData(videoList[currentVideoIndex]);

        wrapper.style.transition = 'none';
        wrapper.style.transform = `translateY(${enterY})`;
        wrapper.style.opacity = '0.5';

        wrapper.offsetHeight; // Força reflow

        requestAnimationFrame(() => {
          wrapper.style.transition = 'transform 0.22s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.22s ease';
          wrapper.style.transform = 'translateY(0)';
          wrapper.style.opacity = '1';

          setTimeout(() => {
            wrapper.style.transition = '';
            wrapper.style.transform = '';
            wrapper.style.opacity = '';
            isTransitioning = false;
          }, 240);
        });
      }, 210);
    } else {
      currentVideoIndex = newIndex;
      loadVideoData(videoList[currentVideoIndex]);
      isTransitioning = false;
    }
  }

  window.openTikTokVideo = openTikTokVideo;
  window.nextTikTokVideo = nextTikTokVideo;
  window.prevTikTokVideo = prevTikTokVideo;

  function closeTikTokModal() {
    if (ttModal) {
      ttModal.classList.remove('comments-open');
      const drw = document.getElementById('tt-comments-drawer');
      if (drw) drw.classList.remove('open');
      ttModal.style.display = 'none';
      document.body.style.overflow = '';
      if (ttVideo) {
        try { ttVideo.pause(); } catch(e) {}
        ttVideo.removeAttribute('src');
        ttVideo.removeAttribute('data-active-src');
        try { ttVideo.load(); } catch(e) {}
      }
      const playOverlay = document.getElementById('tt-play-overlay');
      if (playOverlay) playOverlay.style.display = 'none';
    }
  }

  // Carrega Dados do Vídeo e Inicia Reprodução Instantânea com Faststart
  function loadVideoData(item) {
    if (!ttVideo) return;

    const targetSrc = item.video;
    const posterSrc = item.poster || item.avatar || '';
    const playOverlay = document.getElementById('tt-play-overlay');

    // Seta imediatamente o poster para nunca piscar preto
    if (posterSrc) {
      ttVideo.poster = posterSrc;
      const wrapper = ttModal ? ttModal.querySelector('.tt-video-wrapper') : null;
      if (wrapper) {
        wrapper.style.backgroundImage = 'url("' + posterSrc + '")';
        wrapper.style.backgroundSize = 'cover';
        wrapper.style.backgroundPosition = 'center';
      }
    }

    // Atualiza metadados textuais, avatar idêntico ao card, nome idêntico ao card e contadores
    const actionAvatar = document.getElementById('tt-action-avatar');
    if (actionAvatar && item.avatar) actionAvatar.src = item.avatar;
    const musicAvatar = document.getElementById('tt-music-avatar');
    if (musicAvatar && item.avatar) musicAvatar.src = item.avatar;

    const displayName = document.getElementById('tt-display-name');
    if (displayName) displayName.textContent = item.name || item.username || 'Criador';
    const displayDate = document.getElementById('tt-display-date');
    if (displayDate) displayDate.textContent = `· ${item.postDate || '11-20'}`;

    const displayDesc = document.getElementById('tt-display-desc');
    if (displayDesc) {
      displayDesc.classList.remove('is-expanded');
      const rawDesc = String(item.description || item.desc || '').trim();
      if (rawDesc.length > 62) {
        displayDesc.innerHTML = `${rawDesc.slice(0, 58).trim().replace(/</g, '&lt;')}....<span style="color:rgba(255,255,255,0.78);font-weight:500;">mais</span>`;
        displayDesc.onclick = function(ev) {
          ev.stopPropagation();
          if (displayDesc.classList.contains('is-expanded')) {
            displayDesc.classList.remove('is-expanded');
            displayDesc.innerHTML = `${rawDesc.slice(0, 58).trim().replace(/</g, '&lt;')}....<span style="color:rgba(255,255,255,0.78);font-weight:500;">mais</span>`;
          } else {
            displayDesc.classList.add('is-expanded');
            displayDesc.textContent = rawDesc;
          }
        };
      } else {
        displayDesc.textContent = rawDesc;
        displayDesc.onclick = null;
      }
    }

    const displayMusic = document.getElementById('tt-display-music');
    if (displayMusic) {
      const cleanHandle = String(item.username || item.name || 'criador').replace(/^@/, '');
      displayMusic.textContent = `som original - ${cleanHandle} ...`;
    }

    const likeCount = document.getElementById('tt-like-count');
    if (likeCount) likeCount.textContent = formatNumber(item.likes || 5089);
    const commentCount = document.getElementById('tt-comment-count');
    if (commentCount) commentCount.textContent = formatNumber(item.commentsCount || 94);
    const saveCount = document.getElementById('tt-save-count');
    if (saveCount) saveCount.textContent = formatNumber(item.saves || 695);
    const shareCount = document.getElementById('tt-share-count');
    if (shareCount) shareCount.textContent = formatNumber(item.shares || 753);

    // Atualiza Âncora Oficial de Produto (Loja - ... / Frete grátis · Devoluções gratuitas) + Barra Shop do Drawer
    const anchorEl = document.getElementById('tt-product-anchor');
    const anchorTitle = document.getElementById('tt-anchor-title');
    const prodObj = (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL) ? PRODUTO_ATUAL : (window.PRODUTO_ATUAL || {});
    const pName = prodObj.nome || (document.title ? document.title.replace(' - Stone Shop', '').trim() : 'Produto Oficial');
    if (anchorTitle) {
      anchorTitle.textContent = `Loja - ${pName}`;
      if (anchorEl) {
        anchorEl.setAttribute('data-product-id', prodObj.id || '');
        anchorEl.onclick = function(e) {
          e.stopPropagation();
          closeTikTokModal();
          const buyBtn = document.getElementById('btn-buy') || document.querySelector('.btn-buy');
          if (buyBtn) buyBtn.click();
        };
      }
    }

    const drawerShopName = document.getElementById('tt-drawer-shop-name');
    if (drawerShopName) drawerShopName.textContent = `Shop·${pName}`;
    const drawerShopSold = document.getElementById('tt-drawer-shop-sold');
    if (drawerShopSold) {
      const domSoldNum = document.querySelector('.sold-count .sold-num')?.textContent?.trim();
      const rawSold = domSoldNum || String(prodObj.sales || '').replace(/[^\d]/g, '') || '3842';
      drawerShopSold.textContent = `${rawSold} vendidos`;
    }
    const drawerShopLink = document.getElementById('tt-drawer-shop-link');
    if (drawerShopLink) {
      drawerShopLink.onclick = function(e) {
        e.stopPropagation();
        closeTikTokModal();
        const buyBtn = document.getElementById('btn-buy') || document.querySelector('.btn-buy');
        if (buyBtn) buyBtn.click();
      };
    }

    const drawerTitle = document.getElementById('tt-drawer-title');
    if (drawerTitle) {
      const cNum = parseStatNumber(item.commentsCount, 94);
      drawerTitle.textContent = `${formatNumber(cNum)} ${cNum === 1 ? 'comentário' : 'comentários'}`;
    }

    const likeSvg = document.querySelector('#tt-action-like svg');
    if (likeSvg) likeSvg.style.fill = item.liked ? '#f7355a' : '#ffffff';
    const saveSvg = document.querySelector('#tt-action-save svg');
    if (saveSvg) saveSvg.style.fill = item.saved ? '#face15' : '#ffffff';

    const followEl = document.getElementById('tt-action-follow');
    if (followEl) {
      followEl.innerHTML = item.followed
        ? '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>'
        : '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>';
      followEl.style.background = item.followed ? '#25D366' : '#f7355a';
    }

    // Renderizar comentários da gaveta 1:1 com a referência oficial
    const commentsList = document.getElementById('tt-drawer-comments-list') || document.getElementById('tt-drawer-list');
    if (commentsList && item.commentsList) {
      commentsList.innerHTML = '';
      const firstUserIdx = item.commentsList.findIndex(x => !x.isCreator);
      item.commentsList.forEach((c, cIdx) => {
        const el = document.createElement('div');
        el.className = 'tt-comment-item';
        const showFirstBadge = cIdx === (firstUserIdx >= 0 ? firstUserIdx : 0) && !c.isCreator;
        el.innerHTML = `
          <img class="tt-comment-avatar" src="${c.avatar}" alt="" onerror="this.src='../img/reviews-avatars/mulheres_validadas/mulher_1.jpg'">
          <div style="flex:1; min-width:0;">
            <div class="tt-comment-user">${c.user}${c.isCreator ? ' <span style="background: #fe2c55; color: #fff; font-size: 9.5px; font-weight: 600; padding: 1px 5px; border-radius: 3px; vertical-align: middle; margin-left: 3px;">Criador</span>' : ''}</div>
            <div class="tt-comment-text">${c.text}</div>
            ${showFirstBadge ? '<div class="tt-comment-first-badge">Primeiro comentário</div>' : ''}
            <div class="tt-comment-footer">
              <div class="tt-comment-meta-left">
                <span class="tt-comment-date">${c.date}</span>
                <span class="tt-comment-reply">Responder</span>
              </div>
              <div class="tt-comment-actions-right">
                <div class="tt-comment-like-box" style="color:${c.liked ? '#f7355a' : '#73747b'};">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="${c.liked ? '#f7355a' : 'none'}" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
                  <span class="tt-comment-like-count">${c.likes > 0 ? c.likes : ''}</span>
                </div>
                <div class="tt-comment-dislike-box" style="color:${c.disliked ? '#161823' : '#73747b'};">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"><path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"></path></svg>
                </div>
              </div>
            </div>
          </div>
        `;
        const replyBtn = el.querySelector('.tt-comment-reply');
        if (replyBtn) {
          replyBtn.onclick = function(e) {
            e.stopPropagation();
            const inp = document.getElementById('tt-comment-input-field');
            if (inp) {
              inp.placeholder = `Responder a ${c.user}...`;
              inp.focus();
            }
          };
        }
        const likeBox = el.querySelector('.tt-comment-like-box');
        if (likeBox) {
          likeBox.onclick = function(e) {
            e.stopPropagation();
            c.liked = !c.liked;
            c.likes = (c.likes || 0) + (c.liked ? 1 : -1);
            this.style.color = c.liked ? '#f7355a' : '#73747b';
            const svg = this.querySelector('svg');
            if (svg) svg.setAttribute('fill', c.liked ? '#f7355a' : 'none');
            this.querySelector('.tt-comment-like-count').textContent = c.likes > 0 ? c.likes : '';
          };
        }
        const dislikeBox = el.querySelector('.tt-comment-dislike-box');
        if (dislikeBox) {
          dislikeBox.onclick = function(e) {
            e.stopPropagation();
            c.disliked = !c.disliked;
            this.style.color = c.disliked ? '#161823' : '#73747b';
          };
        }
        commentsList.appendChild(el);
      });
    }

    // Configura source do vídeo (sem chamar .load() para não abortar o gesto do usuário)
    if (ttVideo.getAttribute('data-active-src') !== targetSrc) {
      ttVideo.setAttribute('data-active-src', targetSrc);
      ttVideo.src = targetSrc;
    }

    ttVideo.onplaying = function() {
      if (playOverlay) playOverlay.style.display = 'none';
      const wrapper = ttModal ? ttModal.querySelector('.tt-video-wrapper') : null;
      if (wrapper) wrapper.style.backgroundImage = 'none';
      updateSoundBadge();
    };

    // DISPARO IMEDIATO DO PLAY:
    // Tenta unmuted (com som). Se o navegador mobile bloquear por política de áudio, toca muted na hora!
    ttVideo.muted = false;
    const playPromise = ttVideo.play();
    if (playPromise !== undefined) {
      playPromise.then(() => {
        if (playOverlay) playOverlay.style.display = 'none';
        updateSoundBadge();
      }).catch(err => {
        console.warn('Autoplay unmuted barrado no celular, tocando muted garantido:', err);
        ttVideo.muted = true;
        ttVideo.play().then(() => {
          if (playOverlay) playOverlay.style.display = 'none';
          updateSoundBadge();
        }).catch(err2 => {
          console.warn('Play falhou completamente:', err2);
          if (playOverlay) playOverlay.style.display = 'flex';
        });
      });
    }
  }

  function init() {
    injectStyles();
    initCarousel();
  }


  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
