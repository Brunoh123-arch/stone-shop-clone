const fs = require('fs');
const path = require('path');

const appJsPath = path.join(__dirname, '..', 'js', 'app.js');
let appJs = fs.readFileSync(appJsPath, 'utf8');

const startMarker = '<div id="variacoes-modal">';
const endMarker = '<div class="var-modal-body">';

const idx1 = appJs.indexOf(startMarker);
const idx2 = appJs.indexOf(endMarker, idx1);

if (idx1 !== -1 && idx2 !== -1) {
  const replacement = `<div id="variacoes-modal">
      <div class="var-modal-header">
        <img class="var-modal-img" src="\${getImg()}" alt="\${produto.nome}" onerror="this.src='https://via.placeholder.com/80'">
        <div class="var-modal-info">
          <div class="var-modal-preco-row">
            \${descPercent ? \`<span class="var-modal-desc-badge">-\${descPercent}%</span>\` : ''}
            <div class="var-modal-preco" id="var-modal-preco-val">R$ \${preco}</div>
            <svg viewBox="0 0 667 534" fill="none" xmlns="http://www.w3.org/2000/svg" width="16" height="13" style="flex-shrink:0; margin-left:2px;">
              <path d="M666.666 166.667C640.145 166.667 614.71 177.203 595.956 195.956C577.202 214.71 566.666 240.145 566.666 266.667C566.666 293.189 577.202 318.624 595.956 337.378C614.71 356.131 640.145 366.667 666.666 366.667L666.666 466.667C666.666 484.348 659.642 501.305 647.14 513.808C634.637 526.31 617.681 533.334 600 533.334L466.666 533.334L466.666 470.601C466.666 461.76 463.154 453.281 456.903 447.03C450.652 440.779 442.174 437.267 433.333 437.267C424.492 437.267 416.014 440.779 409.763 447.03C403.512 453.281 400 461.76 400 470.601L400 533.334L66.666 533.334C48.9852 533.334 32.0287 526.31 19.5264 513.808C7.02395 501.305 1.13666e-05 484.348 1.01189e-05 466.667L1.44901e-05 366.666C55.4279 366.576 100.333 266.167 100.333 266.167C100.333 210.718 55.4279 165.758 2.3276e-05 165.668L2.76035e-05 66.667C3.0397e-05 48.9859 7.02397 32.0288 19.5264 19.5264C32.0287 7.02422 48.9852 8.86041e-05 66.666 4.76048e-07L400 1.50465e-05L400 62.7334C400 71.5739 403.512 80.0525 409.763 86.3037C416.014 92.5549 424.492 96.0674 433.333 96.0674C442.174 96.0674 450.652 92.5549 456.903 86.3037C463.154 80.0525 466.666 71.5739 466.666 62.7334L466.666 1.79606e-05L600 2.37888e-05C617.681 0.000113468 634.637 7.02425 647.14 19.5264C659.642 32.0288 666.666 48.9859 666.666 66.667L666.666 166.667Z" fill="#D60643"/>
            </svg>
          </div>
          \${produto.precoOrig ? \`<div class="var-modal-preco-orig" id="var-modal-preco-orig-val" style="font-size: 13px; color: #999; text-decoration: line-through; margin-bottom: 4px; line-height: 1; margin-top: -2px;">R$ \${produto.precoOrig}</div>\` : \`<div class="var-modal-preco-orig" id="var-modal-preco-orig-val" style="display:none; font-size: 13px; color: #999; text-decoration: line-through; margin-bottom: 4px; line-height: 1; margin-top: -2px;"></div>\`}
          <div class="var-modal-preco-unit" style="display:none;" id="var-modal-preco-unit-val">\${produto.preco}</div>
          <div class="var-modal-nome">\${produto.nome}</div>
        </div>
        <button class="var-close-btn" onclick="closeVariacaoModal()">✕</button>
      </div>

      <!-- BANNER 11.11 LIQUIDAÇÃO OFICIAL TIKTOK SHOP (IMAGEM 1 / IMAGEM 3) -->
      <div class="var-modal-banner-1111">
        <img src="/img/banner-1111-modal.png" onerror="this.src='../img/banner-1111-modal.png'" alt="11.11 Liquidação">
      </div>\n\n      `;

  appJs = appJs.slice(0, idx1) + replacement + appJs.slice(idx2);
  fs.writeFileSync(appJsPath, appJs, 'utf8');
  console.log('✅ HTML do modal substituído com sucesso incluindo o banner 11.11!');
} else {
  console.error('❌ Não foi possível encontrar os marcadores do modal no app.js');
}
