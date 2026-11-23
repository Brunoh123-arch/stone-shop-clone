const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

html = html.replace('<div produtos-recomendados-section">', '<div style="background: white; padding: 16px;" id="produtos-recomendados-section">');

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ Corrigido tag produtos-recomendados-section!');
