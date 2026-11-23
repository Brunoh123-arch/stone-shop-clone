const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

console.log('>>> [BRUNO CTO] AJUSTE CIRÚRGICO: LOJA ESTRELA EM NEGRITO E CUPOM COM OPACIDADE EXATA <<<');

// 1. ATUALIZAR O MARKUP DA SEÇÃO DA LOJA E CUPOM
const officialStoreAndCoupon = `<div class="store-section">
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
                  <div style="margin-bottom: 3px;">
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

          <!-- CUPOM DENTRO DA ÁREA DA LOJA (COM OPACIDADE E QUEBRA DE LINHA IDÊNTICA AO PRINT) -->
          <div class="coupons-container">
            <div class="coupon-card-official">
              <div class="coupon-text-left">
                <div class="coupon-title">Cupom de envio</div>
                <div class="coupon-sub">
                  em pedidos acima de R$<br>109
                </div>
              </div>
              <div class="coupon-resgatado-txt">Resgatado</div>
            </div>
          </div>`;

const storeStart = html.indexOf('<div class="store-section">');
const navTabsStart = html.indexOf('<!-- NAV TABS -->');
if (storeStart !== -1 && navTabsStart !== -1) {
  html = html.slice(0, storeStart) + officialStoreAndCoupon + '\n\n          ' + html.slice(navTabsStart);
  console.log('✅ Markup da loja e cupom atualizado com sucesso!');
}

// 2. ATUALIZAR O CSS DO BADGE LOJA ESTRELA E DO TEXTO RESGATADO
const headerCouponCss = `
    /* === AJUSTE DE ALTA FIDELIDADE: LOJA ESTRELA E CUPOM COM OPACIDADE === */
    .badge-loja-estrela {
      display: inline-flex !important;
      align-items: center !important;
      background: #fde5be !important;
      color: #222222 !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif !important;
      padding: 2.5px 7px !important;
      border-radius: 4px !important;
      line-height: 1.1 !important;
      letter-spacing: -0.2px !important;
    }

    .coupon-card-official {
      background: #ebf7f5 !important;
      border: 1px solid #d8f1ec !important;
      border-radius: 8px !important;
      padding: 9px 14px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
    }

    .coupon-title {
      font-size: 13px !important;
      font-weight: 700 !important;
      color: #161823 !important;
      line-height: 1.2 !important;
    }

    .coupon-sub {
      font-size: 11px !important;
      color: #757575 !important;
      line-height: 1.3 !important;
      margin-top: 2px !important;
    }

    .coupon-resgatado-txt {
      font-size: 13px !important;
      font-weight: 500 !important;
      color: #48cfbe !important;
      opacity: 0.55 !important;
      letter-spacing: -0.1px !important;
    }
`;

html = html.replace('</head>', `<style>\n${headerCouponCss}\n</style>\n</head>`);

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ index.html gravado com as novas definições de Loja Estrela e Cupom!');
