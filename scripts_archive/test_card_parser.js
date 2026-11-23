const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const rStart = html.indexOf('id="recommended-grid"');
const catStart = html.indexOf('id="categorias-section"');

const gridContent = html.slice(rStart, catStart);
const cardMatches = [...gridContent.matchAll(/<a class="product-card-rec"([\s\S]*?)<\/a>/g)];

console.log('Total de cards parseados:', cardMatches.length);

// Amostra do card 1 parseado
const c1 = cardMatches[0][0];
const hrefM = c1.match(/href="([^"]+)"/);
const catM = c1.match(/data-cat="([^"]+)"/);
const imgM = c1.match(/<img[^>]+src="([^"]+)"/);
const nameM = c1.match(/<h3[^>]*>([\s\S]*?)<\/h3>/);
const priceCurM = c1.match(/class="current-price"[^>]*>([\s\S]*?)<\/span>/);
const priceOldM = c1.match(/class="old-price"[^>]*>([\s\S]*?)<\/span>/);
const salesM = c1.match(/class="product-sales"[^>]*>([\s\S]*?)<\/div>/);

console.log({
  href: hrefM ? hrefM[1] : null,
  cat: catM ? catM[1] : null,
  img: imgM ? imgM[1] : null,
  name: nameM ? nameM[1].trim() : null,
  priceCur: priceCurM ? priceCurM[1].replace(/<[^>]+>/g, '').trim() : null,
  priceOld: priceOldM ? priceOldM[1].trim() : null,
  sales: salesM ? salesM[1].replace(/<[^>]+>/g, '').trim() : null
});
