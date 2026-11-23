const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// O trecho entre '<!-- COUPONS CONTAINER -->' e '<!-- NAV TABS -->'
const sIdx = html.indexOf('<!-- COUPONS CONTAINER -->');
const eIdx = html.indexOf('<!-- NAV TABS -->');

console.log('Tamanho da sujeira:', eIdx - sIdx);

// O bloco correto e limpo do cupom:
const cleanCoupons = `<!-- COUPONS CONTAINER -->
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
          </div>\n\n          `;

// Substitui com precisão cirúrgica de sIdx até eIdx
html = html.slice(0, sIdx) + cleanCoupons + html.slice(eIdx);

// Agora vamos checar se a subbarra de produtos está sendo controlada perfeitamente
fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ index.html limpo com sucesso! Tags sobrando removidas.');
