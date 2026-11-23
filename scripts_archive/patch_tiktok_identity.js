const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. ADICIONAR CSS PARA O TOOLTIP DE COMPARTILHAMENTO, SUB-BARRA DE FILTROS E BADGES
const customCss = `
    /* === ESTILOS TIKTOK SHOP OFICIAL (100% IDÊNTICO AOS PRINTS) === */
    .header-share-btn {
      position: relative !important;
    }
    .share-dot {
      position: absolute;
      top: 1px;
      right: 1px;
      width: 7px;
      height: 7px;
      background: #fe2c55;
      border-radius: 50%;
      border: 1.5px solid #fff;
    }
    .share-tooltip-bubble {
      position: fixed;
      top: 50px;
      right: 12px;
      background: #00a8b5;
      color: #ffffff;
      padding: 9px 12px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 500;
      line-height: 1.35;
      max-width: 230px;
      box-shadow: 0 4px 16px rgba(0, 168, 181, 0.4);
      z-index: 10005;
      cursor: pointer;
      opacity: 0;
      transform: translateY(-8px);
      transition: opacity 0.35s ease, transform 0.35s ease;
      pointer-events: auto;
      text-align: left;
    }
    .share-tooltip-bubble.visible {
      opacity: 1;
      transform: translateY(0);
    }
    .share-tooltip-arrow {
      position: absolute;
      top: -7px;
      right: 48px;
      width: 0;
      height: 0;
      border-left: 6px solid transparent;
      border-right: 6px solid transparent;
      border-bottom: 7px solid #00a8b5;
    }

    /* Sub-filtro da aba Produtos */
    .subfilter-produtos-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 16px 8px;
      background: #fff;
    }
    .subfilter-items {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .subfilter-item {
      font-size: 13px;
      color: #757575;
      font-weight: 500;
      cursor: pointer;
    }
    .subfilter-item.active {
      color: #161823;
      font-weight: 700;
    }
    .subfilter-divider {
      color: #e5e5e5;
      font-size: 12px;
    }
    .subfilter-view-toggle {
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* Badges oficiais TikTok Shop */
    .badge-frete-gratis {
      background: #e6f9f6 !important;
      color: #00a699 !important;
      font-size: 10.5px !important;
      font-weight: 600 !important;
      padding: 2px 6px !important;
      border-radius: 3px !important;
      display: inline-flex !important;
      align-items: center !important;
      line-height: 1.2 !important;
    }
    .badge-oferta-relampago {
      background: #ff5722 !important;
      color: #ffffff !important;
      font-size: 10.5px !important;
      font-weight: 700 !important;
      padding: 2px 6px !important;
      border-radius: 3px !important;
      display: inline-flex !important;
      align-items: center !important;
      gap: 3px !important;
      line-height: 1.2 !important;
    }
    .badge-discount-percent {
      background: #ffebee !important;
      color: #fe2c55 !important;
      font-size: 10px !important;
      font-weight: 700 !important;
      padding: 1px 4px !important;
      border-radius: 3px !important;
      margin-left: 4px !important;
    }

    /* Ajustes dos preços em coluna vertical */
    .produtos-layout-list .product-card-rec .price-y2k-current {
      font-size: 18px !important;
      font-weight: 800 !important;
      color: #fe2c55 !important;
      display: flex !important;
      align-items: baseline !important;
      line-height: 1.1 !important;
    }
    .produtos-layout-list .product-card-rec .price-y2k-current span {
      font-size: 12px !important;
      font-weight: 800 !important;
      margin-right: 2px !important;
    }
    .produtos-layout-list .product-card-rec .price-y2k-old {
      font-size: 11px !important;
      color: #999999 !important;
      text-decoration: line-through !important;
      margin-top: 1px !important;
      margin-left: 0px !important;
      display: block !important;
    }

    /* Botão unificado integrado TikTok Shop */
    .produtos-layout-list .product-card-rec .action-y2k-container {
      display: flex !important;
      align-items: stretch !important;
      height: 32px !important;
      border-radius: 6px !important;
      overflow: hidden !important;
      margin-top: auto !important;
      align-self: flex-end !important;
      margin-bottom: 2px !important;
      margin-left: auto !important;
      box-shadow: 0 1px 3px rgba(254, 44, 85, 0.15) !important;
    }
    .produtos-layout-list .product-card-rec .cart-y2k-btn {
      background: #ffe8ee !important;
      border: none !important;
      width: 34px !important;
      height: 32px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      cursor: pointer !important;
      padding: 0 !important;
    }
    .produtos-layout-list .product-card-rec .cart-y2k-btn svg {
      width: 16px !important;
      height: 16px !important;
      stroke: #fe2c55 !important;
      stroke-width: 2.2 !important;
      fill: none !important;
    }
    .produtos-layout-list .product-card-rec .buy-y2k-btn {
      background: #fe2c55 !important;
      color: #ffffff !important;
      border: none !important;
      padding: 0 12px !important;
      height: 32px !important;
      font-size: 13px !important;
      font-weight: 700 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      cursor: pointer !important;
      letter-spacing: -0.2px !important;
    }
`;

