const fs = require('fs');
const html = fs.readFileSync('real.html', 'utf8');

const prods = [
  'Esteira Elétrica',
  'Scooter Elétrica',
  'JBL Boombox',
  'Pneus Pirelli',
  'Lava e Seca'
];

prods.forEach(p => {
  const idx = html.indexOf(p);
  const block = html.slice(idx, idx + 1200);
  console.log('=== ' + p + ' ===');
  const m = block.match(/<div class="product-price">[\s\S]*?<\/div>/);
  if (m) console.log(m[0]);
  const b = block.match(/<span class="product-badge-discount">[\s\S]*?<\/span>/);
  if (b) console.log(b[0].replace(/<svg[\s\S]*?<\/svg>/, '[SVG]'));
});
