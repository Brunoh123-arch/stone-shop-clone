const fs = require('fs');
const path = require('path');

const dsDir = 'C:/Users/Dell/Downloads/ds';
const cloneDir = 'C:/Users/Dell/Downloads/stone_shop_clone';

// 1. Update js/catalogo.js in both dirs
const item105 = `  {id:105,nome:'Projetor HY300 Original Portátil Smart Android 11 4K Ultra HD HDMI Wifi Bluetooth Alto',preco:39.9,precoOrig:'399,90',desc:90,vendidos:14829,img:'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/81525a24b6074e6c87b673c8cc37d237~tplv-aphluv4xwc-resize-webp:800:800.webp'},`;

[dsDir, cloneDir].forEach(base => {
  const catPath = path.join(base, 'js', 'catalogo.js');
  let content = fs.readFileSync(catPath, 'utf8');
  if (!content.includes('id:105,')) {
    content = content.replace('const CATALOGO_PRODUTOS = [', `const CATALOGO_PRODUTOS = [\n${item105}`);
    fs.writeFileSync(catPath, content, 'utf8');
    console.log('Registered in:', catPath);
  }
});

// 2. Insert card in index.html in ds and clone
const card105 = `              <!-- PRODUTO 105 -->
              <a class="product-card-rec" href="pages/produto-105.html" data-cat="Eletrônicos" data-nome="projetor hy300 original portatil smart android 11 4k ultra hd hdmi wifi bluetooth alto" data-vendas="14829" data-id="105" style="text-decoration: none; color: inherit;">
                <div class="card-inner-box">
                  <img src="https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/81525a24b6074e6c87b673c8cc37d237~tplv-aphluv4xwc-resize-webp:800:800.webp" alt="Projetor HY300 Original Smart 4K" loading="lazy" class="card-thumb-img" referrerpolicy="no-referrer">
                  <div class="card-details-col">
                    <div class="card-top-info">
                      <h3 class="product-name">Projetor HY300 Original Portátil Smart Android 11 4K Ultra HD HDMI Wifi Bluetooth Alto</h3>
    <!-- TAG OFERTA RELÂMPAGO -->
    <div class="badge-flash-tag" style="display: inline-flex !important; align-items: stretch !important; height: 18px !important; border-radius: 9px !important; overflow: hidden !important; margin: 3px 0 2px 0 !important; width: fit-content !important; box-sizing: border-box !important;">
    <span style="background: #ff4800 !important; color: #ffffff !important; display: inline-flex !important; align-items: center !important; gap: 3px !important; padding: 0 6px 0 6px !important; font-size: 9.5px !important; font-weight: 800 !important; line-height: 1 !important; white-space: nowrap !important;">
      <svg viewBox="0 0 24 24" width="10" height="10" fill="#ffffff" style="flex-shrink: 0 !important;">
        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
      </svg>
      Oferta Relâmpago
    </span>
    <span style="background: #ffebe5 !important; color: #ff4800 !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; padding: 0 6px !important; font-size: 9.5px !important; font-weight: 800 !important; line-height: 1 !important; white-space: nowrap !important; font-variant-numeric: tabular-nums !important;">
      19:46:52
    </span>
  </div>
  
                      <div class="card-badges-row">
                        <span class="badge-frete-gratis">Frete grátis</span>
                        <span class="related-discount" style="background: #fff0f2; color: #fe2c55; border: 1px solid #ffd8e0; font-size: 9px; font-weight: 700; padding: 0.5px 3px; border-radius: 2px; line-height: 1.2;">-90%</span>
                      </div>
                      
                    </div>
                      <div class="card-rating-row"><span class="star-yellow">★</span> <span class="rating-num">4.9</span> <span class="rating-pipe">|</span> <span class="sales-count-txt">14.8K vendido(s)</span></div><div class="card-bottom-action-row">
                      <div class="price-stack-col">
                        <div class="price-current-txt"><span class="currency">R$</span> 39,90</div>
                        <div class="price-old-txt">R$ 399,90</div>
                      </div>
                      <div class="btn-cart-circle" style="width: 32px !important; height: 32px !important; min-width: 32px !important; min-height: 32px !important; border-radius: 50% !important; background: #ffe8ee !important; display: flex !important; align-items: center !important; justify-content: center !important; cursor: pointer !important; border: none !important; flex-shrink: 0 !important;" aria-label="Adicionar ao carrinho">
  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#fe2c55" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="9" cy="21" r="1"></circle>
    <circle cx="20" cy="21" r="1"></circle>
    <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
  </svg>
</div>
                    </div>
                  </div>
                </div>
              </a>\n`;

[dsDir, cloneDir].forEach(base => {
  const indexPath = path.join(base, 'index.html');
  let html = fs.readFileSync(indexPath, 'utf8');
  if (!html.includes('data-id="105"')) {
    html = html.replace('<!-- PRODUTO 104 -->', card105 + '              <!-- PRODUTO 104 -->');
    fs.writeFileSync(indexPath, html, 'utf8');
    console.log('Inserted card in:', indexPath);
  }
});

// 3. Cache buster update
const timestamp = Date.now();
const busterRegex = /videos-criadores\.js(?:\?v=\w+)?/g;
const busterReplacement = `videos-criadores.js?v=${timestamp}`;

function updateBusters(dir) {
  const files = fs.readdirSync(dir);
  for (const f of files) {
    const full = path.join(dir, f);
    if (fs.statSync(full).isDirectory()) {
      if (f !== 'node_modules' && f !== '.git' && f !== 'Temp') {
        updateBusters(full);
      }
    } else if (f.endsWith('.html')) {
      let content = fs.readFileSync(full, 'utf8');
      if (busterRegex.test(content)) {
        content = content.replace(busterRegex, busterReplacement);
        fs.writeFileSync(full, content, 'utf8');
      }
    }
  }
}

updateBusters(dsDir);
updateBusters(cloneDir);
console.log('Cache busters updated with timestamp:', timestamp);

// 4. Synchronize index.html to real.html, stone.html, api/stone_content.js
const masterIndex = fs.readFileSync(path.join(cloneDir, 'index.html'), 'utf8');

[cloneDir, dsDir].forEach(base => {
  fs.writeFileSync(path.join(base, 'real.html'), masterIndex, 'utf8');
  fs.writeFileSync(path.join(base, 'stone.html'), masterIndex, 'utf8');
  const apiFile = path.join(base, 'api', 'stone_content.js');
  if (fs.existsSync(path.dirname(apiFile))) {
    fs.writeFileSync(apiFile, `module.exports = ${JSON.stringify(masterIndex)};\n`, 'utf8');
  }
});

console.log('Synchronized real.html, stone.html, and api/stone_content.js across all workspaces!');
