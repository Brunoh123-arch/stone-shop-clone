import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Substituir renderRelacionados por uma versão unificada e perfeita
old_fn_start = code.find('function renderRelacionados() {')
if old_fn_start == -1:
    print("ERRO: renderRelacionados não encontrado!")
    exit(1)

# Encontrar o final da função renderRelacionados
# Vamos procurar onde a função termina antes da próxima função
old_fn_end = code.find('function initCarrinhoPage()', old_fn_start)
if old_fn_end == -1:
    old_fn_end = code.find('// === INICIALIZAÇÃO GERAL ===', old_fn_start)

print(f"Substituindo de {old_fn_start} até {old_fn_end}")

new_render_relacionados = """function renderRelacionados() {
  const grid = document.querySelector('.related-grid');
  if (!grid) return;
  if (typeof CATALOGO_PRODUTOS === 'undefined') return;

  const idAtual = typeof PRODUTO_ATUAL !== 'undefined' ? Number(PRODUTO_ATUAL.id) : -1;
  const isPagesDir = typeof window !== 'undefined' && window.location.pathname.includes('/pages/');
  const pathPrefix = isPagesDir ? '../' : '';

  function fixPath(src) {
    if (!src) return pathPrefix + 'logo.png';
    if (src.startsWith('http://') || src.startsWith('https://')) return src;
    if (isPagesDir) {
      if (src.startsWith('../')) return src;
      return '../' + src.replace(/^\\.?\\//, '');
    } else {
      return src.replace(/^\\.\\.\\//, '');
    }
  }

  // Mapa rigoroso de vídeos 1:1 por ID do produto
  const PRODUTO_VIDEOS_MAP = {
    104: {
      video: 'https://files.catbox.moe/tsjc1l.mp4',
      poster: fixPath('img/poster-chinelo-real-1.jpg'),
      name: 'Kethellen Jade',
      avatar: fixPath('img/reviews-avatars/review-user-104-c10.jpg'),
      duracao: '00:40'
    },
    106: {
      video: 'https://files.catbox.moe/jpmxf4.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-106.jpg'),
      name: 'Giulia Ferreira',
      avatar: fixPath('img/reviews-avatars/review-user-1.jpg'),
      duracao: '00:28'
    },
    107: {
      video: 'https://files.catbox.moe/nwhxcm.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-107.jpg'),
      name: 'Bia Resenhas',
      avatar: fixPath('img/reviews-avatars/review-user-10.jpg'),
      duracao: '00:24'
    },
    108: {
      video: 'https://files.catbox.moe/e7z9vc.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-108.jpg'),
      name: 'Camila Resenhas',
      avatar: fixPath('img/reviews-avatars/review-user-2.jpg'),
      duracao: '00:32'
    },
    109: {
      video: 'https://files.catbox.moe/bjcwqr.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-109.jpg'),
      name: 'Lorena Cachos',
      avatar: fixPath('img/reviews-avatars/review-user-3.jpg'),
      duracao: '00:35'
    },
    110: {
      video: 'https://files.catbox.moe/2t30kf.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-110.jpg'),
      name: 'Lucas Running',
      avatar: fixPath('img/reviews-avatars/review-user-103-c3.jpg'),
      duracao: '00:28'
    },
    111: {
      video: 'https://files.catbox.moe/facj5t.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-111.jpg'),
      name: 'Decorações & Dicas',
      avatar: fixPath('img/reviews-avatars/review-user-111-de.jpg'),
      duracao: '00:25'
    },
    112: {
      video: 'https://files.catbox.moe/geut5n.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-112.jpg'),
      name: 'Brinquedos Kids',
      avatar: fixPath('img/reviews-avatars/review-user-112-c1.jpg'),
      duracao: '00:20'
    },
    113: {
      video: 'https://files.catbox.moe/grwbds.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-113.jpg'),
      name: 'Pets & Dicas',
      avatar: fixPath('img/reviews-avatars/review-user-4.jpg'),
      duracao: '00:25'
    },
    114: {
      video: 'https://files.catbox.moe/cfm2lc.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-114.jpg'),
      name: 'Gamer Retro TV',
      avatar: fixPath('img/reviews-avatars/review-user-114-c2.jpg'),
      duracao: '00:30'
    }
  };

  const outros = CATALOGO_PRODUTOS.filter(p => Number(p.id) !== idAtual);
  const cardsData = [];

  // Exatamente 2 cards de vídeo no feed inteiro, bem espaçados
  let videoSlotsCount = 0;
  const maxVideoSlots = 2;

  outros.slice(0, 16).forEach((p, idx) => {
    const pPrecoNum = typeof p.preco === 'number' ? p.preco : parseFloat(String(p.preco).replace(',', '.')) || 39.90;
    const pPreco = pPrecoNum.toFixed(2).replace('.', ',');
    const pPrecoOrig = p.precoOrig ? String(p.precoOrig) : (pPrecoNum * 2.5).toFixed(2).replace('.', ',');
    const pVendidos = p.vendidos 
      ? (typeof p.vendidos === 'number' && p.vendidos >= 1000 ? (p.vendidos / 1000).toFixed(1) + 'K vendidos' : p.vendidos + ' vendidos')
      : (5 + ((p.id * 7) % 18) * 0.8).toFixed(1) + 'K vendidos';

    const vInfo = PRODUTO_VIDEOS_MAP[p.id];
    // Ativa vídeo estritamente em apenas 2 posições espaçadas (1º no card 1 e 2º no card 5 ou 6)
    const isTargetSlot = (videoSlotsCount === 0 && (idx === 1 || idx === 0)) || (videoSlotsCount === 1 && (idx === 4 || idx === 5 || idx === 6));
    const shouldHaveVideo = vInfo && videoSlotsCount < maxVideoSlots && isTargetSlot;
    
    let itemVideo = null;
    let itemPoster = null;
    let itemCreatorName = null;
    let itemCreatorAvatar = null;
    let itemDuracao = null;

    if (shouldHaveVideo) {
      itemVideo = vInfo.video;
      itemPoster = vInfo.poster;
      itemCreatorName = vInfo.name;
      itemCreatorAvatar = vInfo.avatar;
      itemDuracao = vInfo.duracao;
      videoSlotsCount++;
    }

    cardsData.push({
      id: p.id,
      video: itemVideo,
      poster: itemPoster,
      name: itemCreatorName,
      avatar: itemCreatorAvatar,
      duracao: itemDuracao,
      img: fixPath(p.img),
      title: p.nome,
      preco: pPreco,
      precoOrig: pPrecoOrig,
      is1111: (idx % 3 === 0),
      badgeTipo: (idx % 4 === 1) ? 'relampago' : 'off_frete',
      descOff: (p.desc || 60) + '% OFF',
      rating: (4.7 + ((p.id * 3) % 3) * 0.1).toFixed(1).replace('.', ','),
      vendidos: pVendidos
    });
  });

  // Proporções verticais para o Masonry
  const ASPECT_RATIOS = ['3 / 4', '4 / 5', '1 / 1', '4 / 5', '3 / 4', '4 / 5', '1 / 1', '3 / 4'];

  function buildCardHtml(item, idx) {
    const ratio = item.video ? '3 / 4' : ASPECT_RATIOS[idx % ASPECT_RATIOS.length];
    const linkHref = isPagesDir ? `produto-${item.id}.html` : `pages/produto-${item.id}.html`;
    
    const parts = (item.preco || '19,90').split(',');
    const precoInt = parts[0];
    const precoCent = parts[1] || '00';

    const badge1111Html = item.is1111 ? `
      <span class="badge-1111" style="background:linear-gradient(135deg, #ff004f, #fe2c55); color:#fff; font-size:9.5px; font-weight:800; padding:1px 4.5px; border-radius:3px; margin-right:4px; vertical-align:middle; display:inline-block; line-height:1.2; letter-spacing:-0.2px;">11.11</span>
    ` : '';

    let badgesHtml = '';
    if (item.badgeTipo === 'relampago') {
      badgesHtml = `
        <span style="background:#fff2e8; color:#ff5722; font-size:10px; font-weight:700; padding:1.5px 5px; border-radius:2px; display:inline-flex; align-items:center; gap:2.5px;">
          <svg width="9" height="9" viewBox="0 0 24 24" fill="currentColor"><path d="M13 2L3 14h8l-1 8 11-12h-8l1-8z"/></svg> Oferta Relâmpago
        </span>
      `;
    } else {
      badgesHtml = `
        <span style="background:#fff0f3; color:#fe2c55; font-size:10px; font-weight:700; padding:1.5px 5px; border-radius:2px; display:inline-flex; align-items:center; gap:2px;">
          <svg width="8" height="8" viewBox="0 0 24 24" fill="currentColor"><path d="M12.7 2.3c-.4-.4-1-.4-1.4 0l-9 9c-.4.4-.4 1 0 1.4l9 9c.4.4 1 .4 1.4 0l9-9c.4-.4.4-1 0-1.4l-9-9z"/></svg> ${item.descOff || '60% OFF'}
        </span>
        <span style="background:#e8f7f5; color:#00a699; font-size:10px; font-weight:600; padding:1.5px 5px; border-radius:2px;">Frete grátis</span>
      `;
    }

    return `
      <a class="related-card" href="${linkHref}" style="background:#fff; border-radius:8px; overflow:hidden; border:none; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-decoration:none; color:inherit; display:flex; flex-direction:column; width:100%; box-sizing:border-box; position:relative; margin-bottom:8px;">
        <div class="related-img-wrapper" style="position:relative; width:100%; aspect-ratio:${ratio}; overflow:hidden; background:#000;">
          ${item.video ? `
            <video class="related-card-video" src="${item.video}" poster="${item.poster || ''}" autoplay muted loop playsinline style="width:100%; height:100%; object-fit:cover; display:block;"></video>
            <div style="position:absolute; top:6px; left:6px; background:rgba(0,0,0,0.55); color:#fff; font-size:9.5px; font-weight:600; padding:2px 5.5px; border-radius:3px; display:flex; align-items:center; gap:3px; backdrop-filter:blur(3px);">
              <svg width="8" height="8" viewBox="0 0 24 24" fill="#fff"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              <span>${item.duracao || '00:30'}</span>
            </div>
            <div style="position:absolute; bottom:6px; left:6px; display:flex; align-items:center; gap:5px; z-index:2;">
              <img src="${item.avatar}" style="width:18px; height:18px; border-radius:50%; object-fit:cover; border:1px solid #fff;" alt="">
              <span style="color:#fff; font-size:10.5px; font-weight:600; text-shadow:0 1px 3px rgba(0,0,0,0.8);">${item.name}</span>
            </div>
          ` : `
            <img src="${item.img}" alt="${item.title}" loading="lazy" style="width:100%; height:100%; object-fit:cover; display:block;">
          `}
        </div>
        <div class="related-card-info" style="padding:7px 8px 10px; display:flex; flex-direction:column; gap:4px; flex:1;">
          <h4 class="related-card-title" style="font-size:12px; font-weight:400; line-height:1.35; color:#161823; margin:0; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
            ${badge1111Html}${item.title}
          </h4>
          <div style="display:flex; align-items:baseline; gap:4px; margin-top:2px;">
            <div style="color:#fe2c55; font-size:11px; font-weight:700;">
              R$ <span style="font-size:15px; font-weight:800;">${precoInt}</span><span style="font-size:11px; font-weight:700;">,${precoCent}</span>
            </div>
            <span style="color:#8a8b91; font-size:10px; text-decoration:line-through;">R$ ${item.precoOrig}</span>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:3px; margin-top:1px;">
            ${badgesHtml}
          </div>
          <div style="display:flex; align-items:center; gap:4px; margin-top:2px; font-size:10px; color:#73747b;">
            <span style="color:#ff8c00; font-weight:700; display:inline-flex; align-items:center; gap:1.5px;">
              ★ ${item.rating}
            </span>
            <span>|</span>
            <span>${item.vendidos}</span>
          </div>
        </div>
      </a>
    `;
  }

  // Divisão balanceada em 2 colunas para efeito Masonry fluido
  const colLeft = [];
  const colRight = [];

  cardsData.forEach((item, i) => {
    if (i % 2 === 0) {
      colLeft.push(buildCardHtml(item, i));
    } else {
      colRight.push(buildCardHtml(item, i));
    }
  });

  grid.innerHTML = `
    <div class="masonry-column" style="display:flex; flex-direction:column; flex:1; min-width:0;">
      ${colLeft.join('')}
    </div>
    <div class="masonry-column" style="display:flex; flex-direction:column; flex:1; min-width:0;">
      ${colRight.join('')}
    </div>
  `;
}
"""

new_code = code[:old_fn_start] + new_render_relacionados + '\n\n' + code[old_fn_end:]
with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("✅ js/app.js atualizado com sucesso!")
