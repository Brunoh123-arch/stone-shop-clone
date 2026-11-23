const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. CALIBRAR A TONALIDADE DO PREÇO ATUAL E RISCADO (Menos saturado, mais suave e idêntico à Foto 1)
html = html.replace(
  /\.produtos-layout-list \.product-card-rec \.price-y2k-current\s*\{[\s\S]*?\}/,
  `.produtos-layout-list .product-card-rec .price-y2k-current {
      font-size: 17px !important;
      font-weight: 700 !important;
      color: #de1f4c !important;
      display: flex !important;
      align-items: baseline !important;
      line-height: 1.15 !important;
    }`
);

html = html.replace(
  /\.produtos-layout-list \.product-card-rec \.price-y2k-current span\s*\{[\s\S]*?\}/,
  `.produtos-layout-list .product-card-rec .price-y2k-current span {
      font-size: 11px !important;
      font-weight: 600 !important;
      margin-right: 2px !important;
      color: #de1f4c !important;
    }`
);

html = html.replace(
  /\.produtos-layout-list \.product-card-rec \.price-y2k-old\s*\{[\s\S]*?\}/,
  `.produtos-layout-list .product-card-rec .price-y2k-old {
      font-size: 11px !important;
      color: #8c8c8c !important;
      font-weight: 400 !important;
      text-decoration: line-through !important;
      margin-top: 1px !important;
      margin-left: 0px !important;
      display: block !important;
    }`
);

// 2. ATUALIZAR O PERFIL DA LOJA (Loja Estrela idêntico à Foto 1)
const storeInfoRegex = /<div class="store-info">[\s\S]*?<\/div>/;
const updatedStoreInfo = `<div class="store-info">
                <h2 style="display: flex; align-items: center; gap: 4px; font-size: 16px; font-weight: 700; color: #161823; margin: 0 0 2px 0;">
                  Stone Shop
                  <svg viewBox="0 0 24 24" width="15" height="15" style="color:#0095f6; flex-shrink:0;" fill="currentColor">
                    <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                  </svg>
                </h2>
                <div style="display: flex; align-items: center; gap: 6px; margin-top: 4px;">
                  <span style="background: #fbf1e2; color: #8e5812; font-size: 11px; font-weight: 600; padding: 1.5px 6px; border-radius: 4px; display: inline-flex; align-items: center; gap: 3px;">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="#8e5812"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                    Loja Estrela
                  </span>
                  <span style="font-size: 12px; color: #161823; font-weight: 400;">36.4K vendido(s)</span>
                </div>
              </div>`;

html = html.replace(storeInfoRegex, updatedStoreInfo);

// 3. ATUALIZAR A LÓGICA DO SCRIPT DOMContentLoaded PARA AS ESTRELAS E VENDAS REAIS (Foto 1 e 4)
const cardLoopStart = html.indexOf('// Gerar badges e layout TikTok Shop Oficial idêntico aos prints');
const cardLoopEnd = html.indexOf('// Mover a camisa de Portugal', cardLoopStart);

