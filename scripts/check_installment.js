const fs = require('fs');
const html104 = fs.readFileSync('pages/produto-104.html', 'utf8');
const match = html104.match(/<div class="installment-row"[\s\S]*?<\/div>/);
console.log('--- produto-104 installment-row ---');
console.log(match ? match[0] : 'not found');

const html100 = fs.readFileSync('pages/produto-100.html', 'utf8');
const match100 = html100.match(/<div class="installment-row"[\s\S]*?<\/div>/);
console.log('--- produto-100 installment-row ---');
console.log(match100 ? match100[0] : 'not found');
