const fs = require('fs');
const path = require('path');

const baseDir = path.resolve(__dirname, '..');
const pagesDir = path.join(baseDir, 'pages');

console.log('--- Padronizando páginas de produtos (pages/produto-*.html) ---');
const files = fs.readdirSync(pagesDir).filter(f => f.startsWith('produto-') && f.endsWith('.html'));

let updated = 0;
files.forEach(file => {
  const filePath = path.join(pagesDir, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let changed = false;

  // 1. Limpar inline margin da installment-row
  if (html.includes('class="installment-row"')) {
    html = html.replace(/class="installment-row"\s+style="([^"]*)"/g, (match, style) => {
      let cleanStyle = style.replace(/margin:[^;]+;?/gi, '').trim();
      return `class="installment-row" style="${cleanStyle}"`;
    });
    changed = true;
  }

  // 2. Limpar inline margin da discount-ticket
  if (html.includes('class="discount-ticket"')) {
    html = html.replace(/class="discount-ticket"\s+style="([^"]*)"/g, (match, style) => {
      let cleanStyle = style.replace(/margin:[^;]+;?/gi, '').trim();
      return `class="discount-ticket" style="${cleanStyle}"`;
    });
    changed = true;
  }

  // 3. Limpar inline style de product-info-rows (deixa o CSS assumir o border-top/bottom de 8px solid #f8f8f8)
  if (html.includes('class="product-info-rows"')) {
    html = html.replace(/class="product-info-rows"\s+style="[^"]*"/g, 'class="product-info-rows"');
    changed = true;
  }

  // 4. Inverter hierarquia de frete: Line 1 = Receba até, Line 2 = Frete grátis R$ 15,60
  const freteRegex = /<div class="info-row-text-group">[\s\S]*?<span[^>]*>[^<]*Frete[\s\S]*?<\/span>[\s\S]*?<\/div>[\s\S]*?<span class="info-row-subtitle"[^>]*>([\s\S]*?)<\/span>[\s\S]*?<\/div>/;
  if (freteRegex.test(html)) {
    html = html.replace(freteRegex, (match, dataTexto) => {
      const cleanData = dataTexto.trim();
      const finalData = cleanData.startsWith('Receba') ? cleanData : `Receba em poucos dias`;
      return `<div class="info-row-text-group" style="display: flex; flex-direction: column; gap: 3px;">
              <span class="info-row-title" style="font-size: 13.5px; font-weight: 500; color: #161823;">${finalData}</span>
              <div style="display: flex; align-items: center; gap: 6px;">
                <span style="background: #e6f8f6; color: #00bfa5; font-size: 10.5px; font-weight: 700; padding: 1px 5px; border-radius: 2px;">Frete grátis</span>
                <span style="font-size: 12px; color: #888; text-decoration: line-through;">R$ 15,60</span>
              </div>
            </div>`;
    });
    changed = true;
  }

  // 5. Remover ícone de grade na linha de opções
  const targetIcon = /<div class="info-row-icon">\s*<svg width="18" height="18" viewBox="0 0 24 24"[\s\S]*?<\/svg>\s*<\/div>/g;
  if (targetIcon.test(html)) {
    html = html.replace(targetIcon, '');
    changed = true;
  }

  if (changed) {
    fs.writeFileSync(filePath, html, 'utf8');
    updated++;
  }
});

console.log(`✅ ${updated} páginas de produtos atualizadas com sucesso!`);
