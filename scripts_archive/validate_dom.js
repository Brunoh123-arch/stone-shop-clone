const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Conta divs abertas e fechadas no body
const bodyStart = html.indexOf('<body');
const bodyEnd = html.indexOf('</body>');
const bodyHtml = html.slice(bodyStart, bodyEnd);

const openDivs = (bodyHtml.match(/<div(\s|>)/gi) || []).length;
const closeDivs = (bodyHtml.match(/<\/div>/gi) || []).length;

console.log('Divs abertas no body:', openDivs);
console.log('Divs fechadas no body:', closeDivs);
console.log('Diferença:', openDivs - closeDivs);

// Verifica se os IDs principais existem
['root', 'principais-produtos-section', 'produtos-recomendados-section', 'recommended-grid', 'subfilter-produtos-bar'].forEach(id => {
  console.log(`ID #${id}:`, html.includes(`id="${id}"`));
});
