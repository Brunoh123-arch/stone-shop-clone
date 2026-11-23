const fs = require('fs');
const path = require('path');

function fixWorkspace(wsDir) {
  const pagesDir = path.join(wsDir, 'pages');
  if (!fs.existsSync(pagesDir)) return;

  const files = fs.readdirSync(pagesDir).filter(f => f.startsWith('produto-') && f.endsWith('.html'));
  console.log(`Verificando ${files.length} produtos em ${wsDir}...`);

  let count = 0;
  for (const file of files) {
    const fullPath = path.join(pagesDir, file);
    let html = fs.readFileSync(fullPath, 'utf8');
    let modified = false;

    // 1. Consertar margem quebrada ou antiga no discount-ticket
    if (html.includes('discount-ticket')) {
      const fixedDiscountTicket = html.replace(
        /<div class="discount-ticket"\s+style="[^"]*"/g,
        '<div class="discount-ticket" style="margin: 0 0 6px 0; display: flex; align-items: center; justify-content: space-between; cursor: pointer;"'
      );
      if (fixedDiscountTicket !== html) {
        html = fixedDiscountTicket;
        modified = true;
      }
    }

    // 2. Padronizar installment-row
    const match = html.match(/<div class="installment-row"[\s\S]*?<\/div>/);
    if (match) {
      const oldInst = match[0];
      const valMatch = oldInst.match(/(\d+x\s*R\$\s*[\d,.]+)/i);
      const semJurosMatch = oldInst.match(/(sem juros)/i);
      
      const parcelamentoValor = valMatch ? valMatch[1] : '2x R$ 11,48';
      const semJurosTexto = semJurosMatch ? semJurosMatch[1] : 'sem juros';

      const newInst = `<div class="installment-row" style="display: flex; align-items: center; justify-content: space-between; font-size: 13px; color: #161823; margin: 0 0 5px 0; cursor: pointer;">
        <div style="display: inline-flex; align-items: center; gap: 5px;">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" style="flex-shrink: 0;">
            <rect x="2" y="4" width="20" height="13.5" rx="2" stroke="#161823" stroke-width="1.8" fill="none"/>
            <line x1="2" y1="8" x2="22" y2="8" stroke="#161823" stroke-width="1.8"/>
            <circle cx="16" cy="14" r="4.2" fill="#fff" stroke="#161823" stroke-width="1.8"/>
            <polyline points="16 11.8 16 14 18 14" stroke="#161823" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span style="font-weight: 500;">${parcelamentoValor}</span>
          <span style="color: #df3564; font-weight: 400; margin-left: 2px;">${semJurosTexto}</span>
        </div>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>`;

      if (oldInst !== newInst) {
        html = html.replace(oldInst, newInst);
        modified = true;
      }
    }

    if (modified) {
      fs.writeFileSync(fullPath, html, 'utf8');
      count++;
    }
  }

  console.log(`[OK] ${count} arquivos atualizados em ${pagesDir}`);

  // 3. Atualizar css/style.css
  const stylePath = path.join(wsDir, 'css', 'style.css');
  if (fs.existsSync(stylePath)) {
    let css = fs.readFileSync(stylePath, 'utf8');
    
    // Atualizar bloco de product-info e installment-row
    const oldCssBlock = /\.product-info\s*\{[^}]*padding:[^}]*\}/;
    css = css.replace(
      /\.product-info\s*\{[^}]*background:[^}]*padding:[^}]*\}/g,
      `.product-info {\n  background: var(--color-white) !important;\n  padding: 4px 14px 14px 14px !important;\n}`
    );

    css = css.replace(
      /\.installment-row\s*\{[^}]*\}/g,
      `.installment-row {\n  display: flex !important;\n  align-items: center !important;\n  justify-content: space-between !important;\n  font-size: 13px !important;\n  color: #161823 !important;\n  margin: 0 0 5px 0 !important;\n  cursor: pointer !important;\n  line-height: 1.3 !important;\n}`
    );

    css = css.replace(
      /\.discount-ticket\s*\{[^}]*\}/g,
      `.discount-ticket {\n  display: flex !important;\n  align-items: center !important;\n  justify-content: space-between !important;\n  gap: 6px !important;\n  margin: 0 0 6px 0 !important;\n  cursor: pointer !important;\n}`
    );

    fs.writeFileSync(stylePath, css, 'utf8');
    console.log(`[OK] style.css atualizado em ${wsDir}`);
  }
}

fixWorkspace('c:\\Users\\Dell\\Downloads\\ds');
fixWorkspace('c:\\Users\\Dell\\Downloads\\stone_shop_clone');
