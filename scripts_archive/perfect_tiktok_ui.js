const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. GARANTIR QUE A PÁGINA INICIA NA ABA 'Página inicial' (IDÊNTICO À FOTO DE REFERÊNCIA)
html = html.replace(
  /document\.addEventListener\('DOMContentLoaded',\s*\(\)\s*=>\s*\{[\s\S]*?if\s*\(urlParams\.get\('tab'\)\s*!==\s*'home'[\s\S]*?switchTab\(prodTab,\s*'produtos'\);\s*\}\s*\}\);/,
  `document.addEventListener('DOMContentLoaded', () => {
      const urlParams = new URLSearchParams(window.location.search);
      // Se tiver explicitamente tab=produtos abre produtos, caso contrário abre na Página inicial (idêntico ao print oficial)
      if (urlParams.get('tab') === 'produtos' || window.location.hash === '#produtos') {
        const prodTab = document.querySelectorAll('.nav-tab')[1];
        if (prodTab && typeof switchTab === 'function') switchTab(prodTab, 'produtos');
      } else {
        const homeTab = document.querySelectorAll('.nav-tab')[0];
        if (homeTab && typeof switchTab === 'function') switchTab(homeTab, 'home');
      }
    });`
);

// 2. CSS DOS BADGES, CUPOM, PREÇOS E BOTÕES IDÊNTICOS À FOTO
const exactCss = `
    /* === CSS TIKTOK SHOP OFICIAL (100% IDÊNTICO AO PRINT) === */
    /* Barra superior e fundo atrás do card da loja */
    .page-content {
      background: #f4f4f4 !important;
    }
    
    /* Card da Loja flutuante com sombra suave */
    .store-section {
      background: #ffffff !important;
      border-radius: 12px 12px 0 0 !important;
      margin: 8px 12px 0 !important;
      padding: 14px 14px 10px !important;
      box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    }
    
    /* Loja Estrela */
    .badge-loja-estrela {
      background: #fdf3e7 !important;
      color: #91580f !important;
      font-size: 11px !important;
      font-weight: 600 !important;
      padding: 1.5px 6px !important;
      border-radius: 4px !important;
      display: inline-block !important;
      letter-spacing: -0.1px !important;
    }

    /* Container de cupons dentro do card da loja */
    .coupons-container {
      background: #ffffff !important;
      margin: 0 12px 8px !important;
      padding: 0 14px 14px !important;
      border-radius: 0 0 12px 12px !important;
      box-shadow: 0 2px 6px rgba(0,0,0,0.04) !important;
      display: flex !important;
    }
    .coupon-card-official {
      background: #eefbf7 !important;
      border-radius: 8px !important;
      width: 100% !important;
      padding: 9px 12px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      box-sizing: border-box !important;
    }
    .coupon-text-left .coupon-title {
      font-size: 13.5px !important;
      font-weight: 700 !important;
      color: #161823 !important;
      line-height: 1.2 !important;
    }
    .coupon-text-left .coupon-sub {
      font-size: 11px !important;
      color: #888888 !important;
      margin-top: 2px !important;
    }
    .coupon-resgatado-txt {
      font-size: 13px !important;
      font-weight: 600 !important;
      color: #20b5a6 !important;
    }

    /* Nav Tabs oficiais */
    .nav-tabs {
      background: #ffffff !important;
      display: flex !important;
      border-bottom: 1px solid #f0f0f0 !important;
      padding: 0 8px !important;
      margin-bottom: 0px !important;
    }
    .nav-tab {
      flex: 1 !important;
      text-align: center !important;
      padding: 12px 0 10px !important;
      font-size: 14.5px !important;
      font-weight: 500 !important;
      color: #757575 !important;
      border: none !important;
      background: transparent !important;
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
      left: 20% !important;
      right: 20% !important;
      height: 2.5px !important;
      background: #161823 !important;
      border-radius: 2px !important;
    }

    /* Badge Frete Grátis Oficial (Ciano Suave) */
    .badge-frete-gratis {
      background: #e6f9f6 !important;
      color: #00a699 !important;
      font-size: 10.5px !important;
      font-weight: 600 !important;
      padding: 2px 5px !important;
      border-radius: 3px !important;
      display: inline-flex !important;
      align-items: center !important;
      line-height: 1.2 !important;
    }

    /* Badge Oferta Relâmpago Oficial (Laranja com raio) */
    .badge-oferta-relampago {
      background: #ff5722 !important;
      color: #ffffff !important;
      font-size: 10.5px !important;
      font-weight: 700 !important;
      padding: 2px 5px !important;
      border-radius: 3px !important;
      display: inline-flex !important;
      align-items: center !important;
      gap: 2px !important;
      line-height: 1.2 !important;
    }

    /* Tonalidade do Preço Oficial TikTok Shop */
    .price-y2k-current, .price-current-tk {
      font-size: 17px !important;
      font-weight: 700 !important;
      color: #de1f4c !important;
      display: flex !important;
      align-items: baseline !important;
      line-height: 1.15 !important;
    }
    .price-y2k-current span, .price-current-tk span {
      font-size: 11px !important;
      font-weight: 600 !important;
      margin-right: 2px !important;
      color: #de1f4c !important;
    }
    .price-y2k-old, .price-old-tk {
      font-size: 11px !important;
      color: #8c8c8c !important;
      font-weight: 400 !important;
      text-decoration: line-through !important;
      margin-top: 1px !important;
      display: block !important;
    }

    /* Botão Unificado Integrado [ 🛒 | Comprar ] */
    .unified-action-btn {
      display: inline-flex !important;
      align-items: stretch !important;
      height: 31px !important;
      border-radius: 6px !important;
      overflow: hidden !important;
      cursor: pointer !important;
      box-shadow: 0 1px 3px rgba(222, 31, 76, 0.15) !important;
      border: none !important;
      padding: 0 !important;
      background: transparent !important;
    }
    .unified-cart-side {
      background: #ffe8ee !important;
      width: 32px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      border: none !important;
      padding: 0 !important;
      cursor: pointer !important;
    }
    .unified-buy-side {
      background: #de1f4c !important;
      color: #ffffff !important;
      font-size: 12.5px !important;
      font-weight: 700 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      padding: 0 11px !important;
      border: none !important;
      cursor: pointer !important;
      letter-spacing: -0.2px !important;
    }

    /* Divisor Central Estilizado —— Recomendado para você —— */
    .divider-home-rec {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      margin: 16px 0 12px !important;
      gap: 8px !important;
      color: #161823 !important;
      font-size: 14.5px !important;
      font-weight: 700 !important;
    }
    .divider-home-rec::before, .divider-home-rec::after {
      content: '' !important;
      width: 36px !important;
      height: 1.5px !important;
      background: linear-gradient(to right, transparent, #fe2c55) !important;
      border-radius: 2px !important;
    }
    .divider-home-rec::after {
      background: linear-gradient(to left, transparent, #fe2c55) !important;
    }
`;

