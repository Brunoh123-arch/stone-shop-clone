const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const rStart = html.indexOf('id="recommended-grid"');
const card1Start = html.indexOf('<a class="product-card-rec"', rStart);
const card1End = html.indexOf('</a>', card1Start) + 4;

console.log('--- ESTRUTURA ATUAL DO CARD 1 ---');
console.log(html.slice(card1Start, card1End));
