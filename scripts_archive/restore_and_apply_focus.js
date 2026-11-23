const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
const originalPrincipais = fs.readFileSync('original_principais.html', 'utf8');

// 1. RESTAURAR A SEÇÃO STORE SECTION COM A LOGO ORIGINAL (./logo.png) E NOME STONE SHOP
const storeAndCouponHtml = `<div class="store-section">
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <div style="display: flex; align-items: center; gap: 10px;">
                <img src="./logo.png" alt="Stone Shop"
                  style="width: 58px; height: 58px; object-fit: cover; border-radius: 50%; border: 1px solid #f0f0f0;">
                <div>
                  <h2 style="display: flex; align-items: center; gap: 4px; font-size: 16px; font-weight: 700; color: #161823; margin: 0 0 3px 0; line-height: 1.2;">
                    Stone Shop
                    <svg viewBox="0 0 24 24" width="15" height="15" style="color:#0095f6; flex-shrink:0;" fill="currentColor">
                      <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                    </svg>
                  </h2>
                  <div style="margin-bottom: 2px;">
                    <span class="badge-loja-estrela">Loja Estrela</span>
                  </div>
                  <div style="font-size: 12px; color: #161823; font-weight: 400;">
                    112.2K vendido(s)
                  </div>
                </div>
              </div>
              <div style="display: flex; flex-direction: column; gap: 6px; align-items: flex-end;">
                <button style="background: #fe2c55; color: #fff; border: none; height: 32px; padding: 0 20px; border-radius: 16px; font-size: 13px; font-weight: 700; cursor: pointer;">Seguir</button>
                <button style="background: #f1f1f2; color: #161823; border: none; height: 32px; padding: 0 16px; border-radius: 16px; font-size: 13px; font-weight: 600; cursor: pointer;" onclick="openSmartChat()">Mensagem</button>
              </div>
            </div>
          </div>

          <!-- CUPOM DENTRO DA ÁREA DA LOJA (SEM CORTES, RESGATADO EM VERDE-ÁGUA) -->
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

// 2. RESTAURAR A SEÇÃO "PRINCIPAIS PRODUTOS" ORIGINAL (COM AS IMAGENS ORIGINAIS QUE ESTAVAM LÁ)
// Aplicando nela os badges suaves de Frete Grátis e preços corretos
let tunedPrincipais = originalPrincipais;

// Substituir a classe de badge de frete grátis antiga pelo badge ciano suave oficial
tunedPrincipais = tunedPrincipais.replace(/class="product-badge"/g, 'class="badge-frete-gratis"');

// Atualizar a seção de principais produtos no html
const pStart = html.indexOf('<!-- PRINCIPAIS PRODUTOS -->');
const rEnd = html.indexOf('<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;" id="recommended-grid">') + '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;" id="recommended-grid">'.length;

const cleanRecHeader = `<!-- PRODUTOS RECOMENDADOS -->
          <div style="background: white; padding: 14px 16px;" id="produtos-recomendados-section">
            <div class="divider-home-rec">Recomendado para você</div>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;" id="recommended-grid">`;

html = html.slice(0, pStart) + '<!-- PRINCIPAIS PRODUTOS -->\n          ' + tunedPrincipais + '\n\n          ' + cleanRecHeader + html.slice(rEnd);

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ Imagens originais restauradas com foco total nos elementos de cupom, frete grátis e texto!');
