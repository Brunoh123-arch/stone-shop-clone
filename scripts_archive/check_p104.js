const fs = require('fs');
const html = fs.readFileSync('pages/produto-104.html', 'utf8');

const sIdx = html.indexOf('<div class="product-info"');
console.log(html.slice(sIdx, sIdx + 1500));