// Substitui o bloco de estilo anterior
if (html.includes('/* === ESTILOS TIKTOK SHOP OFICIAL')) {
  const cssStart = html.indexOf('/* === ESTILOS TIKTOK SHOP OFICIAL');
  const cssEnd = html.indexOf('</style>', cssStart);
  html = html.slice(0, cssStart) + exactCss + html.slice(cssEnd);
} else {
  html = html.replace('</head>', `<style>${exactCss}</style>\n</head>`);
}

// 3. RECRIAR O CARD DA LOJA E CUPOM INTEGRADO (IDÊNTICO AO PRINT)
const storeAndCouponHtml = `<div class="store-section">
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <div style="display: flex; align-items: center; gap: 10px;">
                <img src="./img/essencia-avatar.jpg" alt="Essência outlet"
                  style="width: 58px; height: 58px; object-fit: cover; border-radius: 50%; border: 1px solid #f0f0f0;">
                <div>
                  <h2 style="font-size: 16px; font-weight: 700; color: #161823; margin: 0 0 3px 0; line-height: 1.2;">
                    Essência outlet
                  </h2>
                  <div style="margin-bottom: 2px;">
                    <span class="badge-loja-estrela">Loja Estrela</span>
                  </div>
                  <div style="font-size: 12px; color: #161823; font-weight: 400;">
                    36.4K vendido(s)
                  </div>
                </div>
              </div>
              <div style="display: flex; flex-direction: column; gap: 6px; align-items: flex-end;">
                <button style="background: #fe2c55; color: #fff; border: none; height: 32px; padding: 0 20px; border-radius: 16px; font-size: 13px; font-weight: 700; cursor: pointer;">Seguir</button>
                <button style="background: #f1f1f2; color: #161823; border: none; height: 32px; padding: 0 16px; border-radius: 16px; font-size: 13px; font-weight: 600; cursor: pointer;" onclick="openSmartChat()">Mensagem</button>
              </div>
            </div>
          </div>

          <!-- CUPOM DENTRO DA ÁREA DA LOJA -->
          <div class="coupons-container">
            <div class="coupon-card-official">
              <div class="coupon-text-left">
                <div class="coupon-title">Cupom de envio</div>
                <div class="coupon-sub">em pedidos acima de R$ 109</div>
              </div>
              <div class="coupon-resgatado-txt">Resgatado</div>
            </div>
          </div>`;

