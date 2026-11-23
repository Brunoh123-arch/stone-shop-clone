# Script para implementar renderRelacionados com vídeo real de criador, badge 11.11, miniatura de variação e dados idênticos aos prints
with open('js/app.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

idx_start = js_content.find('// ===== PRODUTOS RELACIONADOS DINÂMICOS')
if idx_start == -1:
    idx_start = js_content.find('function renderRelacionados() {')

idx_end = js_content.find('// ===== ABAS DE NAVEGAÇÃO DO PRODUTO =====', idx_start)
if idx_end == -1:
    idx_end = js_content.find('function initProductTabs() {', idx_start)

new_render_relacionados = """// ===== PRODUTOS RELACIONADOS DINÂMICOS — MASONRY CASCATA REAL COM VÍDEO E DADOS 1:1 TIKTOK SHOP =====
function renderRelacionados() {
  const grid = document.querySelector('.related-grid');
  if (!grid) return;
  if (typeof CATALOGO_PRODUTOS === 'undefined') return;

  const idAtual = typeof PRODUTO_ATUAL !== 'undefined' ? PRODUTO_ATUAL.id : -1;
  const isPagesDir = typeof window !== 'undefined' && window.location.pathname.includes('/pages/');
  const pathPrefix = isPagesDir ? '../' : '';

  // Determina se a página atual é de moda/calçado feminino (ex: 104 chinelo, 103 vestido, 106 cinta, etc.)
  const prodNome = (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL.nome) ? PRODUTO_ATUAL.nome.toLowerCase() : '';
  const isModaFeminina = prodNome.includes('chinelo') || prodNome.includes('sandália') || prodNome.includes('vestido') || prodNome.includes('cinta') || idAtual === 104 || idAtual === 103;

  // Catálogo de produtos para a grade de recomendados
  const outros = CATALOGO_PRODUTOS.filter(p => p.id !== idAtual);

  // Pool de criadores reais oficiais com avatares e nomes
  const CREATOR_VIDEOS = [
    {
      video: pathPrefix + 'img/video-chinelo-caramelo-mao.mp4',
      poster: pathPrefix + 'img/poster-chinelo-caramelo-mao.jpg',
      name: 'Vanessa e Edgar creator',
      avatar: pathPrefix + 'img/reviews-avatars/review-user-1.jpg',
      duracao: '00:32',
      hasThumbVar: true,
      thumbVar: pathPrefix + 'img/poster-chinelo-branco-pe.jpg',
      title: 'Chinelo Feminino Luxo Strass Brilhante Conforto',
      preco: '14,90',
      precoOrig: '59,90',
      badgeTipo: 'off_frete',
      descOff: '60% OFF',
      rating: '4,8',
      vendidos: '23.8K vendidos'
    },
    {
      video: null,
      img: pathPrefix + 'img/poster-chinelo-caramelo-pe.jpg',
      title: 'Chinelo Feminino No St...',
      preco: '11,98',
      precoOrig: '49,90',
      badgeTipo: 'off_frete',
      descOff: '60% OFF',
      rating: '4,8',
      vendidos: '1311 vendidos'
    },
    {
      video: null,
      is1111: true,
      img: pathPrefix + 'img/poster-chinelo-branco-pe.jpg',
      title: 'Sandalia Feminina Chinelo Rasteirinha Lux...',
      preco: '13,72',
      precoOrig: '69,80',
      badgeTipo: 'off_frete',
      descOff: '60% OFF',
      rating: '4,7',
      vendidos: '6599 vendidos'
    },
    {
      video: null,
      img: pathPrefix + 'img/frame_chinelo.jpg',
      title: 'Chinelo femino nó stras...',
      preco: '19,85',
      precoOrig: '69,90',
      badgeTipo: 'relampago',
      rating: '4,7',
      vendidos: '11.2K vendidos on-line'
    },
    {
      video: pathPrefix + 'img/video-chinelo-branco-pe.mp4',
      poster: pathPrefix + 'img/poster-chinelo-branco-pe.jpg',
      name: 'Duda Campos',
      avatar: pathPrefix + 'img/reviews-avatars/review-user-10.jpg',
      duracao: '00:20',
      title: 'Chinelo feminino LUXO...',
      preco: '19,53',
      precoOrig: '59,90',
      badgeTipo: 'off_frete',
      descOff: '60% OFF',
      rating: '4,7',
      vendidos: '10.7K vendidos'
    },
    {
      video: pathPrefix + 'img/video-chinelo-unboxing.mp4',
      poster: pathPrefix + 'img/frame_chinelo_6s.jpg',
      name: 'Kethellen Jade | Creator',
      avatar: pathPrefix + 'img/reviews-avatars/review-user-104-c10.jpg',
      duracao: '00:40',
      title: 'Sandália Rasteira Brilho Pedraria Blogueira',
      preco: '18,90',
      precoOrig: '59,90',
      badgeTipo: 'off_frete',
      descOff: '68% OFF',
      rating: '4,9',
      vendidos: '15.4K vendidos'
    }
  ];

  // Monta a lista completa de cards para o Masonry (mistura os itens destacados com produtos do catálogo)
  const cardsData = [];

  // Se for chinelo ou moda, começa com o pool oficial 1:1 idêntico ao print
  if (isModaFeminina) {
    cardsData.push(...CREATOR_VIDEOS);
    // Adiciona outros produtos do catálogo para scroll longo
    outros.slice(0, 10).forEach((p, idx) => {
      cardsData.push({
        id: p.id,
        video: null,
        img: p.img,
        title: p.nome,
        preco: parseFloat(p.preco).toFixed(2).replace('.', ','),
        precoOrig: p.precoOrig ? p.precoOrig : (parseFloat(p.preco) * 2.5).toFixed(2).replace('.', ','),
        is1111: (idx % 4 === 1),
        badgeTipo: (idx % 3 === 0) ? 'relampago' : 'off_frete',
        descOff: (p.desc || 55) + '% OFF',
        rating: (4.6 + ((p.id * 3) % 4) * 0.1).toFixed(1).replace('.', ','),
        vendidos: (5 + ((p.id * 7) % 20) * 0.8).toFixed(1) + 'K vendidos'
      });
    });
  } else {
    // Para outros nichos (eletrônicos, casa, etc.), usa produtos do catálogo com vídeo do nicho
    let techVideo = pathPrefix + 'img/video-projetor-1.mp4';
    if (idAtual === 105) techVideo = pathPrefix + 'videosprodutos/video-produto-108.mp4';

    cardsData.push({
      video: techVideo,
      poster: pathPrefix + 'img/poster-projetor-1.jpg',
      name: 'Lucas Tech Reviews',
      avatar: pathPrefix + 'img/reviews-avatars/review-user-1.jpg',
      duracao: '00:32',
      hasThumbVar: true,
      thumbVar: outros[0] ? outros[0].img : '',
      title: outros[0] ? outros[0].nome : 'Produto em Destaque',
      preco: outros[0] ? parseFloat(outros[0].preco).toFixed(2).replace('.', ',') : '39,90',
      precoOrig: '199,90',
      is1111: true,
      badgeTipo: 'off_frete',
      descOff: '70% OFF',
      rating: '4,9',
      vendidos: '18.2K vendidos'
    });

    outros.slice(0, 15).forEach((p, idx) => {
      cardsData.push({
        id: p.id,
        video: (idx === 4 ? pathPrefix + 'videosprodutos/video-produto-107.mp4' : null),
        poster: (idx === 4 ? pathPrefix + 'img/poster-aspirador-1.jpg' : null),
        name: (idx === 4 ? 'Bia Resenhas' : null),
        avatar: (idx === 4 ? pathPrefix + 'img/reviews-avatars/review-user-10.jpg' : null),
        duracao: (idx === 4 ? '00:24' : null),
        img: p.img,
        title: p.nome,
        preco: parseFloat(p.preco).toFixed(2).replace('.', ','),
        precoOrig: p.precoOrig ? p.precoOrig : (parseFloat(p.preco) * 2.6).toFixed(2).replace('.', ','),
        is1111: (idx % 3 === 0),
        badgeTipo: (idx % 4 === 1) ? 'relampago' : 'off_frete',
        descOff: (p.desc || 60) + '% OFF',
        rating: (4.6 + ((p.id * 3) % 4) * 0.1).toFixed(1).replace('.', ','),
        vendidos: (6 + ((p.id * 9) % 22) * 0.8).toFixed(1) + 'K vendidos'
      });
    });
  }

  // Proporções verticais variadas para descompassar a altura e criar o Masonry
  const ASPECT_RATIOS = ['3 / 4', '4 / 5', '1 / 1', '4 / 5', '3 / 4', '4 / 5', '1 / 1', '3 / 4'];

  function buildCardHtml(item, idx) {
    const ratio = item.video ? '3 / 4' : ASPECT_RATIOS[idx % ASPECT_RATIOS.length];
    const linkHref = item.id ? `produto-${item.id}.html` : 'produto-104.html';
    
    const parts = (item.preco || '19,90').split(',');
    const precoInt = parts[0];
    const precoCent = parts[1] || '00';

    // Badge 11.11 idêntico ao print oficial
    const badge1111Html = item.is1111 ? `
      <span class="badge-1111" style="background:linear-gradient(135deg, #ff004f, #fe2c55); color:#fff; font-size:9.5px; font-weight:800; padding:1px 4.5px; border-radius:3px; margin-right:4px; vertical-align:middle; display:inline-block; line-height:1.2; letter-spacing:-0.2px;">11.11</span>
    ` : '';

    // Badges de desconto ou oferta relâmpago
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
        <!-- Mídia do Card: Vídeo Real com Autoplay Silencioso ou Imagem Vertical -->
        <div class="related-img-wrapper" style="position:relative; width:100%; aspect-ratio:${ratio}; overflow:hidden; background:#f0f0f0;">
          ${item.video ? `
            <video class="related-card-video" src="${item.video}" poster="${item.poster || ''}" autoplay muted loop playsinline style="width:100%; height:100%; object-fit:cover; display:block;"></video>
            <!-- Badge de Tempo de Vídeo TikTok Shop -->
            <div style="position:absolute; top:7px; left:7px; background:rgba(0,0,0,0.45); color:#fff; font-size:9.5px; font-weight:700; padding:2px 6px; border-radius:3px; display:flex; align-items:center; gap:3px; z-index:2; backdrop-filter:blur(2px);">
              <span style="font-size:7.5px; letter-spacing:-1px;">❚❚</span> ${item.duracao || '00:32'}
            </div>
            <!-- Tag do Criador Real no Rodapé da Mídia -->
            <div style="position:absolute; bottom:6px; left:7px; right:7px; display:flex; align-items:center; gap:5px; color:#fff; font-size:11px; font-weight:500; text-shadow:0 1px 2px rgba(0,0,0,0.9); z-index:2; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
              <img src="${item.avatar || (pathPrefix + 'img/reviews-avatars/review-user-1.jpg')}" style="width:18px; height:18px; border-radius:50%; object-fit:cover; border:1px solid rgba(255,255,255,0.7); flex-shrink:0;">
              <span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${item.name || 'Criador TikTok'}</span>
            </div>
            <div style="position:absolute; bottom:0; left:0; right:0; height:36px; background:linear-gradient(to top, rgba(0,0,0,0.55), transparent); pointer-events:none;"></div>
          ` : `
            <img class="related-img" src="${item.img}" alt="${item.title}" loading="lazy" onerror="this.src='../logo.png'" style="width:100%; height:100%; object-fit:cover; display:block;">
          `}
        </div>

        <!-- Informações do Produto (Ordem e Tipografia 1:1 com os Prints Oficiais) -->
        <div class="related-info" style="padding:8px 8px 10px 8px; display:flex; flex-direction:column; flex:1; box-sizing:border-box;">
          <!-- Linha 1: Título com miniatura de variação à direita (quando houver) -->
          <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:4px; margin-bottom:3px;">
            <div class="related-name" style="flex:1; font-size:12.5px; font-weight:400; color:#161823; line-height:1.35; max-height:2.7em; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; text-overflow:ellipsis;">
              ${badge1111Html}${item.title}
            </div>
            ${item.hasThumbVar ? `
              <img src="${item.thumbVar}" alt="Variação" style="width:28px; height:28px; border-radius:4px; object-fit:cover; flex-shrink:0; border:1px solid #f0f0f0;">
            ` : ''}
          </div>

          <!-- Linha 2: Preço Promocional em Vermelho Grande + Original Riscado -->
          <div class="related-price-row" style="display:flex; align-items:baseline; gap:3px; margin-top:2px; margin-bottom:3px;">
            <span style="font-size:11px; font-weight:700; color:#fe2c55; margin-right:1px;">R$</span>
            <span style="font-size:16px; font-weight:700; color:#fe2c55; line-height:1;">${precoInt}</span><span style="font-size:12.5px; font-weight:700; color:#fe2c55; line-height:1;">,${precoCent}</span>
            <span style="font-size:11px; color:#8a8b91; text-decoration:line-through; font-weight:400; margin-left:3px;">R$ ${item.precoOrig}</span>
          </div>

          <!-- Linha 3: Badges de Oferta / Frete Grátis -->
          <div class="card-badges-row" style="display:flex; align-items:center; gap:4px; flex-wrap:wrap; margin-bottom:4px;">
            ${badgesHtml}
          </div>

          <!-- Linha 4: Avaliação e Quantidade de Vendidos -->
          <div class="card-rating-row" style="display:flex; align-items:center; gap:3px; font-size:11px; color:#8a8b91; margin-top:auto;">
            <span style="color:#ffb800; font-size:11px; line-height:1;">★</span>
            <span style="color:#161823; font-weight:600; font-size:11.5px;">${item.rating}</span>
            <span style="color:#d8d8d8; margin:0 2px;">|</span>
            <span style="color:#8a8b91; font-size:11px;">${item.vendidos}</span>
          </div>
        </div>
      </a>`;
  }

  // Cria as 2 colunas independentes para formar a Cascata Real (Masonry)
  const colLeft = document.createElement('div');
  const colRight = document.createElement('div');
  colLeft.className = 'related-col';
  colRight.className = 'related-col';
  colLeft.style.cssText = 'flex:1; min-width:0; display:flex; flex-direction:column; gap:8px;';
  colRight.style.cssText = 'flex:1; min-width:0; display:flex; flex-direction:column; gap:8px;';

  // Distribui alternadamente entre coluna esquerda e direita
  cardsData.forEach((item, i) => {
    const html = buildCardHtml(item, i);
    const col = (i % 2 === 0) ? colLeft : colRight;
    col.insertAdjacentHTML('beforeend', html);
  });

  // Configura o grid pai
  grid.style.cssText = 'display:flex; align-items:flex-start; gap:8px; padding:0 8px 24px 8px; width:100%; box-sizing:border-box; background:#f5f5f5;';
  grid.innerHTML = '';
  grid.appendChild(colLeft);
  grid.appendChild(colRight);

  // Garante que a seção e o título tenham o fundo e tipografia oficiais
  const sec = grid.closest('.related-section');
  if (sec) {
    sec.style.cssText = 'background:#f5f5f5; padding-top:4px; border-top:8px solid #f5f5f5; margin-top:10px; width:100%; box-sizing:border-box;';
    const title = sec.querySelector('.related-title');
    if (title) {
      title.style.cssText = 'font-size:15.5px; font-weight:700; color:#161823; padding:12px 10px 8px 10px; margin:0; letter-spacing:-0.2px; background:#f5f5f5;';
    }
  }

  // Garante autoplay nos vídeos mesmo em navegadores mobile rigorosos com baixo consumo
  setTimeout(() => {
    document.querySelectorAll('.related-card-video').forEach(v => {
      v.muted = true;
      v.play().catch(() => {});
    });
  }, 300);
}
"""

js_content = js_content[:idx_start] + new_render_relacionados + js_content[idx_end:]

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("SUCCESS: Updated renderRelacionados with 1:1 real video, 11.11 badge and creators!")
