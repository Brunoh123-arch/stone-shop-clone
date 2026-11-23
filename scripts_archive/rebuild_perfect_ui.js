const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

console.log('>>> [BRUNO CTO] RECONSTRUÇÃO CANÔNICA DA UI OFICIAL TIKTOK SHOP <<<');

// =========================================================================
// 1. REPARAR O TOPO DA PÁGINA (HEADER FIXO NÃO PODE COBRIR A LOJA)
// =========================================================================
// Garantir que o container principal tenha margin-top adequada para o header fixo (48px)
html = html.replace(/<div id="root"[^>]*>/i, '<div id="root" style="max-width: 480px; margin: 0 auto; min-height: 100vh; background: #f8f8f8; padding-top: 50px;">');

// =========================================================================
// 2. PARSEAR E REESTRUTURAR TODOS OS 87 CARDS DO RECOMMENDED-GRID
// =========================================================================
const rStart = html.indexOf('id="recommended-grid"');
const catStart = html.indexOf('id="categorias-section"');

if (rStart === -1 || catStart === -1) {
  console.error('❌ Não encontrou recommended-grid ou categorias-section');
  process.exit(1);
}

const beforeGrid = html.slice(0, rStart);
const afterGrid = html.slice(catStart);
const gridSection = html.slice(rStart, catStart);

// Pegar a tag de abertura de recommended-grid
const gridOpenTagMatch = gridSection.match(/<div[^>]*id="recommended-grid"[^>]*>/i);
const gridOpenTag = gridOpenTagMatch ? gridOpenTagMatch[0] : '<div id="recommended-grid">';

const cardMatches = [...gridSection.matchAll(/<a class="product-card-rec"([\s\S]*?)<\/a>/g)];
console.log(`Parseando ${cardMatches.length} cards...`);

const cleanCards = cardMatches.map((m, idx) => {
  const fullCard = m[0];
  
  // Extrair atributos do link
  const hrefM = fullCard.match(/href="([^"]+)"/);
  const href = hrefM ? hrefM[1] : 'pages/produto-104.html';
  
  const catM = fullCard.match(/data-cat="([^"]+)"/);
  const cat = catM ? catM[1] : 'Geral';
  
  const nomeM = fullCard.match(/data-nome="([^"]+)"/);
  const dataNome = nomeM ? nomeM[1] : '';

  // Imagem
  const imgM = fullCard.match(/<img[^>]+src="([^"]+)"/);
  const imgSrc = imgM ? imgM[1] : '';
  
  const altM = fullCard.match(/<img[^>]+alt="([^"]+)"/);
  const imgAlt = altM ? altM[1] : 'Produto';

  // Título
  const titleM = fullCard.match(/<h3[^>]*>([\s\S]*?)<\/h3>/);
  const title = titleM ? titleM[1].trim() : imgAlt;

  // Preço atual
  let priceCur = '19,90';
  const curM = fullCard.match(/class="current-price"[^>]*>[\s\S]*?<span class="currency">R\$<\/span>\s*([\d\.,]+)/i) ||
               fullCard.match(/class="current-price"[^>]*>([\s\S]*?)<\/span>/i);
  if (curM) {
    const raw = curM[1].replace(/<[^>]+>/g, '').replace('R$', '').trim();
    if (raw) priceCur = raw;
  }

  // Preço antigo
  let priceOld = 'R$ 59,90';
  const oldM = fullCard.match(/class="old-price"[^>]*>([\s\S]*?)<\/span>/i);
  if (oldM) {
    priceOld = oldM[1].replace(/<[^>]+>/g, '').trim();
    if (!priceOld.startsWith('R$')) priceOld = 'R$ ' + priceOld;
  }

  // Vendas
  let salesText = '1250 vendido(s)';
  let salesNum = 1250;
  const salesM = fullCard.match(/class="product-sales"[^>]*>([\s\S]*?)<\/div>/i);
  if (salesM) {
    salesText = salesM[1].replace(/<[^>]+>/g, '').trim();
    const numM = salesText.match(/([\d\.,]+)\s*k?/i);
    if (numM) {
      let n = parseFloat(numM[1].replace(',', '.'));
      if (salesText.toLowerCase().includes('k')) n *= 1000;
      salesNum = Math.round(n);
    }
  }

  // ID do produto
  const idM = href.match(/produto-(\d+)\.html/);
  const prodId = idM ? parseInt(idM[1], 10) : (100 - idx);

  // Avaliação simulada de acordo com o print oficial (ex: 4.7, 4.5, etc.)
  const rating = (4.5 + ((prodId * 7) % 5) / 10).toFixed(1);
  const hasRating = (prodId % 4 !== 0); // Alguns não têm rating, igual ao print!

  // Badge de desconto percentual da Home
  const discM = fullCard.match(/class="product-badge-discount"[^>]*>([\s\S]*?)<\/span>/i);
  const discHtml = discM ? discM[0] : '';

  return `<!-- PRODUTO ${prodId} -->
              <a class="product-card-rec" href="${href}" data-cat="${cat}" data-nome="${dataNome}" data-vendas="${salesNum}" data-id="${prodId}" style="text-decoration: none; color: inherit;">
                <div class="card-inner-box">
                  <img src="${imgSrc}" alt="${imgAlt}" loading="lazy" class="card-thumb-img">
                  <div class="card-details-col">
                    <div class="card-top-info">
                      <h3 class="product-name">${title}</h3>
                      <div class="card-badges-row">
                        ${discHtml ? `<div class="home-discount-badge">${discHtml}</div>` : ''}
                        <span class="badge-frete-gratis">Frete grátis</span>
                      </div>
                      ${hasRating ? `
                      <div class="card-rating-row">
                        <span class="star-yellow">★</span>
                        <span class="rating-num">${rating}</span>
                        <span class="rating-pipe">|</span>
                        <span class="sales-count-txt">${salesText}</span>
                      </div>` : ''}
                    </div>
                    <div class="card-bottom-action-row">
                      <div class="price-stack-col">
                        <div class="price-current-txt"><span class="currency">R$</span> ${priceCur}</div>
                        <div class="price-old-txt">${priceOld}</div>
                      </div>
                      <div class="unified-buy-btn" onclick="event.preventDefault(); event.stopPropagation(); window.location.href='${href}';">
                        <div class="btn-cart-part">
                          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#fe2c55" stroke-width="2">
                            <circle cx="9" cy="21" r="1"></circle>
                            <circle cx="20" cy="21" r="1"></circle>
                            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                          </svg>
                        </div>
                        <div class="btn-txt-part">
                          Comprar
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </a>`;
});

