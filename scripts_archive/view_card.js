const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const rStart = html.indexOf('id="recommended-grid"');
const firstCard = html.indexOf('<a class="product-card-rec"', rStart);
const secondCard = html.indexOf('<a class="product-card-rec"', firstCard + 10);

console.log('=== PRIMEIRO CARD EM RECOMMENDED GRID ===');
console.log(html.slice(firstCard, secondCard));