const storeStart = html.indexOf('<div class="store-section">');
const navTabsStart = html.indexOf('<!-- NAV TABS -->');
html = html.slice(0, storeStart) + storeAndCouponHtml + '\n\n          ' + html.slice(navTabsStart);

// 4. ATUALIZAR A SEÇÃO "PRINCIPAIS PRODUTOS" E "NOVOS LANÇAMENTOS" COM AS FOTOS E TEXTOS EXATOS DO PRINT
const principaisSectionHtml = `<!-- PRINCIPAIS PRODUTOS -->
          <div style="background: white; padding: 14px 16px; margin-bottom: 8px;" id="principais-produtos-section">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; cursor: pointer;" onclick="switchTab(document.querySelectorAll('.nav-tab')[1], 'produtos')">
              <h2 style="font-size: 16px; font-weight: 700; color: #161823; margin: 0px;">Principais produtos</h2>
              <div style="display: flex; align-items: center; gap: 2px; font-size: 13px; color: #757575;">
                Ver mais
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 18l6-6-6-6"></path>
                </svg>
              </div>
            </div>
            
            <!-- GRADE TOP 3 RANKING (IDÊNTICO AO PRINT) -->
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 18px;">
              <!-- TOP 1 -->
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;">
                <div style="position: relative; background: #f7f7f7; border-radius: 6px; overflow: hidden; aspect-ratio: 1/1; margin-bottom: 6px;">
                  <span style="position: absolute; top: 0; left: 0; background: #ecd299; color: #523910; font-size: 11px; font-weight: 800; padding: 2px 7px; border-bottom-right-radius: 6px; z-index: 5;">1</span>
                  <img src="img/real-top1.jpg" alt="Chinelo feminino Cruzada Glitter" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <h3 style="font-size: 12.5px; font-weight: 500; color: #161823; line-height: 1.25; margin: 0 0 4px 0; height: 32px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                  Chinelo feminino Cruz...
                </h3>
                <div style="margin-bottom: 3px;">
                  <span class="badge-frete-gratis">Frete grátis</span>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-start;">
                  <div class="price-current-tk">
                    <span>R$</span>32,44
                  </div>
                  <div class="price-old-tk">R$ 49,90</div>
                </div>
                <div style="font-size: 11px; color: #888; margin-top: 2px;">14.1K vendido(s)</div>
              </a>

              <!-- TOP 2 -->
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;">
                <div style="position: relative; background: #f7f7f7; border-radius: 6px; overflow: hidden; aspect-ratio: 1/1; margin-bottom: 6px;">
                  <span style="position: absolute; top: 0; left: 0; background: #cbd5e1; color: #334155; font-size: 11px; font-weight: 800; padding: 2px 7px; border-bottom-right-radius: 6px; z-index: 5;">2</span>
                  <img src="img/real-top2.jpg" alt="Chinelo feminino NO STRASS Verão 2025" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <h3 style="font-size: 12.5px; font-weight: 500; color: #161823; line-height: 1.25; margin: 0 0 4px 0; height: 32px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                  Chinelo feminino NO S...
                </h3>
                <div style="margin-bottom: 3px;">
                  <span class="badge-frete-gratis">Frete grátis</span>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-start;">
                  <div class="price-current-tk">
                    <span>R$</span>39,53
                  </div>
                  <div class="price-old-tk">R$ 59,90</div>
                </div>
                <div style="font-size: 11px; color: #888; margin-top: 2px;">9017 vendido(s)</div>
              </a>

              <!-- TOP 3 -->
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;">
                <div style="position: relative; background: #f7f7f7; border-radius: 6px; overflow: hidden; aspect-ratio: 1/1; margin-bottom: 6px;">
                  <span style="position: absolute; top: 0; left: 0; background: #d9b89d; color: #4a2c16; font-size: 11px; font-weight: 800; padding: 2px 7px; border-bottom-right-radius: 6px; z-index: 5;">3</span>
                  <img src="img/real-top3.jpg" alt="Chinelo feminino LUXO Strass" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <h3 style="font-size: 12.5px; font-weight: 500; color: #161823; line-height: 1.25; margin: 0 0 4px 0; height: 32px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                  Chinelo feminino LUX...
                </h3>
                <div style="margin-bottom: 3px;">
                  <span class="badge-frete-gratis">Frete grátis</span>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-start;">
                  <div class="price-current-tk">
                    <span>R$</span>39,53
                  </div>
                  <div class="price-old-tk">R$ 59,90</div>
                </div>
                <div style="font-size: 11px; color: #888; margin-top: 2px;">8967 vendido(s)</div>
              </a>
            </div>

            <!-- SEÇÃO NOVOS LANÇAMENTOS (IDÊNTICO AO PRINT) -->
            <div style="margin-top: 8px;">
              <h2 style="font-size: 16px; font-weight: 700; color: #161823; margin: 0 0 12px 0;">Novos lançamentos</h2>
              
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: flex; gap: 12px; background: #fff; border-radius: 8px; align-items: center;">
                <div style="width: 110px; height: 110px; min-width: 110px; border-radius: 8px; overflow: hidden; background: #f7f7f7;">
                  <img src="img/real-novo.jpg" alt="Sandália feminino LIA Delicada" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <div style="flex: 1; display: flex; flex-direction: column; justify-content: space-between; height: 110px; padding: 2px 0;">
                  <div>
                    <h3 style="font-size: 13.5px; font-weight: 500; color: #161823; line-height: 1.3; margin: 0 0 4px 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                      Sandália feminino LIA Delicada, C...
                    </h3>
                    <div style="margin-bottom: 6px;">
                      <span class="badge-frete-gratis">Frete grátis</span>
                    </div>
                  </div>
                  <div style="display: flex; align-items: flex-end; justify-content: space-between; width: 100%;">
                    <div style="display: flex; flex-direction: column; align-items: flex-start;">
                      <div class="price-current-tk">
                        <span>R$</span>25,95
                      </div>
                      <div style="display: flex; align-items: center; gap: 4px; margin-top: 2px;">
                        <span class="price-old-tk">R$ 49,90</span>
                        <span style="background: #ffebee; color: #fe2c55; font-size: 10px; font-weight: 700; padding: 1px 4px; border-radius: 3px;">-48%</span>
                      </div>
                    </div>
                    <div class="unified-action-btn">
                      <div class="unified-cart-side" onclick="event.preventDefault(); event.stopPropagation(); window.openProductModalDirectly('pages/produto-104.html');">
                        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#fe2c55" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="9" cy="21" r="1"></circle>
                          <circle cx="20" cy="21" r="1"></circle>
                          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                        </svg>
                      </div>
                      <div class="unified-buy-side" onclick="event.stopPropagation(); window.location.href='pages/produto-104.html';">
                        Comprar
                      </div>
                    </div>
                  </div>
                </div>
              </a>
            </div>
          </div>

          <!-- PRODUTOS RECOMENDADOS -->
          <div style="background: white; padding: 14px 16px;" id="produtos-recomendados-section">
            <div class="divider-home-rec">Recomendado para você</div>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;" id="recommended-grid">`;

const pStart = html.indexOf('<!-- PRINCIPAIS PRODUTOS -->');
const rEnd = html.indexOf('<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;" id="recommended-grid">') + '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;" id="recommended-grid">'.length;

html = html.slice(0, pStart) + principaisSectionHtml + html.slice(rEnd);

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ UI 100% idêntica reconstruída!');