if (cardLoopStart !== -1 && cardLoopEnd !== -1) {
  const newCardLogic = `// Gerar badges e layout TikTok Shop Oficial idêntico aos prints
        const isOfertaRelampago = nome.toLowerCase().includes('chinelo') || nome.toLowerCase().includes('sandalia') || nome.toLowerCase().includes('plataforma') || prodId === '104';
        
        let badgesHtml = '';
        if (isOfertaRelampago) {
          badgesHtml += \`<span class="badge-oferta-relampago"><svg width="9" height="11" viewBox="0 0 24 24" fill="#ffffff"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>Oferta Relâmpago</span> \`;
        }
        badgesHtml += \`<span class="badge-frete-gratis">Frete grátis</span>\`;

        // Tratamento autêntico de Vendas e Avaliações (idêntico à Imagem 1 e 4)
        // Alguns produtos têm poucas vendas e não têm estrela/nota!
        let salesText = '100 vendidos';
        const salesEl = card.querySelector('.product-sales');
        if (salesEl) {
          salesText = salesEl.textContent.replace('vendido(s)', 'vendidos').trim();
        } else {
          if (prodId === '104') salesText = '21.3k vendidos';
          else if (prodId === '99') salesText = '14.7k vendidos';
          else if (prodId === '84') salesText = '200 vendidos';
          else if (prodId === '79') salesText = '131 vendidos';
          else if (prodId === '28') salesText = '12.5k vendidos';
        }

        // Determinar se tem avaliação ou apenas contagem de vendas
        const salesCountNum = parseInt(salesText.replace(/[^0-9]/g, ''), 10) || 0;
        let ratingHtml = '';
        if (salesCountNum < 50 && !salesText.includes('k')) {
          // Sem avaliação, apenas número de vendas (como no print 4: "4 vendidos")
          ratingHtml = \`<div class="sales-y2k-row" style="display: flex; align-items: center; font-size: 12px; color: #757575; margin-bottom: 6px;">
            <span>\${salesText}</span>
          </div>\`;
        } else {
          // Com estrela amarela suave e nota
          let ratingVal = '4.8';
          if (prodId === '104') ratingVal = '4.8';
          else if (nome.toLowerCase().includes('flat rafia')) ratingVal = '4.5';
          else if (nome.toLowerCase().includes('cruzada')) ratingVal = '4.5';
          else if (nome.toLowerCase().includes('no strass')) ratingVal = '4.7';
          else if (nome.toLowerCase().includes('portugal')) ratingVal = '4.9';

          ratingHtml = \`<div class="sales-y2k-row" style="display: flex; align-items: center; gap: 3px; font-size: 12px; color: #757575; margin-bottom: 6px;">
            <span style="color: #faad14; font-size: 12px;">★</span>
            <span style="color: #757575; font-size: 11.5px; font-weight: 500;">\${ratingVal}</span>
            <span style="color: #e5e5e5; margin: 0 3px;">|</span>
            <span style="color: #757575; font-size: 11.5px;">\${salesText}</span>
          </div>\`;
        }

        // Montagem do card no padrão TikTok Shop Oficial com tonalidade calibrada
        card.innerHTML = \`
      <div style="background: white; border: none; border-radius: 8px; overflow: hidden; height: 100%; display: flex; flex-direction: column; width: 100%;">
        <img src="\${imgUrl}" alt="\${productName}" loading="lazy" onerror="this.style.display='none'">
        <div style="padding: 6px 8px 8px 8px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
          <h3 class="product-name" style="font-size: 13.5px; font-weight: 500; color: #161823; line-height: 1.3; margin: 0 0 4px 0;">\${productName}</h3>
          <div>
            <div class="badges-y2k-container" style="margin-bottom: 4px; display: flex; flex-wrap: wrap; gap: 4px; align-items: center;">
              \${badgesHtml}
            </div>
            \${ratingHtml}
            <div style="display: flex; align-items: flex-end; justify-content: space-between; width: 100%;">
              <div class="product-price" style="display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-end;">
                <div class="price-y2k-current">
                  <span>R$</span>\${currentPriceText}
                </div>
                \${oldPriceText ? \`<div class="price-y2k-old">\${oldPriceText}</div>\` : ''}
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
      </div>\`;
      });
      `;

  html = html.slice(0, cardLoopStart) + newCardLogic + html.slice(cardLoopEnd);
}

// 4. ATUALIZAR A FUNÇÃO setSubFilter PARA ORDENAÇÃO REAL DE RECOMENDADO / MAIS VENDIDOS / LANÇAMENTOS
const oldSetSubFilter = /function setSubFilter\(el, type\) \{[\s\S]*?\}/;
const newSetSubFilter = `function setSubFilter(el, type) {
      document.querySelectorAll('.subfilter-item').forEach(item => item.classList.remove('active'));
      el.classList.add('active');

      const grid = document.getElementById('recommended-grid');
      if (!grid) return;
      const cards = Array.from(grid.querySelectorAll('.product-card-rec'));

      if (type === 'mais-vendidos') {
        cards.sort((a, b) => {
          const getSalesNum = (card) => {
            const text = card.textContent || '';
            const match = text.match(/([\\d\\.,]+)\\s*k?\\s*vendido/i);
            if (!match) return 0;
            let val = parseFloat(match[1].replace(',', '.'));
            if (text.toLowerCase().includes('k vendido') || text.toLowerCase().includes('k. vendido')) val *= 1000;
            return val;
          };
          return getSalesNum(b) - getSalesNum(a);
        });
      } else if (type === 'lancamentos') {
        cards.sort((a, b) => {
          const getProdId = (card) => {
            const href = card.getAttribute('href') || '';
            const m = href.match(/produto-(\\d+)\\.html/);
            return m ? parseInt(m[1], 10) : 0;
          };
          return getProdId(b) - getProdId(a);
        });
      } else {
        // Recomendado: traz o produto 104 primeiro, seguido dos outros
        cards.sort((a, b) => {
          const hrefA = a.getAttribute('href') || '';
          const hrefB = b.getAttribute('href') || '';
          if (hrefA.includes('produto-104.html')) return -1;
          if (hrefB.includes('produto-104.html')) return 1;
          return 0;
        });
      }

      // Reanexa os cards na ordem correta
      cards.forEach(card => grid.appendChild(card));
    }`;

html = html.replace(oldSetSubFilter, newSetSubFilter);

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ index.html refinado com sucesso!');
