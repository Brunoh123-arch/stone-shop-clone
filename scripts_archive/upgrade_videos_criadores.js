const fs = require('fs');
const path = require('path');

// 1. ATUALIZAR js/videos-criadores.js COM INTELIGÊNCIA CONTEXTUAL E CARDS COM THUMBNAILS REAIS
const jsPath = path.join(__dirname, 'js', 'videos-criadores.js');
let js = fs.readFileSync(jsPath, 'utf8');

// Injetar dataset de Moda / Calçados / Chinelo no topo
const fashionDataset = `
  // Dataset Oficial de Criadoras de Moda / Calçados / Lifestyle (TikTok Shop)
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
`;

if (!js.includes('CREATORS_FASHION')) {
  js = js.replace('const CREATORS_DATA = [', fashionDataset + '\n  const CREATORS_DATA = [');
}

// Atualizar seletor contextual em initCarousel
const oldInitCarouselRegex = /function initCarousel\(\)\s*\{[\s\S]*?const totalCardsCount = 39;/;
const newInitCarousel = `function initCarousel() {
    const targetContainer = document.getElementById('creators-section');
    if (!targetContainer) return;

    // Detecta contexto do produto
    let activeDataset = CREATORS_DATA;
    const pageText = (document.title + ' ' + (document.querySelector('h1')?.textContent || '')).toLowerCase();
    const url = window.location.pathname.toLowerCase();

    if (url.includes('produto-104') || pageText.includes('chinelo') || pageText.includes('sandália') || pageText.includes('luxo') || pageText.includes('vestido') || pageText.includes('feminino')) {
      activeDataset = CREATORS_FASHION;
    } else if (url.includes('produto-101') || pageText.includes('pneu') || pageText.includes('pirelli')) {
      activeDataset = CREATORS_DATA;
    } else {
      activeDataset = CREATORS_FASHION;
    }

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
        item.commentsList.push(generateRandomComment(j + i * 2));
      }

      videoList.push(item);

      // Card com preview do vídeo real
      const cardHtml = \`
        <div class="creator-card" data-video-id="\${videoId}" style="position:relative; flex: 0 0 92px; height: 150px; border-radius: 8px; overflow: hidden; background: #161823; cursor: pointer;">
          <img src="\${item.poster}" alt="\${item.name}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 40%, rgba(0,0,0,0.75) 100%);"></div>
          <div class="creator-card-play-btn" style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2;">
            <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div class="creator-card-info" style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 6px; display: flex; align-items: center; gap: 5px; z-index: 2; box-sizing: border-box;">
            <img class="creator-card-avatar" src="\${item.avatar}" alt="\${item.name}" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;" onerror="this.src='https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/085171b8ffe0c64bcc1fce3ce127b415~tplv-tiktokx-cropcenter:100:100.jpg'">
            <span class="creator-card-name" style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">\${item.name}</span>
          </div>
        </div>
      \`;
      listElement.insertAdjacentHTML('beforeend', cardHtml);
    }`;

if (oldInitCarouselRegex.test(js)) {
  js = js.replace(oldInitCarouselRegex, newInitCarousel);
  console.log('✅ initCarousel atualizado com suporte contextual e thumbnails de alta fidelidade!');
}

fs.writeFileSync(jsPath, js, 'utf8');

// 2. INJETAR A SEÇÃO "Vídeos de criadores" EM pages/produto-104.html (PRODUTO PRINCIPAL)
const p104Path = path.join(__dirname, 'pages', 'produto-104.html');
let p104 = fs.readFileSync(p104Path, 'utf8');

if (!p104.includes('id="creators-section"')) {
  // Inserir antes de <!-- AVALIAÇÕES -->
  const reviewsAnchor = '<!-- AVALIAÇÕES -->';
  const creatorsBlock = `<!-- VÍDEOS DE CRIADORES OFICIAL TIKTOK SHOP -->
      <div id="creators-section" class="creators-section"></div>\n\n      `;
  
  if (p104.includes(reviewsAnchor)) {
    p104 = p104.replace(reviewsAnchor, creatorsBlock + reviewsAnchor);
  } else {
    // fallback antes de reviews-section
    p104 = p104.replace('<div class="reviews-section"', creatorsBlock + '<div class="reviews-section"');
  }

  // Inserir script antes de </body> se não tiver
  if (!p104.includes('videos-criadores.js')) {
    p104 = p104.replace('</body>', '  <script src="../js/videos-criadores.js"></script>\n</body>');
  }

  fs.writeFileSync(p104Path, p104, 'utf8');
  console.log('✅ produto-104.html recebeu a seção de Vídeos de Criadores oficial!');
}

// 3. INJETAR EM TODAS AS OUTRAS PÁGINAS DE PRODUTO QUE ESTAVAM SEM
const pagesDir = path.join(__dirname, 'pages');
const allPages = fs.readdirSync(pagesDir).filter(f => f.startsWith('produto-') && f.endsWith('.html'));

let batchCount = 0;
allPages.forEach(file => {
  const pPath = path.join(pagesDir, file);
  let content = fs.readFileSync(pPath, 'utf8');
  let modified = false;

  if (!content.includes('id="creators-section"')) {
    const creatorsBlock = `<!-- VÍDEOS DE CRIADORES -->\n      <div id="creators-section" class="creators-section"></div>\n\n      `;
    if (content.includes('<!-- AVALIAÇÕES -->')) {
      content = content.replace('<!-- AVALIAÇÕES -->', creatorsBlock + '<!-- AVALIAÇÕES -->');
      modified = true;
    } else if (content.includes('class="reviews-section"')) {
      content = content.replace(/<div[^>]*class="[^"]*reviews-section[^"]*"/, creatorsBlock + '$&');
      modified = true;
    }
  }

  if (!content.includes('videos-criadores.js')) {
    content = content.replace('</body>', '  <script src="../js/videos-criadores.js"></script>\n</body>');
    modified = true;
  }

  if (modified) {
    fs.writeFileSync(pPath, content, 'utf8');
    batchCount++;
  }
});

console.log(`✅ Sucesso: ${batchCount} páginas receberam a seção "Vídeos de criadores"!`);

// Sincronizar com ds/
const ds104 = path.join('C:', 'Users', 'Dell', 'Downloads', 'ds', 'produto-chinelo-tiktok.html');
if (fs.existsSync(ds104)) {
  fs.writeFileSync(ds104, p104, 'utf8');
  console.log('✅ ds/produto-chinelo-tiktok.html sincronizado!');
}
const dsJs = path.join('C:', 'Users', 'Dell', 'Downloads', 'ds', 'js', 'videos-criadores.js');
if (fs.existsSync(dsJs)) {
  fs.writeFileSync(dsJs, js, 'utf8');
  console.log('✅ ds/js/videos-criadores.js sincronizado!');
}
