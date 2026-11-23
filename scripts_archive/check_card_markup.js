const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const rStart = html.indexOf('id="recommended-grid"');
const card1 = html.indexOf('<a class="product-card-rec"', rStart);
const card2 = html.indexOf('<a class="product-card-rec"', card1 + 10);
const card3 = html.indexOf('<a class="product-card-rec"', card2 + 10);

console.log('CARD 1:\n' + html.slice(card1, card2));
console.log('CARD 2:\n' + html.slice(card2, card3));
