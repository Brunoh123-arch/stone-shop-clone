const fs = require('fs');
const path = require('path');

['c:/Users/Dell/Downloads/ds/pages', 'c:/Users/Dell/Downloads/stone_shop_clone/pages'].forEach(dir => {
  const files = fs.readdirSync(dir).filter(f => f.startsWith('produto-') && f.endsWith('.html'));
  files.forEach(f => {
    const p = path.join(dir, f);
    let html = fs.readFileSync(p, 'utf8');
    
    // Procura por duplicata de svg fechamento logo apos installment-row
    const doubleSvgRegex = /(<div class="installment-row"[\s\S]*?<\/div>)\s*<svg width="13" height="13"[\s\S]*?<\/div>/;
    if (doubleSvgRegex.test(html)) {
      html = html.replace(doubleSvgRegex, '$1');
      fs.writeFileSync(p, html, 'utf8');
      console.log('Duplicata corrigida em', p);
    }
  });
});
