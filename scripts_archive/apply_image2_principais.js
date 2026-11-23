const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

console.log('>>> [BRUNO CTO] APLICANDO PADRÃO CANÔNICO DA IMAGEM 2 EM PRINCIPAIS PRODUTOS <<<');

// 1. REESTRUTURAR A SEÇÃO "PRINCIPAIS PRODUTOS" IDÊNTICA À IMAGEM 2
const principaisSectionImage2 = `<!-- PRINCIPAIS PRODUTOS (Padrão Oficial Imagem 2) -->
          <div style="background: white; padding: 16px; margin-bottom: 8px;" id="principais-produtos-section">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; cursor: pointer;" onclick="switchTab(document.querySelectorAll('.nav-tab')[1], 'produtos')">
              <h2 style="font-size: 19px; font-weight: 700; color: #161823; margin: 0; letter-spacing: -0.3px;">Principais produtos</h2>
              <div style="display: flex; align-items: center; gap: 3px; font-size: 14px; font-weight: 500; color: #161823;">
                Ver mais
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 18l6-6-6-6"></path>
                </svg>
              </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;">
              <!-- TOP 1 -->
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: block;">
                <div style="position: relative; background: white;">
                  <!-- Selo discreto TOP 1 Imagem 2 -->
                  <div class="top-ranking-badge badge-top-1">1</div>
                  <img src="img/real-top1.jpg" alt="Chinelo feminino Cruzada Glitter" loading="eager"
                    onerror="this.src='https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/937eda3788b14961af3dc12028a4c886~tplv-aphluv4xwc-resize-webp:800:800.webp'"
                    style="width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; margin-bottom: 6px; display: block; background: #f5f5f5;">
                  <h3 class="principais-prod-title">Chinelo feminino Cruz...</h3>
                  <div style="margin-bottom: 4px;">
                    <span class="badge-frete-gratis">Frete grátis</span>
                  </div>
                  <div class="principais-price-stack">
                    <div class="principais-price-cur"><span class="currency">R$</span> 32,44</div>
                    <div class="principais-price-old">R$ 49,90</div>
                  </div>
                  <div class="principais-sales-txt">14.1K vendido(s)</div>
                </div>
              </a>

              <!-- TOP 2 -->
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: block;">
                <div style="position: relative; background: white;">
                  <!-- Selo discreto TOP 2 Imagem 2 -->
                  <div class="top-ranking-badge badge-top-2">2</div>
                  <img src="img/real-top2.jpg" alt="Chinelo feminino NO STRASS Verão" loading="eager"
                    onerror="this.src='https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/937eda3788b14961af3dc12028a4c886~tplv-aphluv4xwc-resize-webp:800:800.webp'"
                    style="width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; margin-bottom: 6px; display: block; background: #f5f5f5;">
                  <h3 class="principais-prod-title">Chinelo feminino NO S...</h3>
                  <div style="margin-bottom: 4px;">
                    <span class="badge-frete-gratis">Frete grátis</span>
                  </div>
                  <div class="principais-price-stack">
                    <div class="principais-price-cur"><span class="currency">R$</span> 39,53</div>
                    <div class="principais-price-old">R$ 59,90</div>
                  </div>
                  <div class="principais-sales-txt">9017 vendido(s)</div>
                </div>
              </a>

              <!-- TOP 3 -->
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: block;">
                <div style="position: relative; background: white;">
                  <!-- Selo discreto TOP 3 Imagem 2 -->
                  <div class="top-ranking-badge badge-top-3">3</div>
                  <img src="img/real-top3.jpg" alt="Chinelo feminino LUXO STRASS" loading="eager"
                    onerror="this.src='https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/937eda3788b14961af3dc12028a4c886~tplv-aphluv4xwc-resize-webp:800:800.webp'"
                    style="width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; margin-bottom: 6px; display: block; background: #f5f5f5;">
                  <h3 class="principais-prod-title">Chinelo feminino LUX...</h3>
                  <div style="margin-bottom: 4px;">
                    <span class="badge-frete-gratis">Frete grátis</span>
                  </div>
                  <div class="principais-price-stack">
                    <div class="principais-price-cur"><span class="currency">R$</span> 39,53</div>
                    <div class="principais-price-old">R$ 59,90</div>
                  </div>
                  <div class="principais-sales-txt">8967 vendido(s)</div>
                </div>
              </a>
            </div>
          </div>`;

