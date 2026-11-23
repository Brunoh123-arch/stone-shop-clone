const fs = require('fs');
const path = require('path');

const jsPath = path.join(__dirname, 'js', 'videos-criadores.js');

const newJsContent = `// =============================================================
// LÓGICA E UI DOS VÍDEOS DOS CRIADORES — js/videos-criadores.js
// SISTEMA OFICIAL TIKTOK SHOP (COM SUPORTE CONTEXTUAL POR PRODUTO)
// =============================================================

(function() {
  // 1. DATASET DE MODA / CALÇADOS / CHINELO / SANDÁLIA (PRODUTO PRINCIPAL 104)
  const CREATORS_FASHION = [
    {
      name: "Amanda Ribeiro",
      username: "amandaribeiroo",
      avatar: "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.11.jpeg",
      poster: "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/4b108ccc0c6e416ca36785b3b83d1cc3~tplv-aphluv4xwc-resize-jpeg:800:1066.jpeg",
      video: "../img/tiktok-anim-v5.mp4",
      likes: 14820,
      commentsCount: 124,
      saves: 1820,
      shares: 340,
      description: "Gente, chocada com o brilho desse chinelo de strass! ✨ Super macio, parece que tô pisando em nuvem. Chegou em 3 dias aqui em SP! #tiktokshop #moda #chinelo"
    },
    {
      name: "Juliana Costa",
      username: "julianastyle",
      avatar: "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.11 (1).jpeg",
      poster: "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/de0ebc96ce0f425994bce34ba59976d3~tplv-aphluv4xwc-resize-jpeg:800:1066.jpeg",
      video: "../img/tiktok-anim-v5.mp4",
      likes: 9340,
      commentsCount: 87,
      saves: 950,
      shares: 210,
      description: "Look do dia combinando o chinelo preto com vestido leve de verão. O strass dá um toque chique sem perder o conforto! 👡💖"
    },
    {
      name: "Camila Rocha",
      username: "camilasouza.fit",
      avatar: "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.11 (2).jpeg",
      poster: "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/337346130ae44bd5a6b821de09482ee4~tplv-aphluv4xwc-resize-jpeg:800:1066.jpeg",
      video: "../img/tiktok-anim-v5.mp4",
      likes: 21540,
      commentsCount: 198,
      saves: 3410,
      shares: 780,
      description: "Dica de achadinho no TikTok Shop que valeu cada centavo! Peguei o caramelo e o branco. A sola é antiderrapante e muito segura."
    },
    {
      name: "Mariana Castro",
      username: "maricastroboutique",
      avatar: "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.12.jpeg",
      poster: "../img/ranking-top1.webp",
      video: "../img/tiktok-anim-v5.mp4",
      likes: 12100,
      commentsCount: 95,
      saves: 1420,
      shares: 290,
      description: "Unboxing e teste de conforto! Não machuca entre os dedos e a tira cravejada de strass é super resistente. Nota 10/10!"
    },
    {
      name: "Beatriz Lima",
      username: "bialima_closet",
      avatar: "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.12 (1).jpeg",
      poster: "../img/ranking-top2.webp",
      video: "../img/tiktok-anim-v5.mp4",
      likes: 8750,
      commentsCount: 64,
      saves: 880,
      shares: 160,
      description: "Mostrando de pertinho os detalhes desse brilho! Já lavei e não soltou nenhuma pedrinha. Muito apaixonada!"
    },
    {
      name: "Larissa Mendes",
      username: "larimendes_oficial",
      avatar: "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.12 (2).jpeg",
      poster: "../img/ranking-top3.webp",
      video: "../img/tiktok-anim-v5.mp4",
      likes: 16420,
      commentsCount: 142,
      saves: 2100,
      shares: 430,
      description: "Minha mãe e minha irmã também pediram depois que viram o meu. Conforto absurdo para o dia a dia! 🌸"
    },
    {
      name: "Patrícia Lima",
      username: "paty_lima92",
      avatar: "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.13 (1).jpeg",
      poster: "../img/ranking-novo.webp",
      video: "../img/tiktok-anim-v5.mp4",
      likes: 7230,
      commentsCount: 53,
      saves: 690,
      shares: 110,
      description: "Chegou super bem embalado com saquinho de proteção individual. Frete grátis do TikTok entregou rapidinho!"
    },
    {
      name: "Fernanda Dias",
      username: "fehdias_modas",
      avatar: "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.13 (2).jpeg",
      poster: "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/4b108ccc0c6e416ca36785b3b83d1cc3~tplv-aphluv4xwc-resize-jpeg:800:1066.jpeg",
      video: "../img/tiktok-anim-v5.mp4",
      likes: 11840,
      commentsCount: 110,
      saves: 1350,
      shares: 270,
      description: "Perfeito para praia, piscina ou passeio casual. Combina com jeans, shorts e saia. Amei demais!"
    }
  ];

  // 2. DATASET AUTOMOTIVO / PNEUS PIRELLI (APENAS PARA PRODUTO-101)
  const CREATORS_TIRES = [
    {
      name: "Império Neumáticos",
      username: "imperioneumaticos",
      avatar: "../fotodeperfildoscriadores/WhatsApp Image 2026-07-27 at 19.37.32.jpeg",
      poster: "",
      video: "../videosdoscriadorespneu/WhatsApp Video 2026-07-27 at 19.36.22.mp4",
      likes: 4402,
      commentsCount: 28,
      saves: 915,
      shares: 175,
      description: "Pneu Pirelli é bom? Mostramos os principais pontos técnicos que influenciam na escolha do pneu ideal para o seu veículo! #pirelli #pneus"
    },
    {
      name: "Auto Soft",
      username: "autosoft",
      avatar: "../fotodeperfildoscriadores/WhatsApp Image 2026-07-27 at 19.37.33 (1).jpeg",
      poster: "",
      video: "../videosdoscriadorespneu/WhatsApp Video 2026-07-27 at 19.36.26.mp4",
      likes: 8912,
      commentsCount: 21,
      saves: 456,
      shares: 89,
      description: "Super dica de calibragem dos pneus Pirelli! Economiza combustível e aumenta a vida útil da borracha. Confere aí! 🚗🔥"
    },
    {
      name: "Gerardo Bastos",
      username: "gerardobastos",
      avatar: "../fotodeperfildoscriadores/WhatsApp Image 2026-07-27 at 19.37.33 (2).jpeg",
      poster: "",
      video: "../videosdoscriadorespneu/WhatsApp Video 2026-07-27 at 19.36.27.mp4",
      likes: 12304,
      commentsCount: 25,
      saves: 812,
      shares: 230,
      description: "Mostrando a incrível tecnologia Seal Inside do Pirelli Cinturato P7. Fura e não perde o ar na hora! Sensacional!"
    },
    {
      name: "Alpha Centro Automotivo",
      username: "alphacentro",
      avatar: "../fotodeperfildoscriadores/WhatsApp Image 2026-07-27 at 19.37.33 (3).jpeg",
      poster: "",
      video: "../videosdoscriadorespneu/WhatsApp Video 2026-07-27 at 19.36.32.mp4",
      likes: 5120,
      commentsCount: 19,
      saves: 310,
      shares: 64,
      description: "Por que escolher o Pirelli P Zero para o seu esportivo? Aderência absurda nas curvas e resposta imediata. 🏁⚡"
    }
  ];

  // Avatares FEMININOS reais mapeados do diretório FOTOSDEPERFIL
  const AVATARS_FEMININOS = [
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.18.jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.18 (2).jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.18 (4).jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.20 (2).jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.19 (3).jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.18 (3).jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.17.jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.19 (4).jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.18 (5).jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.17 (5).jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.11 (2).jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.20 (1).jpeg"
  ];

  const AVATARS_MASCULINOS = [
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.13 (2).jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.11.jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.13 (5).jpeg",
    "../FOTOSDEPERFIL/WhatsApp Image 2026-06-29 at 23.31.20 (3).jpeg"
  ];

  const NOMES_FEMININOS = ["camila", "larissa", "aninha", "gabi", "mari", "bia", "ju", "amanda"];

  function getAvatarByGender(username) {
    const nameLower = username.toLowerCase();
    const isFem = NOMES_FEMININOS.some(n => nameLower.startsWith(n));
    let hash = 0;
    for (let i = 0; i < username.length; i++) {
      hash = (hash << 5) - hash + username.charCodeAt(i);
      hash |= 0;
    }
    const idx = Math.abs(hash);
    return isFem ? AVATARS_FEMININOS[idx % AVATARS_FEMININOS.length] : AVATARS_MASCULINOS[idx % AVATARS_MASCULINOS.length];
  }

  // Comentários de Moda / Sandália / Chinelo
  const COMMENTS_FASHION = [
    "Gente, esse chinelo é lindo demais, o strass brilha muito na luz! 💖",
    "Chegou certinho aqui no RJ em 4 dias, super bem embalado!",
    "Peguei o tamanho 37/38 e ficou perfeito no pé, muito macio.",
    "Não machuca nada entre os dedos, dá pra andar o dia todo.",
    "Comprei o branco e agora quero o preto e o caramelo também kkkk",
    "Qualidade surreal pelo preço, no shopping um desse não sai por menos de 100!",
    "Amei demais, super levinho e a sola não escorrega em piso molhado.",
    "Minha mãe viu o meu e pediu pra comprar um pra ela também!",
    "Entrega rápida e frete grátis, nota 10 TikTok Shop!",
    "Combina com tudo, vestido, shortinho jeans, saia... perfeito pro verão!",
    "O acabamento das pedrinhas é muito firme, não solta fácil.",
    "Podem comprar sem medo meninas, é idêntico ao anúncio!",
    "Muito delicado nos pés, dá um charme especial no look.",
    "Chegou antes do prazo e veio com saquinho de proteção, amei!",
    "O salto é baixinho e super confortável, não cansa nada as pernas."
  ];

  // Comentários de Pneus
  const COMMENTS_TIRES = [
    "pneu excelente, recomendo demais!",
    "coloquei o cinturato p7 e achei muito macio no asfalto",
    "Pirelli original de verdade, vale cada centavo",
    "entrega rápida, comprei no pix e enviaram na hora",
    "borracha muito fresca, DOT de fabricação recente"
  ];

  const USERNAME_PREFIXES = ["camila_", "larissa.", "aninha_", "gabi_", "mari_", "bia_closet", "ju_costa", "amanda_"];

  function generateRandomComment(idx, isTires) {
    const prefix = USERNAME_PREFIXES[idx % USERNAME_PREFIXES.length];
    const user = \`\${prefix}\${(idx * 17) % 100}\`;
    const avatar = getAvatarByGender(user);
    const pool = isTires ? COMMENTS_TIRES : COMMENTS_FASHION;
    const text = pool[idx % pool.length];
    const dates = ["5-7", "2026-10-11", "2026-10-13", "4-17", "2026-09-21"];
    const date = dates[idx % dates.length];
    const likes = Math.floor(((idx * 7) % 85) + 15);
    return { avatar, user, text, date, likes, liked: false };
  }

  // Elementos globais do modal TikTok
  let ttModal = null;
  let ttVideo = null;
  let ttLoader = null;
  let currentVideoIndex = 0;
  let videoList = [];

  function formatNumber(num) {
    return num.toLocaleString('pt-BR');
  }

  // Injeta estilos CSS necessários
  function injectStyles() {
    if (document.getElementById('tt-styles')) return;
    const style = document.createElement('style');
    style.id = 'tt-styles';
    style.innerHTML = \`
      .creators-section {
        padding: 16px;
        background: #ffffff;
        margin-bottom: 8px;
        border-bottom: 8px solid #f5f5f5;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "TikTok Sans", "Plus Jakarta Sans", sans-serif;
      }
      .creators-title {
        font-size: 16px;
        font-weight: 700;
        color: #161823;
        margin-bottom: 12px;
        letter-spacing: -0.2px;
      }
      .creators-carousel {
        display: flex;
        gap: 8px;
        overflow-x: auto;
        padding: 0 2px 8px 2px;
        scroll-behavior: smooth;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
      }
      .creators-carousel::-webkit-scrollbar {
        display: none;
      }
      .creator-card {
        position: relative;
        flex: 0 0 94px;
        height: 154px;
        border-radius: 8px;
        overflow: hidden;
        background: #161823;
        cursor: pointer;
        user-select: none;
      }
      .tt-modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #000;
        z-index: 100000;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
      .tt-container {
        position: relative;
        width: 100%;
        max-width: 480px;
        height: 100%;
        background: #000;
        display: flex;
        flex-direction: column;
        overflow: hidden;
      }
      .tt-top-bar {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        padding: 12px 14px;
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 10;
        box-sizing: border-box;
        background: linear-gradient(180deg, rgba(0,0,0,0.6) 0%, transparent 100%);
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
        position: relative;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #000;
      }
      .tt-video {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .tt-right-actions {
        position: absolute;
        right: 12px;
        bottom: 84px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
        z-index: 5;
      }
      .tt-creator-wrapper {
        position: relative;
        margin-bottom: 4px;
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
        bottom: -6px;
        left: 50%;
        transform: translateX(-50%);
        background: #fe2c55;
        color: #fff;
        border: none;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        font-size: 14px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
      }
      .tt-action-btn {
        background: none;
        border: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        color: #fff;
        cursor: pointer;
        gap: 4px;
      }
      .tt-action-label {
        font-size: 12px;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
      }
      .tt-left-info {
        position: absolute;
        bottom: 16px;
        left: 12px;
        right: 80px;
        color: #fff;
        z-index: 5;
      }
      .tt-username {
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 6px;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
      }
      .tt-desc {
        font-size: 13.5px;
        line-height: 1.35;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
      }
      /* Drawer de comentários */
      .tt-comments-drawer {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 65%;
        background: #fff;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        transform: translateY(100%);
        transition: transform 0.25s ease-out;
        z-index: 100;
        display: flex;
        flex-direction: column;
      }
      .tt-comments-drawer.open {
        transform: translateY(0);
      }
      .tt-drawer-header {
        padding: 14px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #f2f2f2;
      }
      .tt-drawer-title {
        font-size: 14px;
        font-weight: 700;
        color: #161823;
      }
      .tt-drawer-close {
        background: none;
        border: none;
        font-size: 18px;
        cursor: pointer;
        color: #888;
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
    \`;
    document.head.appendChild(style);
  }

  // Inicializa o carrossel na página
  function initCarousel() {
    const targetContainer = document.getElementById('creators-section');
    if (!targetContainer) return;

    // Detecta contexto do produto
    const pageText = (document.title + ' ' + (document.querySelector('h1')?.textContent || '')).toLowerCase();
    const url = window.location.pathname.toLowerCase();

    const isTires = url.includes('produto-101') || pageText.includes('pneu') || pageText.includes('pirelli');
    const activeDataset = isTires ? CREATORS_TIRES : CREATORS_FASHION;

    // Criamos a estrutura interna do carrossel
    targetContainer.innerHTML = \`
      <h3 class="creators-title">Vídeos de criadores (28+)</h3>
      <div class="creators-carousel" id="creators-carousel-list"></div>
    \`;

    const listElement = document.getElementById('creators-carousel-list');
    const totalCardsCount = 28;
    videoList = [];

    for (let i = 0; i < totalCardsCount; i++) {
      const originalItem = activeDataset[i % activeDataset.length];
      const videoId = i;
      
      const likesOffset = (i * 123) % 1500 - 750;
      const finalLikes = Math.max(2000, Math.min(16000, originalItem.likes + likesOffset));
      const commentsOffset = (i * 3) % 8 - 4;
      const finalComments = Math.max(17, Math.min(29, originalItem.commentsCount + commentsOffset));

      const item = {
        id: videoId,
        name: originalItem.name,
        username: originalItem.username,
        avatar: originalItem.avatar,
        poster: originalItem.poster || originalItem.avatar,
        video: originalItem.video,
        likes: finalLikes,
        commentsCount: finalComments,
        saves: originalItem.saves + (i * 11) % 150,
        shares: originalItem.shares + (i * 7) % 50,
        description: originalItem.description,
        liked: false,
        saved: false,
        followed: false,
        commentsList: []
      };

      for (let j = 0; j < item.commentsCount; j++) {
        item.commentsList.push(generateRandomComment(j + i * 2, isTires));
      }

      videoList.push(item);

      // Card com preview do vídeo real
      const cardHtml = \`
        <div class="creator-card" data-video-id="\${videoId}">
          <img src="\${item.poster}" alt="\${item.name}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 40%, rgba(0,0,0,0.75) 100%);"></div>
          <div style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2;">
            <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 6px; display: flex; align-items: center; gap: 5px; z-index: 2; box-sizing: border-box;">
            <img src="\${item.avatar}" alt="\${item.name}" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;" onerror="this.src='https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/085171b8ffe0c64bcc1fce3ce127b415~tplv-tiktokx-cropcenter:100:100.jpg'">
            <span style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">\${item.name}</span>
          </div>
        </div>
      \`;
      listElement.insertAdjacentHTML('beforeend', cardHtml);
    }

    // Vincula clique nos cards APENAS UMA VEZ
    const cards = listElement.querySelectorAll('.creator-card');
    cards.forEach(card => {
      card.addEventListener('click', function() {
        const id = parseInt(this.getAttribute('data-video-id'), 10);
        openTikTokVideo(id);
      });
    });
  }

  // Cria e abre o Modal TikTok
  function openTikTokVideo(id) {
    currentVideoIndex = id;
    const item = videoList[id];
    if (!item) return;

    if (!ttModal) {
      createTikTokModalMarkup();
    }

    ttModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    loadVideoData(item);
  }

  function closeTikTokModal() {
    if (ttModal) {
      ttModal.style.display = 'none';
      document.body.style.overflow = '';
      if (ttVideo) {
        ttVideo.pause();
        ttVideo.src = "";
      }
    }
  }

  function createTikTokModalMarkup() {
    ttModal = document.createElement('div');
    ttModal.className = 'tt-modal';
    ttModal.id = 'tiktok-modal';

    ttModal.innerHTML = \`
      <div class="tt-container">
        <div class="tt-top-bar">
          <button class="tt-back-btn" id="tt-close-btn">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
          </button>
          <div class="tt-search-container">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input class="tt-search-input" type="text" value="Encontrar conteúdo relacionado" readonly>
          </div>
        </div>

        <div class="tt-video-wrapper">
          <video class="tt-video" id="tt-modal-player" loop playsinline autoplay></video>

          <div class="tt-right-actions">
            <div class="tt-creator-wrapper">
              <img class="tt-creator-avatar" id="tt-action-avatar" src="" alt="avatar">
              <button class="tt-follow-btn" id="tt-action-follow">+</button>
            </div>
            <button class="tt-action-btn" id="tt-action-like">
              <svg viewBox="0 0 24 24" width="36" height="36" fill="#fff"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
              <span class="tt-action-label" id="tt-like-count">0</span>
            </button>
            <button class="tt-action-btn" id="tt-action-comment">
              <svg viewBox="0 0 24 24" width="34" height="34" fill="#fff"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              <span class="tt-action-label" id="tt-comment-count">0</span>
            </button>
            <button class="tt-action-btn" id="tt-action-save">
              <svg viewBox="0 0 24 24" width="34" height="34" fill="#fff"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
              <span class="tt-action-label" id="tt-save-count">0</span>
            </button>
          </div>

          <div class="tt-left-info">
            <div class="tt-username" id="tt-display-name">@amandaribeiroo</div>
            <div class="tt-desc" id="tt-display-desc"></div>
          </div>
        </div>

        <div class="tt-comments-drawer" id="tt-comments-drawer">
          <div class="tt-drawer-header">
            <span class="tt-drawer-title" id="tt-drawer-title">Comentários</span>
            <button class="tt-drawer-close" id="tt-drawer-close">✕</button>
          </div>
          <div class="tt-drawer-list" id="tt-drawer-list"></div>
        </div>
      </div>
    \`;

    document.body.appendChild(ttModal);
    ttVideo = document.getElementById('tt-modal-player');

    document.getElementById('tt-close-btn').addEventListener('click', closeTikTokModal);
    document.getElementById('tt-drawer-close').addEventListener('click', () => {
      document.getElementById('tt-comments-drawer').classList.remove('open');
    });
    document.getElementById('tt-action-comment').addEventListener('click', () => {
      document.getElementById('tt-comments-drawer').classList.toggle('open');
    });

    const likeBtn = document.getElementById('tt-action-like');
    likeBtn.addEventListener('click', function() {
      const item = videoList[currentVideoIndex];
      item.liked = !item.liked;
      this.querySelector('svg').style.fill = item.liked ? '#fe2c55' : '#fff';
      item.likes += item.liked ? 1 : -1;
      document.getElementById('tt-like-count').textContent = formatNumber(item.likes);
    });

    const followBtn = document.getElementById('tt-action-follow');
    followBtn.addEventListener('click', function() {
      const item = videoList[currentVideoIndex];
      item.followed = !item.followed;
      this.textContent = item.followed ? '✓' : '+';
      this.style.background = item.followed ? '#25D366' : '#fe2c55';
    });
  }

  function loadVideoData(item) {
    if (!ttVideo) return;
    ttVideo.src = item.video;
    ttVideo.play().catch(e => console.log('Autoplay:', e));

    document.getElementById('tt-action-avatar').src = item.avatar;
    document.getElementById('tt-display-name').textContent = \`@\${item.username}\`;
    document.getElementById('tt-display-desc').textContent = item.description;
    document.getElementById('tt-like-count').textContent = formatNumber(item.likes);
    document.getElementById('tt-comment-count').textContent = formatNumber(item.commentsCount);
    document.getElementById('tt-save-count').textContent = formatNumber(item.saves);
    document.getElementById('tt-drawer-title').textContent = \`\${formatNumber(item.commentsCount)} comentários\`;

    // Renderizar comentários
    const list = document.getElementById('tt-drawer-list');
    list.innerHTML = '';
    item.commentsList.forEach(c => {
      const el = document.createElement('div');
      el.className = 'tt-comment-item';
      el.innerHTML = \`
        <img class="tt-comment-avatar" src="\${c.avatar}" alt="\${c.user}" onerror="this.src='https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/085171b8ffe0c64bcc1fce3ce127b415~tplv-tiktokx-cropcenter:100:100.jpg'">
        <div style="flex:1;">
          <div class="tt-comment-user">\${c.user}</div>
          <div class="tt-comment-text">\${c.text}</div>
          <div style="font-size:11px; color:#999; margin-top:3px;">\${c.date} · Responder</div>
        </div>
        <div style="display:flex; flex-direction:column; align-items:center; color:#888; font-size:11px;">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          <span>\${c.likes}</span>
        </div>
      \`;
      list.appendChild(el);
    });
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
`;

fs.writeFileSync(jsPath, newJsContent, 'utf8');
console.log('✅ js/videos-criadores.js reconstruído do zero com separação 100% perfeita de sandália/chinelo e pneus!');

// Sincronizar com ds/js/videos-criadores.js
const dsJsPath = path.join('C:', 'Users', 'Dell', 'Downloads', 'ds', 'js', 'videos-criadores.js');
if (fs.existsSync(dsJsPath)) {
  fs.writeFileSync(dsJsPath, newJsContent, 'utf8');
  console.log('✅ ds/js/videos-criadores.js sincronizado!');
}
