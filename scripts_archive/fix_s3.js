const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

html = html.replace(/\s*initShareTooltip\(\);\s*\}\);/g, `
    document.addEventListener('DOMContentLoaded', () => {
      initShareTooltip();
    });`);

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ Sintaxe do Script 3 corrigida!');
