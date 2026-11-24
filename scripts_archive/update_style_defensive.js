const fs = require('fs');
let css = fs.readFileSync('css/style.css', 'utf8');

// Replace .price-currency-sign, .price-label-apartir
css = css.replace(
  '.price-currency-sign, .price-label-apartir {',
  '.price-left { display: contents !important; }\n.price-label-apartir { display: none !important; }\n\n.price-currency-sign {'
);

fs.writeFileSync('css/style.css', css, 'utf8');
console.log('Defensive CSS added to style.css');