const rebuiltGridHtml = `${gridOpenTag}\n              ${cleanCards.join('\n              ')}\n            </div>\n\n          </div>\n\n          `;
html = beforeGrid + rebuiltGridHtml + afterGrid;
console.log('✅ Todos os 87 cards reconstruídos com estrutura canônica!');

// =========================================================================
// 3. CSS CANÔNICO DE ALTA FIDELIDADE (100% IDENTICO AOS PRINTS)
// =========================================================================
const perfectStyles = `
    /* ========================================================
       ESTILOS CANÔNICOS TIKTOK SHOP (BRUNO CTO MODO ZIKA)
       ======================================================== */
    /* Root container mobile */
    body {
      background-color: #f8f8f8;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }

    #root {
      max-width: 480px !important;
      margin: 0 auto !important;
      background: #f8f8f8 !important;
      padding-top: 52px !important;
      min-height: 100vh !important;
      box-shadow: 0 0 20px rgba(0,0,0,0.06);
    }

    /* Header fixo */
    .header {
      position: fixed !important;
      top: 0 !important;
      left: 50% !important;
      transform: translateX(-50%) !important;
      width: 100% !important;
      max-width: 480px !important;
      height: 52px !important;
      background: #fff !important;
      z-index: 9999 !important;
      border-bottom: 1px solid #f0f0f0 !important;
    }

    /* Store Section & Cupons */
    .store-section {
      background: #fff !important;
      padding: 14px 16px 8px 16px !important;
      margin-top: 0 !important;
    }

    .badge-loja-estrela {
      display: inline-flex !important;
      align-items: center !important;
      background: #faeed7 !important;
      color: #8c5b08 !important;
      font-size: 10.5px !important;
      font-weight: 600 !important;
      padding: 2px 6px !important;
      border-radius: 4px !important;
      line-height: 1.2 !important;
    }

    .coupons-container {
      background: #fff !important;
      padding: 0 16px 12px 16px !important;
    }

    .coupon-card-official {
      background: #eafbf7 !important;
      border: 1px solid #d4f4ed !important;
      border-radius: 8px !important;
      padding: 10px 14px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
    }

    .coupon-title {
      font-size: 13.5px !important;
      font-weight: 700 !important;
      color: #161823 !important;
      line-height: 1.2 !important;
    }

    .coupon-sub {
      font-size: 11px !important;
      color: #6b7280 !important;
      margin-top: 3px !important;
    }

    .coupon-resgatado-txt {
      font-size: 13px !important;
      font-weight: 600 !important;
      color: #20b5a6 !important;
    }

    /* Nav Tabs */
    .nav-tabs {
      background: #fff !important;
      display: flex !important;
      border-bottom: 1px solid #f0f0f0 !important;
      position: sticky !important;
      top: 52px !important;
      z-index: 100 !important;
    }

    .nav-tab {
      flex: 1 !important;
      height: 44px !important;
      background: transparent !important;
      border: none !important;
      font-size: 14px !important;
      color: #757575 !important;
      font-weight: 500 !important;
      cursor: pointer !important;
      position: relative !important;
    }

    .nav-tab.active {
      color: #161823 !important;
      font-weight: 700 !important;
    }

    .nav-tab.active::after {
      content: '' !important;
      position: absolute !important;
      bottom: 0 !important;
      left: 25% !important;
      width: 50% !important;
      height: 2.5px !important;
      background: #161823 !important;
      border-radius: 2px !important;
    }

    /* Sub-barra de ordenação da aba Produtos (Print 1) */
    .subfilter-produtos-bar {
      display: none;
      align-items: center;
      justify-content: space-between;
      padding: 10px 16px;
      background: #fff;
      border-bottom: 1px solid #f2f2f2;
      position: sticky;
      top: 96px;
      z-index: 90;
    }

    .subfilter-items {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .subfilter-item {
      font-size: 13px;
      color: #4b4d53;
      cursor: pointer;
      font-weight: 500;
    }

    .subfilter-item.active {
      color: #161823;
      font-weight: 700;
    }

    .subfilter-divider {
      color: #e5e5e5;
      font-size: 11px;
    }

    .subfilter-view-toggle {
      cursor: pointer;
      display: flex;
      align-items: center;
      color: #757575;
    }

    /* Badge Frete Grátis Oficial */
    .badge-frete-gratis {
      display: inline-flex !important;
      align-items: center !important;
      background: #e6f9f6 !important;
      color: #00a699 !important;
      font-size: 10.5px !important;
      font-weight: 700 !important;
      padding: 1.5px 5px !important;
      border-radius: 3px !important;
      line-height: 1.2 !important;
    }

    /* Divisor com degradê rosa oficial (Print 4) */
    .divider-home-rec {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      font-size: 13.5px;
      font-weight: 600;
      color: #161823;
      margin: 14px 0 16px 0;
      text-align: center;
    }

    .divider-home-rec::before {
      content: '';
      height: 1.5px;
      flex: 1;
      max-width: 40px;
      background: linear-gradient(to right, transparent, #fe2c55);
    }

    .divider-home-rec::after {
      content: '';
      height: 1.5px;
      flex: 1;
      max-width: 40px;
      background: linear-gradient(to left, transparent, #fe2c55);
    }

    /* Ocultar divisor na aba de produtos */
    .hide-home-divider .divider-home-rec {
      display: none !important;
    }

    /* ----------------------------------------------------
       MODO 1: GRADE DE 2 COLUNAS (PÁGINA INICIAL)
       ---------------------------------------------------- */
    #recommended-grid:not(.produtos-layout-list) {
      display: grid !important;
      grid-template-columns: repeat(2, 1fr) !important;
      gap: 8px !important;
      background: transparent !important;
      padding: 0 !important;
    }

    #recommended-grid:not(.produtos-layout-list) .product-card-rec {
      display: block !important;
      background: #fff !important;
      border: 1px solid #f0f0f0 !important;
      border-radius: 8px !important;
      overflow: hidden !important;
    }

    #recommended-grid:not(.produtos-layout-list) .card-inner-box {
      display: flex !important;
      flex-direction: column !important;
      height: 100% !important;
    }

    #recommended-grid:not(.produtos-layout-list) .card-thumb-img {
      width: 100% !important;
      aspect-ratio: 1 / 1 !important;
      object-fit: cover !important;
      display: block !important;
    }

    #recommended-grid:not(.produtos-layout-list) .card-details-col {
      padding: 8px !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      flex: 1 !important;
    }

    #recommended-grid:not(.produtos-layout-list) .product-name {
      font-size: 12px !important;
      font-weight: 500 !important;
      color: #333 !important;
      line-height: 1.35 !important;
      margin-top: 0 !important;
      margin-bottom: 6px !important;
      display: -webkit-box !important;
      -webkit-line-clamp: 2 !important;
      -webkit-box-orient: vertical !important;
      overflow: hidden !important;
      height: 32px !important;
    }

    #recommended-grid:not(.produtos-layout-list) .card-badges-row {
      display: flex !important;
      align-items: center !important;
      gap: 4px !important;
      margin-top: 4px !important;
      flex-wrap: wrap !important;
    }

    #recommended-grid:not(.produtos-layout-list) .home-discount-badge {
      display: inline-flex !important;
    }

    #recommended-grid:not(.produtos-layout-list) .card-rating-row {
      display: flex !important;
      align-items: center !important;
      gap: 3px !important;
      font-size: 11px !important;
      color: #8a8b91 !important;
      margin-top: 4px !important;
    }

    #recommended-grid:not(.produtos-layout-list) .card-bottom-action-row {
      margin-top: 6px !important;
    }

    #recommended-grid:not(.produtos-layout-list) .price-stack-col {
      display: flex !important;
      align-items: baseline !important;
      gap: 4px !important;
    }

    #recommended-grid:not(.produtos-layout-list) .price-current-txt {
      font-size: 15px !important;
      font-weight: 700 !important;
      color: #fe2c55 !important;
    }

    #recommended-grid:not(.produtos-layout-list) .price-old-txt {
      font-size: 11px !important;
      color: #8a8b91 !important;
      text-decoration: line-through !important;
    }

    #recommended-grid:not(.produtos-layout-list) .unified-buy-btn {
      display: none !important; /* OCULTO NO GRID DA HOME */
    }

    /* Não exibir botão de compra nos Principais Produtos da Home */
    #principais-produtos-section .unified-buy-btn {
      display: none !important;
    }

    /* ----------------------------------------------------
       MODO 2: LISTA EMPILHADA CANÔNICA (ABA PRODUTOS - PRINT 1)
       ---------------------------------------------------- */
    #recommended-grid.produtos-layout-list {
      display: flex !important;
      flex-direction: column !important;
      gap: 0 !important;
      background: #fff !important;
      padding: 0 !important;
    }

    #recommended-grid.produtos-layout-list .product-card-rec {
      display: block !important;
      background: #fff !important;
      border: none !important;
      border-radius: 0 !important;
      padding: 12px 16px !important;
      border-bottom: 1px solid #f5f5f5 !important;
      width: 100% !important;
      box-sizing: border-box !important;
    }

    #recommended-grid.produtos-layout-list .card-inner-box {
      display: flex !important;
      flex-direction: row !important;
      align-items: center !important;
      gap: 12px !important;
      width: 100% !important;
    }

    #recommended-grid.produtos-layout-list .card-thumb-img {
      width: 108px !important;
      height: 108px !important;
      min-width: 108px !important;
      max-width: 108px !important;
      aspect-ratio: 1 / 1 !important;
      object-fit: cover !important;
      border-radius: 8px !important;
      background: #f7f7f7 !important;
      flex-shrink: 0 !important;
    }

    #recommended-grid.produtos-layout-list .card-details-col {
      flex: 1 !important;
      min-width: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      height: 108px !important;
      padding: 2px 0 !important;
    }

    #recommended-grid.produtos-layout-list .product-name {
      font-size: 13.5px !important;
      font-weight: 500 !important;
      color: #161823 !important;
      line-height: 1.3 !important;
      margin: 0 0 4px 0 !important;
      display: -webkit-box !important;
      -webkit-line-clamp: 2 !important;
      -webkit-box-orient: vertical !important;
      overflow: hidden !important;
      height: auto !important;
      max-height: 35px !important;
    }

    #recommended-grid.produtos-layout-list .card-badges-row {
      display: flex !important;
      align-items: center !important;
      margin-bottom: 3px !important;
    }

    #recommended-grid.produtos-layout-list .home-discount-badge {
      display: none !important; /* OCULTA DESCONTO % VERMELHO NA LISTA DO PRINT */
    }

    #recommended-grid.produtos-layout-list .badge-frete-gratis {
      display: inline-flex !important;
      background: #e6f9f6 !important;
      color: #00a699 !important;
      font-size: 10.5px !important;
      font-weight: 700 !important;
      padding: 1.5px 5px !important;
      border-radius: 3px !important;
    }

    #recommended-grid.produtos-layout-list .card-rating-row {
      display: flex !important;
      align-items: center !important;
      gap: 3px !important;
      font-size: 11px !important;
      color: #8a8b91 !important;
      margin-bottom: auto !important;
    }

    #recommended-grid.produtos-layout-list .star-yellow {
      color: #ffaa00 !important;
      font-size: 11px !important;
    }

    #recommended-grid.produtos-layout-list .rating-pipe {
      color: #d1d5db !important;
      margin: 0 1px !important;
    }

    #recommended-grid.produtos-layout-list .card-bottom-action-row {
      display: flex !important;
      align-items: flex-end !important;
      justify-content: space-between !important;
      width: 100% !important;
      margin-top: auto !important;
    }

    #recommended-grid.produtos-layout-list .price-stack-col {
      display: flex !important;
      flex-direction: column !important;
    }

    #recommended-grid.produtos-layout-list .price-current-txt {
      font-size: 16.5px !important;
      font-weight: 700 !important;
      color: #fe2c55 !important;
      line-height: 1 !important;
      display: flex !important;
      align-items: baseline !important;
      gap: 1px !important;
    }

    #recommended-grid.produtos-layout-list .price-current-txt .currency {
      font-size: 11px !important;
      font-weight: 700 !important;
      color: #fe2c55 !important;
      margin-right: 1px !important;
    }

    #recommended-grid.produtos-layout-list .price-old-txt {
      font-size: 11px !important;
      color: #8a8b91 !important;
      text-decoration: line-through !important;
      margin-top: 2px !important;
      line-height: 1 !important;
      display: block !important;
    }

    #recommended-grid.produtos-layout-list .unified-buy-btn {
      display: flex !important;
      align-items: stretch !important;
      background: #fe2c55 !important;
      border-radius: 6px !important;
      overflow: hidden !important;
      height: 30px !important;
      box-shadow: 0 1px 3px rgba(254,44,85,0.2) !important;
      flex-shrink: 0 !important;
      cursor: pointer !important;
      text-decoration: none !important;
    }

    #recommended-grid.produtos-layout-list .btn-cart-part {
      background: #fdf0f3 !important;
      padding: 0 8px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
    }

    #recommended-grid.produtos-layout-list .btn-txt-part {
      background: #fe2c55 !important;
      color: #fff !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      padding: 0 10px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      white-space: nowrap !important;
    }
`;