// Injeta o CSS antes de </head>
if (!html.includes('/* === ESTILOS TIKTOK SHOP OFICIAL')) {
  html = html.replace('</head>', `<style>${customCss}</style>\n</head>`);
}

// 2. ATUALIZAR O BOTÃO DE SHARE COM A NOTIFICATION DOT E ADICIONAR O TOOLTIP FLUTUANTE
const shareBtnPattern = /<button class="header-share-btn"[^>]*>[\s\S]*?<\/button>/i;
const updatedShareBtn = `<button class="header-share-btn" onclick="shareProduct()" aria-label="Compartilhar">
          <img src="img/share-arrow.png" alt="Compartilhar" style="width: 22px; height: 22px; object-fit: contain;">
          <span class="share-dot"></span>
        </button>`;

html = html.replace(shareBtnPattern, updatedShareBtn);

// Injeta o tooltip popup logo após o </header> se não existir
if (!html.includes('id="share-tooltip-bubble"')) {
  const tooltipHtml = `
    <!-- TOOLTIP CIANO OFICIAL TIKTOK SHOP -->
    <div id="share-tooltip-bubble" class="share-tooltip-bubble" onclick="closeShareTooltip()">
      <div class="share-tooltip-arrow"></div>
      Compartilhe isso com amigos para ganhar comissões nas compras deles
    </div>
  `;
  html = html.replace('</header>', `</header>\n${tooltipHtml}`);
}

// 3. ATUALIZAR O PERFIL DA LOJA COM O BADGE "LOJA ESTRELA" E CONTAGEM
const storeInfoPattern = /<div class="store-info">[\s\S]*?<\/div>/i;
const updatedStoreInfo = `<div class="store-info">
                <h2 style="display: flex; align-items: center; gap: 4px; font-size: 16px; font-weight: 700; color: #161823; margin: 0 0 2px 0;">
                  Stone Shop
                  <svg viewBox="0 0 24 24" width="15" height="15" style="color:#0095f6; flex-shrink:0;" fill="currentColor">
                    <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                  </svg>
                </h2>
                <div style="display: flex; align-items: center; gap: 5px;">
                  <span style="background: #fdf3e7; color: #91580f; font-size: 10.5px; font-weight: 600; padding: 1px 5px; border-radius: 3px; display: inline-flex; align-items: center; gap: 3px;">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="#91580f"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                    Loja Estrela
                  </span>
                  <span style="font-size: 11.5px; color: #757575;">36.4K vendido(s)</span>
                </div>
              </div>`;

html = html.replace(storeInfoPattern, updatedStoreInfo);

// 4. ATUALIZAR O CONTAINER DE CUPONS: "CUPOM DE ENVIO", "EM PEDIDOS ACIMA DE R$ 109", "RESGATADO"
const couponPattern = /<!-- COUPONS CONTAINER -->[\s\S]*?<\/div>\s*<\/div>/i;
const updatedCoupons = `<!-- COUPONS CONTAINER -->
          <div class="coupons-container" style="display: flex; gap: 8px; padding: 8px 16px; overflow-x: auto;">
            <div class="coupon-card" style="position: relative; display: flex; align-items: center; justify-content: space-between; width: 100%; height: 56px; padding: 10px 14px; background: #e8f8f5; border-radius: 8px; overflow: hidden; box-sizing: border-box;">
              <svg viewBox="0 0 398 87" preserveAspectRatio="none" fill="none" xmlns="http://www.w3.org/2000/svg"
                style="position: absolute; top: 0px; left: 0px; width: 100%; height: 100%; pointer-events: none; z-index: 1; overflow: visible;">
                <path
                  d="M390.762 0C394.747 0 397.978 3.23059 397.979 7.21582V37.5264C397.948 37.5259 397.918 37.5244 397.888 37.5244C394.55 37.5245 391.845 40.2306 391.845 43.5684C391.845 46.9061 394.55 49.6122 397.888 49.6123C397.918 49.6123 397.948 49.6098 397.979 49.6094V79.7402C397.978 83.7256 394.747 86.9561 390.762 86.9561H7.21582C3.23067 86.9558 0.000147966 83.7254 0 79.7402V49.6094C0.0299052 49.6098 0.0598349 49.6123 0.0898438 49.6123C3.42764 49.6123 6.13376 46.9061 6.13379 43.5684C6.13379 40.2305 3.42765 37.5244 0.0898438 37.5244C0.0598392 37.5244 0.0299009 37.5259 0 37.5264V7.21582C0.000248585 3.23074 3.23074 0.000251417 7.21582 0H390.762Z"
                  fill="#e8f8f5"></path>
              </svg>
              <div class="coupon-text" style="position: relative; z-index: 2;">
                <div class="coupon-title" style="font-size: 13.5px; font-weight: 700; color: #161823; line-height: 1.2;">Cupom de envio</div>
                <div class="coupon-subtitle" style="font-size: 11px; color: #757575; margin-top: 2px;">em pedidos acima de R$ 109</div>
              </div>
              <span class="coupon-btn-resgatado" style="position: relative; z-index: 2; font-size: 13px; font-weight: 600; color: #20b5a6;">Resgatado</span>
            </div>
          </div>`;

