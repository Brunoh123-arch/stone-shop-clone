const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('<div class="store-section">');
const eIdx = html.indexOf('<!-- COUPONS CONTAINER -->');

console.log('--- TRECHO ATUAL DA STORE SECTION ---');
console.log(html.slice(sIdx, eIdx));

const cleanStoreSection = `<div class="store-section">
            <div class="store-left">
              <div class="store-logo">
                <img src="./logo.png" alt="Stone Shop"
                  style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">
              </div>
              <div class="store-info">
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
              </div>
            </div>
            <div class="store-buttons">
              <button class="store-follow-btn">Seguir</button>
              <button class="store-message-btn" onclick="openSmartChat()">Mensagem</button>
            </div>
          </div>\n\n          `;

html = html.slice(0, sIdx) + cleanStoreSection + html.slice(eIdx);

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ store-section reestruturada e limpa perfeitamente!');