// Substituir ou injetar styles limpos
const headCloseIdx = html.indexOf('</head>');
html = html.slice(0, headCloseIdx) + `<style>\n${perfectStyles}\n</style>\n` + html.slice(headCloseIdx);

// =========================================================================
// 4. JS CANÔNICO PARA TROCA DE ABAS E ORDENAÇÃO
// =========================================================================
const perfectScript = `
    // Switch de Abas Oficial TikTok Shop
    function switchTab(btn, tab) {
      document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');

      const mainSec = document.getElementById('principais-produtos-section');
      const novosSec = document.getElementById('novos-lancamentos-section');
      const recSec = document.getElementById('produtos-recomendados-section');
      const catSec = document.getElementById('categorias-section');
      const subBar = document.getElementById('subfilter-produtos-bar');
      const grid = document.getElementById('recommended-grid');
      const divider = document.querySelector('.divider-home-rec');

      // Garante que o scroll vá pro topo instantaneamente
      window.scrollTo({ top: 0, behavior: 'instant' });

      if (tab === 'home') {
        if (mainSec) mainSec.style.display = 'block';
        if (novosSec) novosSec.style.display = 'block';
        if (recSec) {
          recSec.style.display = 'block';
          recSec.classList.remove('hide-home-divider');
        }
        if (catSec) catSec.style.display = 'none';
        if (subBar) subBar.style.display = 'none';
        if (divider) divider.style.display = 'flex';
        if (grid) grid.classList.remove('produtos-layout-list');
        document.querySelectorAll('.product-card-rec').forEach(c => c.style.display = '');
      } else if (tab === 'produtos') {
        if (mainSec) mainSec.style.display = 'none';
        if (novosSec) novosSec.style.display = 'none';
        if (recSec) {
          recSec.style.display = 'block';
          recSec.classList.add('hide-home-divider');
        }
        if (catSec) catSec.style.display = 'none';
        if (subBar) subBar.style.display = 'flex';
        if (divider) divider.style.display = 'none';
        if (grid) grid.classList.add('produtos-layout-list');
        document.querySelectorAll('.product-card-rec').forEach(c => c.style.display = '');
      } else if (tab === 'categorias') {
        if (mainSec) mainSec.style.display = 'none';
        if (novosSec) novosSec.style.display = 'none';
        if (recSec) recSec.style.display = 'none';
        if (catSec) catSec.style.display = 'block';
        if (subBar) subBar.style.display = 'none';
      }
    }

    // Filtro por categoria (Print 2)
    function filterByCategory(catName) {
      const produtosTabBtn = document.querySelectorAll('.nav-tab')[1];
      switchTab(produtosTabBtn, 'produtos');

      const cards = document.querySelectorAll('.product-card-rec');
      cards.forEach(card => {
        const cat = card.getAttribute('data-cat') || '';
        const nome = card.getAttribute('data-nome') || '';
        if (cat.toLowerCase().includes(catName.toLowerCase()) || nome.toLowerCase().includes(catName.toLowerCase())) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    }

    // Sub-filtro da aba Produtos: Recomendado | Mais vendidos | Lançamentos
    function setSubFilter(el, type) {
      document.querySelectorAll('.subfilter-item').forEach(item => item.classList.remove('active'));
      if (el) el.classList.add('active');

      const grid = document.getElementById('recommended-grid');
      if (!grid) return;
      const cards = Array.from(grid.querySelectorAll('.product-card-rec'));

      if (type === 'mais-vendidos') {
        cards.sort((a, b) => {
          const vA = parseInt(a.getAttribute('data-vendas') || '0', 10);
          const vB = parseInt(b.getAttribute('data-vendas') || '0', 10);
          return vB - vA;
        });
      } else if (type === 'lancamentos') {
        cards.sort((a, b) => {
          const idA = parseInt(a.getAttribute('data-id') || '0', 10);
          const idB = parseInt(b.getAttribute('data-id') || '0', 10);
          return idB - idA;
        });
      } else {
        // Recomendado: produto 104 primeiro, seguido dos outros
        cards.sort((a, b) => {
          const hrefA = a.getAttribute('href') || '';
          const hrefB = b.getAttribute('href') || '';
          if (hrefA.includes('produto-104.html')) return -1;
          if (hrefB.includes('produto-104.html')) return 1;
          return 0;
        });
      }

      cards.forEach(card => grid.appendChild(card));
    }

    window.applySubFilter = setSubFilter;
    window.setSubFilter = setSubFilter;
    window.switchTab = switchTab;
    window.filterByCategory = filterByCategory;

    function toggleLayoutView() {
      const grid = document.getElementById('recommended-grid');
      if (!grid) return;
      grid.classList.toggle('produtos-layout-list');
    }
`;

const sStart = html.indexOf('function switchTab');
const sEnd = html.indexOf('initShareTooltip();');
if (sStart !== -1 && sEnd !== -1) {
  html = html.slice(0, sStart) + perfectScript + '\n\n    ' + html.slice(sEnd);
  console.log('✅ JS de abas e ordenação canônica atualizado!');
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('>>> [BRUNO CTO] RECONSTRUÇÃO FINAL CONCLUÍDA! <<<');