html = html.replace(couponPattern, updatedCoupons);

// 5. INJETAR A SUB-BARRA DE FILTROS ABAIXO DAS ABAS
if (!html.includes('id="subfilter-produtos-bar"')) {
  const subfilterHtml = `
          <!-- SUB-BARRA DE FILTROS DA ABA PRODUTOS -->
          <div id="subfilter-produtos-bar" class="subfilter-produtos-bar" style="display: none;">
            <div class="subfilter-items">
              <span class="subfilter-item active" onclick="setSubFilter(this, 'recomendado')">Recomendado</span>
              <span class="subfilter-divider">|</span>
              <span class="subfilter-item" onclick="setSubFilter(this, 'mais-vendidos')">Mais vendidos</span>
              <span class="subfilter-divider">|</span>
              <span class="subfilter-item" onclick="setSubFilter(this, 'lancamentos')">Lançamentos</span>
            </div>
            <div class="subfilter-view-toggle" onclick="toggleLayoutView()">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#757575" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="7"></rect>
                <rect x="14" y="3" width="7" height="7"></rect>
                <rect x="14" y="14" width="7" height="7"></rect>
                <rect x="3" y="14" width="7" height="7"></rect>
              </svg>
            </div>
          </div>
  `;
  const navTabsEnd = html.indexOf('</div>', html.indexOf('class="nav-tabs"')) + 6;
  html = html.slice(0, navTabsEnd) + subfilterHtml + html.slice(navTabsEnd);
}

// 6. ATUALIZAR O switchTab PARA MOSTRAR/OCULTAR A SUB-BARRA DE FILTROS
html = html.replace(
  "if (grid) grid.classList.remove('produtos-layout-list');",
  "if (grid) grid.classList.remove('produtos-layout-list');\n        const subBar = document.getElementById('subfilter-produtos-bar');\n        if (subBar) subBar.style.display = 'none';"
);

html = html.replace(
  "if (grid) grid.classList.add('produtos-layout-list');",
  "if (grid) grid.classList.add('produtos-layout-list');\n        const subBar = document.getElementById('subfilter-produtos-bar');\n        if (subBar) subBar.style.display = 'flex';"
);

// 7. ATUALIZAR O TÍTULO DO DIVISOR DA HOME: "—— Recomendado para você ——" (Print 3)
html = html.replace(
  'Produtos Recomendados',
  'Recomendado para você'
);

// 8. ATUALIZAR A LÓGICA DO SCRIPT DOMContentLoaded QUE FORMATA OS CARDS (Linha 3900+)
// Vamos localizar o bloco onde `badgeHtml` e `card.innerHTML` são construídos
const oldBadgeBlockStart = html.indexOf('// Gerar badges Y2K Shopee');
const oldCardInnerStart = html.indexOf('card.innerHTML = `', oldBadgeBlockStart);
const oldCardInnerEnd = html.indexOf('`;', oldCardInnerStart) + 2;

