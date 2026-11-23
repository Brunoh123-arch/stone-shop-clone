const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const rStart = html.indexOf('id="recommended-grid"');
const catStart = html.indexOf('id="categorias-section"');

const gridContent = html.slice(rStart, catStart);
const cardMatches = [...gridContent.matchAll(/<a class="product-card-rec"([\s\S]*?)<\/a>/g)];

cardMatches.slice(0, 3).forEach((m, i) => {
  const c = m[0];
  const priceM = c.match(/class="product-price"[\s\S]*?<\/div>/);
  console.log(`[Card ${i + 1} Price Markup]:`, priceM ? priceM[0] : 'not found');
});
