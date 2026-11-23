const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

// Target block
const oldBlockRegex = /<div style="display: grid; grid-template-columns: repeat\(3, 1fr\); gap: 8px;">[\s\S]*?<!-- SEÇÃO NOVOS LANÇAMENTOS/;

const newBlock = `<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;">
              <!-- TOP 1 -->
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: block;">
                <div style="position: relative; background: white;">
                  <span style="position: absolute; top: 0; left: 0; background: #ecd299; color: #523910; font-size: 11px; font-weight: 800; padding: 2px 7px; border-bottom-right-radius: 6px; z-index: 5;">1</span>
                  <img src="img/ranking-top1.webp" alt="Chinelo feminino Cruzada Glitter" loading="eager"
                    onerror="this.src='https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/937eda3788b14961af3dc12028a4c886~tplv-aphluv4xwc-resize-webp:800:800.webp'"
                    style="width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; margin-bottom: 6px; display: block; background: #f5f5f5;">
                  <h3 class="principais-prod-title">Chinelo feminino Cruz...</h3>
                  <div style="margin-bottom: 4px;">
                    <span class="badge-frete-gratis">Frete grátis</span>
                  </div>
                  <div class="principais-price-stack">
                    <div class="principais-price-cur"><span class="currency">R$</span> 19,90</div>
                    <div style="display: flex; align-items: center; gap: 4px; margin-top: 1.5px;">
                      <div class="principais-price-old">R$ 59,90</div>
                      <span style="background: #ffe8ee; color: #ff2b56; font-size: 10px; font-weight: 700; padding: 1px 4px; border-radius: 3px; line-height: 1;">-67%</span>
                    </div>
                  </div>
                  <div class="principais-sales-txt">14.1K vendido(s)</div>
                </div>
              </a>

              <!-- TOP 2 -->
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: block;">
                <div style="position: relative; background: white;">
                  <span style="position: absolute; top: 0; left: 0; background: #cbd5e1; color: #334155; font-size: 11px; font-weight: 800; padding: 2px 7px; border-bottom-right-radius: 6px; z-index: 5;">2</span>
                  <img src="img/ranking-top2.webp" alt="Chinelo feminino NO STRASS Verão" loading="eager"
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
                  <span style="position: absolute; top: 0; left: 0; background: #d9b89d; color: #4a2c16; font-size: 11px; font-weight: 800; padding: 2px 7px; border-bottom-right-radius: 6px; z-index: 5;">3</span>
                  <img src="img/ranking-top3.webp" alt="Chinelo feminino LUXO STRASS" loading="eager"
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
          </div>

          <!-- SEÇÃO NOVOS LANÇAMENTOS`;

if (oldBlockRegex.test(html)) {
  html = html.replace(oldBlockRegex, newBlock);
  fs.writeFileSync(indexPath, html, 'utf8');
  console.log('✅ Principais produtos atualizado com imagens anteriores e -67% R$ 19,90!');
} else {
  console.error('❌ Não encontrou o bloco de Principais produtos para substituir!');
  process.exit(1);
}