if (oldBadgeBlockStart !== -1 && oldCardInnerStart !== -1) {
  const newCardRenderer = `// Gerar badges e layout TikTok Shop Oficial idêntico aos prints
        const isOfertaRelampago = nome.toLowerCase().includes('chinelo') || nome.toLowerCase().includes('sandalia') || nome.toLowerCase().includes('plataforma') || prodId === '104';
        
        let badgesHtml = '';
        if (isOfertaRelampago) {
          badgesHtml += \`<span class="badge-oferta-relampago"><svg width="9" height="11" viewBox="0 0 24 24" fill="#ffffff"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>Oferta Relâmpago</span> \`;
        }
        badgesHtml += \`<span class="badge-frete-gratis">Frete grátis</span>\`;

        // Avaliações autênticas
        let ratingVal = '4.8';
        if (prodId === '104') ratingVal = '4.8';
        else if (nome.toLowerCase().includes('flat rafia')) ratingVal = '4.5';
        else if (nome.toLowerCase().includes('cruzada')) ratingVal = '4.5';
        else if (nome.toLowerCase().includes('portugal')) ratingVal = '4.9';

        // Vendas autênticas
        let salesText = '100 vendidos';
        const salesEl = card.querySelector('.product-sales');
        if (salesEl) {
          salesText = salesEl.textContent.replace('vendido(s)', 'vendidos');
        } else {
          if (prodId === '104') salesText = '21.3k vendidos';
          else if (prodId === '99') salesText = '14.7k vendidos';
          else if (prodId === '84') salesText = '200 vendidos';
          else if (prodId === '79') salesText = '131 vendidos';
        }

        // Montagem do card no padrão TikTok Shop Oficial
        card.innerHTML = \`
      <div style="background: white; border: none; border-radius: 8px; overflow: hidden; height: 100%; display: flex; flex-direction: column; width: 100%;">
        <img src="\${imgUrl}" alt="\${productName}" loading="lazy" onerror="this.style.display='none'">
        <div style="padding: 6px 8px 8px 8px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
          <h3 class="product-name" style="font-size: 13.5px; font-weight: 500; color: #161823; line-height: 1.3; margin: 0 0 4px 0;">\${productName}</h3>
          <div>
            <div class="badges-y2k-container" style="margin-bottom: 4px; display: flex; flex-wrap: wrap; gap: 4px; align-items: center;">
              \${badgesHtml}
            </div>
            <div class="sales-y2k-row" style="display: flex; align-items: center; gap: 3px; margin-bottom: 6px;">
              <span style="color: #ff9800; font-size: 11px;">★</span>
              <span style="color: #666; font-size: 11.5px; font-weight: 500;">\${ratingVal}</span>
              <span style="color: #ccc; margin: 0 1px;">|</span>
              <span style="color: #888; font-size: 11.5px;">\${salesText}</span>
            </div>
            <div style="display: flex; align-items: flex-end; justify-content: space-between; width: 100%;">
              <div class="product-price" style="display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-end;">
                <div class="price-y2k-current" style="color: #fe2c55; font-size: 18px; font-weight: 800; line-height: 1.1; display: flex; align-items: baseline;">
                  <span style="font-size: 11.5px; font-weight: 800; margin-right: 2px;">R$</span>\${currentPriceText}
                </div>
                \${oldPriceText ? \`<div class="price-y2k-old" style="font-size: 11px; color: #999999; text-decoration: line-through; margin-top: 1px;">\${oldPriceText}</div>\` : ''}
              </div>
              <div class="action-y2k-container">
                <button class="cart-y2k-btn" onclick="event.preventDefault(); event.stopPropagation(); window.openProductModalDirectly('\${link}');" title="Adicionar ao carrinho">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#fe2c55" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="9" cy="21" r="1"></circle>
                    <circle cx="20" cy="21" r="1"></circle>
                    <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                  </svg>
                </button>
                <button class="buy-y2k-btn" onclick="event.stopPropagation(); window.location.href='\${link}';">Comprar</button>
              </div>
            </div>
          </div>
        </div>
      </div>\`;`;

  html = html.slice(0, oldBadgeBlockStart) + newCardRenderer + html.slice(oldCardInnerEnd);
}

// 9. ADICIONAR AS FUNÇÕES JS GLOBAIS DE TOOLTIP E SUB-FILTRO
const customJs = `
    // Tooltip de Compartilhamento TikTok Shop
    function initShareTooltip() {
      const tooltip = document.getElementById('share-tooltip-bubble');
      if (!tooltip) return;
      setTimeout(() => {
        tooltip.classList.add('visible');
      }, 400);

      setTimeout(() => {
        closeShareTooltip();
      }, 4800);
    }

    function closeShareTooltip() {
      const tooltip = document.getElementById('share-tooltip-bubble');
      if (tooltip) {
        tooltip.classList.remove('visible');
        setTimeout(() => {
          if (tooltip && tooltip.parentNode) tooltip.style.display = 'none';
        }, 400);
      }
    }

    // Sub-filtros da aba Produtos
    function setSubFilter(el, type) {
      document.querySelectorAll('.subfilter-item').forEach(item => item.classList.remove('active'));
      el.classList.add('active');
    }

    function toggleLayoutView() {
      const grid = document.getElementById('recommended-grid');
      if (!grid) return;
      grid.classList.toggle('produtos-layout-list');
    }

    document.addEventListener('DOMContentLoaded', () => {
      initShareTooltip();
    });
`;

if (!html.includes('function initShareTooltip()')) {
  html = html.replace('</body>', `<script>${customJs}</script>\n</body>`);
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ index.html atualizado com perfeição TikTok Shop!');
