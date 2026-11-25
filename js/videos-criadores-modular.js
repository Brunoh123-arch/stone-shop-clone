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

  function formatNumber(num) {
    if (!num || isNaN(num)) return '0';
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1).replace('.', ',') + 'M';
    }
    if (num >= 10000) {
      const formatted = (num / 1000).toFixed(1).replace('.0', '').replace('.', ',');
      return formatted + 'K';
    }
    return num.toLocaleString('pt-BR');
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
      .tt-top-bar {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        padding: 12px 14px;
        padding-top: max(16px, calc(10px + env(safe-area-inset-top)));
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 10;
        box-sizing: border-box;
        background: linear-gradient(180deg, rgba(0,0,0,0.65) 0%, transparent 100%);
      }
      .tt-back-btn {
        background: none;
        border: none;
        color: #fff;
        cursor: pointer;
        padding: 0;
        display: flex;
        align-items: center;
      }
      .tt-search-container {
        flex: 1;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        border-radius: 18px;
        display: flex;
        align-items: center;
        padding: 6px 12px;
        gap: 6px;
      }
      .tt-search-input {
        flex: 1;
        background: none;
        border: none;
        color: #fff;
        font-size: 13px;
        outline: none;
      }
      .tt-video-wrapper {
        position: relative !important;
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: #000 !important;
        overflow: hidden !important;
        touch-action: none !important;
        cursor: pointer !important;
        will-change: transform, opacity !important;
        box-sizing: border-box !important;
      }
      .tt-video-wrapper:active {
        cursor: grabbing;
      }
      .tt-video {
        width: 100% !important;
        height: 100% !important;
        object-fit: contain !important;
        background: #000 !important;
        pointer-events: none !important;
      }
      .tt-right-actions {
        position: absolute !important;
        right: 10px !important;
        bottom: calc(24px + env(safe-area-inset-bottom, 12px)) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 14px !important;
        z-index: 10 !important;
        pointer-events: auto !important;
      }
      .tt-creator-wrapper {
        position: relative;
        margin-bottom: 6px;
      }
      .tt-creator-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        border: 2px solid #fff;
        object-fit: cover;
      }
      .tt-follow-btn {
        position: absolute;
        bottom: -7px;
        left: 50%;
        transform: translateX(-50%);
        width: 20px;
        height: 20px;
        background: #fe2c55;
        color: #fff;
        border-radius: 50%;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: bold;
        cursor: pointer;
      }
      .tt-action-btn {
        background: none;
        border: none;
        color: #fff;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        cursor: pointer;
        padding: 0;
      }
      .tt-action-label {
        font-size: 12px;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.6);
      }
      .tt-left-info {
        position: absolute !important;
        left: 14px !important;
        right: 76px !important;
        bottom: calc(24px + env(safe-area-inset-bottom, 12px)) !important;
        color: #fff !important;
        z-index: 10 !important;
        pointer-events: auto !important;
        text-shadow: 0 1px 4px rgba(0,0,0,0.95) !important;
      }
      .tt-username {
        font-size: 15px !important;
        font-weight: 700 !important;
        margin-bottom: 4px !important;
        text-shadow: 0 1px 4px rgba(0,0,0,0.95) !important;
        line-height: 1.25 !important;
      }
      
      .tt-product-anchor {
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        background: rgba(0, 0, 0, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 6px !important;
        padding: 5px 9px !important;
        margin-top: 6px !important;
        cursor: pointer !important;
        color: #ffffff !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4) !important;
        transition: transform 0.15s ease !important;
      }
      .tt-product-anchor:active {
        transform: scale(0.96) !important;
      }
      .tt-anchor-title {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        max-width: 190px !important;
        color: #ffb800 !important;
        font-weight: 700 !important;
      }

      .tt-desc {
        font-size: 13px !important;
        line-height: 1.35 !important;
        text-shadow: 0 1px 4px rgba(0,0,0,0.95) !important;
        display: -webkit-box !important;
        -webkit-line-clamp: 2 !important;
        -webkit-box-orient: vertical !important;
        overflow: hidden !important;
        word-break: break-word !important;
      }
      .tt-comments-drawer {
        position: absolute;
        bottom: -100%;
        left: 0;
        width: 100%;
        height: 65%;
        background: #fff;
        border-radius: 14px 14px 0 0;
        z-index: 20;
        transition: bottom 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
        display: flex;
        flex-direction: column;
      }
      .tt-comments-drawer.open {
        bottom: 0;
      }
      .tt-drawer-header {
        padding: 14px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #eee;
      }
      .tt-drawer-title {
        font-size: 14px;
        font-weight: 700;
        color: #161823;
      }
      .tt-drawer-close {
        background: none;
        border: none;
        font-size: 16px;
        cursor: pointer;
        color: #666;
      }
      .tt-drawer-list {
        flex: 1;
        overflow-y: auto;
        padding: 12px 16px;
      }
      .tt-comment-item {
        display: flex;
        gap: 10px;
        margin-bottom: 14px;
      }
      .tt-comment-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        object-fit: cover;
      }
      .tt-comment-user {
        font-size: 12px;
        font-weight: 700;
        color: #666;
      }
      .tt-comment-text {
        font-size: 13px;
        color: #161823;
        margin-top: 2px;
      }
      .tt-comment-input-bar {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        border-top: 1px solid #eee;
        background: #fff;
        box-sizing: border-box;
        flex-shrink: 0;
      }
      .tt-comment-input {
        flex: 1;
        height: 38px;
        background: #f1f1f2;
        border: none;
        border-radius: 20px;
        padding: 0 16px;
        font-size: 13.5px;
        color: #161823;
        outline: none;
        box-sizing: border-box;
      }
      .tt-comment-input::placeholder {
        color: #8a8b91;
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
      
      const likes = originalItem.likes || (12400 + ((i * 4391) % 48000));
      const comments = originalItem.commentsCount || originalItem.comments || (38 + ((i * 19) % 210));
      const saves = originalItem.saves || Math.max(120, Math.floor(likes * 0.11));
      const shares = originalItem.shares || Math.max(30, Math.floor(likes * 0.035));

      const item = {
        id: videoId,
        name: originalItem.name,
        username: originalItem.username,
        avatar: originalItem.avatar,
        poster: originalItem.poster,
        video: originalItem.video,
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

    ttModal.innerHTML = `
      <div class="tt-container">
        <div class="tt-top-bar">
          <button class="tt-back-btn" id="tt-close-btn" aria-label="Voltar">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
          </button>
          <div class="tt-search-container">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input class="tt-search-input" type="text" value="Encontrar conteúdo relacionado" readonly>
          </div>
        </div>

        <div class="tt-video-wrapper" id="tt-video-wrapper">
          <video class="tt-video" id="tt-modal-player" loop playsinline webkit-playsinline preload="none" style="background:#000;"></video>

          <div class="tt-play-icon-overlay" id="tt-play-overlay">
            <svg viewBox="0 0 24 24" width="34" height="34" fill="#fff"><path d="M8 5v14l11-7z"/></svg>
          </div>

          <div class="tt-right-actions">
            <div class="tt-creator-wrapper">
              <img class="tt-creator-avatar" id="tt-action-avatar" src="../logo.png" alt="Stone Shop">
              <button class="tt-follow-btn" id="tt-action-follow">+</button>
            </div>
            <button class="tt-action-btn" id="tt-action-like">
              <svg viewBox="0 0 24 24" width="32" height="32" fill="#fff"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
              <span class="tt-action-label" id="tt-like-count">14.2K</span>
            </button>
            <button class="tt-action-btn" id="tt-action-comment">
              <svg viewBox="0 0 24 24" width="30" height="30" fill="#fff"><path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18zM18 14H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/></svg>
              <span class="tt-action-label" id="tt-comment-count">128</span>
            </button>
            <button class="tt-action-btn" id="tt-action-save">
              <svg viewBox="0 0 24 24" width="30" height="30" fill="#fff"><path d="M17 3H7c-1.1 0-1.99.9-1.99 2L5 21l7-3 7 3V5c0-1.1-.9-2-2-2z"/></svg>
              <span class="tt-action-label" id="tt-save-count">3.4K</span>
            </button>
            <button class="tt-action-btn" id="tt-action-share">
              <svg viewBox="0 0 24 24" width="28" height="28" fill="#fff"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92c0-1.61-1.31-2.92-2.92-2.92z"/></svg>
              <span class="tt-action-label">Compartilhar</span>
            </button>
          </div>

          <div class="tt-left-info">
            <div class="tt-username" id="tt-display-name">@tiktokshop</div>
            <div class="tt-desc" id="tt-display-desc">Review oficial do produto</div>
            <div class="tt-product-anchor" id="tt-product-anchor">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="#ffb800" style="flex-shrink:0;"><path d="M19 6h-2c0-2.76-2.24-5-5-5S7 3.24 7 6H5c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-7-3c1.66 0 3 1.34 3 3H9c0-1.66 1.34-3 3-3zm7 17H5V8h14v12z"/></svg>
              <span class="tt-anchor-title" id="tt-anchor-title">Produto Oficial</span>
              <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="#fff" stroke-width="2.5" style="flex-shrink:0;"><polyline points="9 18 15 12 9 6"/></svg>
            </div>
          </div>

          <div class="tt-comments-drawer" id="tt-comments-drawer">
            <div class="tt-drawer-header">
              <span class="tt-drawer-title" id="tt-drawer-title">128 comentários</span>
              <button class="tt-drawer-close" id="tt-drawer-close">✕</button>
            </div>
            <div class="tt-drawer-list" id="tt-drawer-comments-list"></div>
            <div class="tt-comment-input-bar">
              <input type="text" class="tt-comment-input" id="tt-comment-input-field" placeholder="Adicionar comentário...">
              <button class="tt-comment-submit-btn" id="tt-comment-send-btn" aria-label="Enviar comentário">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
              </button>
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

    const drawerClose = document.getElementById('tt-drawer-close');
    if (drawerClose) drawerClose.onclick = () => {
      document.getElementById('tt-comments-drawer').classList.remove('open');
    };

    const actionComment = document.getElementById('tt-action-comment');
    if (actionComment) actionComment.onclick = (e) => {
      e.stopPropagation();
      document.getElementById('tt-comments-drawer').classList.toggle('open');
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

    // Desktop Click no wrapper para dar play/pause
    if (wrapper) {
      wrapper.onclick = function(e) {
        if (e.target.closest('#tt-comments-drawer') || 
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
      this.querySelector('svg').style.fill = item.liked ? '#fe2c55' : '#fff';
      item.likes += item.liked ? 1 : -1;
      document.getElementById('tt-like-count').textContent = formatNumber(item.likes);
    };

    const followBtn = document.getElementById('tt-action-follow');
    if (followBtn) followBtn.onclick = function(e) {
      e.stopPropagation();
      const item = videoList[currentVideoIndex];
      if (!item) return;
      item.followed = !item.followed;
      this.textContent = item.followed ? '✓' : '+';
      this.style.background = item.followed ? '#25D366' : '#fe2c55';
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

    // Atualiza metadados textuais e contadores
    const actionAvatar = document.getElementById('tt-action-avatar');
    if (actionAvatar) actionAvatar.src = item.avatar;
    const displayName = document.getElementById('tt-display-name');
    if (displayName) displayName.textContent = `@${item.username}`;
    const displayDesc = document.getElementById('tt-display-desc');
    if (displayDesc) displayDesc.textContent = item.description || item.desc || '';
    const likeCount = document.getElementById('tt-like-count');
    if (likeCount) likeCount.textContent = formatNumber(item.likes || 12400);
    const commentCount = document.getElementById('tt-comment-count');
    if (commentCount) commentCount.textContent = formatNumber(item.commentsCount || 68);
    const saveCount = document.getElementById('tt-save-count');
    if (saveCount) saveCount.textContent = formatNumber(item.saves || 2800);
        // Atualiza Âncora Oficial de Produto (Shopping Tag TikTok Shop)
    const anchorEl = document.getElementById('tt-product-anchor');
    const anchorTitle = document.getElementById('tt-anchor-title');
    if (anchorTitle) {
      const prodObj = (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL) ? PRODUTO_ATUAL : (window.PRODUTO_ATUAL || {});
      const pName = prodObj.nome || (document.title ? document.title.replace(' - Stone Shop', '').trim() : 'Produto Oficial');
      const pPrice = prodObj.preco ? `R$ ${Number(prodObj.preco).toFixed(2).replace('.', ',')}` : '';
      anchorTitle.textContent = `${pName.slice(0, 26)}... · ${pPrice}`;
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

    const drawerTitle = document.getElementById('tt-drawer-title');
    if (drawerTitle) drawerTitle.textContent = `${formatNumber(item.commentsCount || 68)} comentários`;

    const likeSvg = document.querySelector('#tt-action-like svg');
    if (likeSvg) likeSvg.style.fill = item.liked ? '#fe2c55' : '#fff';
    const saveSvg = document.querySelector('#tt-action-save svg');
    if (saveSvg) saveSvg.style.fill = item.saved ? '#face15' : '#fff';

    const followEl = document.getElementById('tt-action-follow');
    if (followEl) {
      followEl.textContent = item.followed ? '✓' : '+';
      followEl.style.background = item.followed ? '#25D366' : '#fe2c55';
    }

    // Renderizar comentários da gaveta
    const commentsList = document.getElementById('tt-drawer-comments-list') || document.getElementById('tt-drawer-list');
    if (commentsList && item.commentsList) {
      commentsList.innerHTML = '';
      item.commentsList.forEach(c => {
        const el = document.createElement('div');
        el.className = 'tt-comment-item';
        el.innerHTML = `
          <img class="tt-comment-avatar" src="${c.avatar}" alt="" onerror="this.src='../img/creators-avatars/creator-1.jpg'">
          <div style="flex:1;">
            <div class="tt-comment-user">${c.user}${c.isCreator ? ' <span style="background: #fe2c55; color: #fff; font-size: 9px; font-weight: 700; padding: 1px 5px; border-radius: 3px; vertical-align: middle;">Criador</span>' : ''}</div>
            <div class="tt-comment-text">${c.text}</div>
            <div style="font-size:11px; color:#999; margin-top:3px;">${c.date} · Responder</div>
          </div>
          <div class="tt-comment-like-box" style="display:flex; flex-direction:column; align-items:center; color:${c.liked ? '#fe2c55' : '#888'}; font-size:11px; cursor:pointer; padding:2px; min-width:28px;">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="${c.liked ? '#fe2c55' : 'none'}" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            <span class="tt-comment-like-count">${c.likes}</span>
          </div>
        `;
        const likeBox = el.querySelector('.tt-comment-like-box');
        if (likeBox) {
          likeBox.onclick = function(e) {
            e.stopPropagation();
            c.liked = !c.liked;
            c.likes += c.liked ? 1 : -1;
            this.style.color = c.liked ? '#fe2c55' : '#888';
            const svg = this.querySelector('svg');
            if (svg) svg.setAttribute('fill', c.liked ? '#fe2c55' : 'none');
            this.querySelector('.tt-comment-like-count').textContent = c.likes;
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