// Substituir a seção antiga pela nova
const pStart = html.indexOf('<div style="background: white; padding: 16px; margin-bottom: 8px;" id="principais-produtos-section">');
const pEnd = html.indexOf('<!-- SEÇÃO NOVOS LANÇAMENTOS');

if (pStart !== -1 && pEnd !== -1) {
  html = html.slice(0, pStart) + principaisSectionImage2 + '\n\n          ' + html.slice(pEnd);
  console.log('✅ Seção Principais produtos reconstruída conforme Imagem 2!');
} else {
  console.log('Tentando busca alternativa para pEnd...');
  const altEnd = html.indexOf('id="novos-lancamentos-section"');
  if (pStart !== -1 && altEnd !== -1) {
    const divBeforeNovos = html.lastIndexOf('<div', altEnd);
    html = html.slice(0, pStart) + principaisSectionImage2 + '\n\n          ' + html.slice(divBeforeNovos);
    console.log('✅ Seção Principais produtos reconstruída (busca alternativa)!');
  }
}

// 2. CSS DOS SELOS E TIPOGRAFIA DA IMAGEM 2
const image2Css = `
    /* === CSS OFICIAL IMAGEM 2 (PRINCIPAIS PRODUTOS E ABAS) === */
    /* Abas com tipografia de sistema oficial */
    .nav-tabs {
      background: #ffffff !important;
      border-bottom: 1px solid #e8e8e8 !important;
      display: flex !important;
      position: sticky !important;
      top: 50px !important;
      z-index: 100 !important;
    }

    .nav-tab {
      flex: 1 !important;
      height: 44px !important;
      background: transparent !important;
      border: none !important;
      font-size: 16px !important;
      font-weight: 500 !important;
      color: #8A8B91 !important;
      cursor: pointer !important;
      position: relative !important;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif !important;
      transition: color 0.15s ease !important;
    }

    .nav-tab.active {
      color: #161823 !important;
      font-weight: 700 !important;
    }

    .nav-tab.active::after {
      content: '' !important;
      position: absolute !important;
      bottom: 0 !important;
      left: 18% !important;
      width: 64% !important;
      height: 2.5px !important;
      background: #161823 !important;
      border-radius: 2px !important;
    }

    /* Selos discretos TOP 1, 2, 3 da Imagem 2 */
    .top-ranking-badge {
      position: absolute !important;
      top: 0 !important;
      left: 0 !important;
      z-index: 10 !important;
      width: 22px !important;
      height: 24px !important;
      border-top-left-radius: 8px !important;
      border-bottom-right-radius: 6px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }

    .badge-top-1 {
      background: #d8ba82 !important;
      color: #3d2b0e !important;
    }

    .badge-top-2 {
      background: #cad1d8 !important;
      color: #333d47 !important;
    }

    .badge-top-3 {
      background: #d5ab92 !important;
      color: #45291b !important;
    }

    /* Título do produto nos Principais Produtos */
    .principais-prod-title {
      font-size: 13px !important;
      font-weight: 500 !important;
      color: #161823 !important;
      line-height: 1.3 !important;
      margin: 0 0 4px 0 !important;
      display: -webkit-box !important;
      -webkit-line-clamp: 2 !important;
      -webkit-box-orient: vertical !important;
      overflow: hidden !important;
      height: 34px !important;
    }

    /* Preço nos Principais Produtos (Imagem 2) */
    .principais-price-stack {
      display: flex !important;
      flex-direction: column !important;
      margin-top: 2px !important;
    }

    .principais-price-cur {
      font-size: 15.5px !important;
      font-weight: 700 !important;
      color: #fe2c55 !important;
      line-height: 1.1 !important;
      display: flex !important;
      align-items: baseline !important;
      gap: 1.5px !important;
    }

    .principais-price-cur .currency {
      font-size: 11px !important;
      font-weight: 700 !important;
      color: #fe2c55 !important;
    }

    .principais-price-old {
      font-size: 11px !important;
      color: #8a8b91 !important;
      text-decoration: line-through !important;
      margin-top: 1.5px !important;
      line-height: 1 !important;
    }

    .principais-sales-txt {
      font-size: 11px !important;
      color: #8a8b91 !important;
      margin-top: 3px !important;
      line-height: 1.1 !important;
    }
`;

html = html.replace('</head>', `<style>\n${image2Css}\n</style>\n</head>`);

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ index.html gravado com padrão canônico da Imagem 2!');
