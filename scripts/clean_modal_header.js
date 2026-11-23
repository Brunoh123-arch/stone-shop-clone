const fs = require('fs');
const path = require('path');

const appJsPath = path.join(__dirname, '..', 'js', 'app.js');
let appJs = fs.readFileSync(appJsPath, 'utf8');

// 1. descPercent
const oldDesc = /let descPercent = produto\.desc \|\| produto\.desconto \|\| '';[\s\S]*?if \(!descPercent\) \{[\s\S]*?\}\s*\}/;
const newDesc = `let descPercent = produto.desc || produto.desconto || '';
  if (!descPercent) {
    const badgeEl = document.querySelector('.discount-badge-white') || document.querySelector('.flash-discount-badge');
    if (badgeEl) descPercent = badgeEl.textContent.replace(/[^0-9]/g, '');
  }
  if (!descPercent && produto.precoOrig && produto.preco) {
    const orig = parseFloat(String(produto.precoOrig).replace(/\\./g, '').replace(',', '.'));
    const atual = parseFloat(String(produto.preco).replace(/\\./g, '').replace(',', '.'));
    if (orig > atual) {
      descPercent = Math.round(((orig - atual) / orig) * 100);
    }
  }
  if (descPercent) {
    descPercent = String(descPercent).replace(/[^0-9]/g, '');
  }`;

if (oldDesc.test(appJs)) {
  appJs = appJs.replace(oldDesc, newDesc);
  console.log('✅ descPercent atualizado com sucesso');
} else {
  console.log('❌ descPercent regex não bateu');
}

// 2. internal styles
const oldInternalStyles = /\.var-modal-header\s*\{[\s\S]*?align-items:\s*flex-start;\s*\}/;
const newInternalStyles = `.var-modal-header {
        display: flex;
        gap: 12px;
        padding: 16px 16px 8px;
        border-bottom: none;
        align-items: center;
      }
      .var-modal-img {
        width: 72px;
        height: 72px;
        object-fit: cover;
        border-radius: 8px;
        background: #f5f5f5;
        flex-shrink: 0;
      }
      .var-modal-info {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      .var-modal-preco-row {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 2px;
      }
      .var-modal-desc-badge {
        background: #ff2b56;
        color: #ffffff;
        font-size: 13px;
        font-weight: 700;
        padding: 1.5px 5.5px;
        border-radius: 4px;
        line-height: 1.2;
        display: inline-block;
      }
      .var-modal-preco {
        display: inline-flex;
        align-items: baseline;
        color: #ff2b56;
        font-weight: 700;
        line-height: 1;
      }
      .var-modal-currency {
        font-size: 14px;
        font-weight: 700;
        margin-right: 2px;
      }
      .var-modal-int {
        font-size: 22px;
        font-weight: 700;
      }
      .var-modal-cents {
        font-size: 15px;
        font-weight: 700;
      }
      .var-modal-preco-orig {
        font-size: 13px;
        color: #8a8b91;
        text-decoration: line-through;
        margin: 0;
        line-height: 1.2;
      }
      .var-modal-nome {
        display: none !important;
      }`;

if (oldInternalStyles.test(appJs)) {
  appJs = appJs.replace(oldInternalStyles, newInternalStyles);
  console.log('✅ internal styles atualizados com sucesso');
} else {
  console.log('❌ internal styles regex não bateu');
}

fs.writeFileSync(appJsPath, appJs, 'utf8');
console.log('✅ js/app.js gravado!');
