const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('<!-- COUPONS CONTAINER -->');
const eIdx = html.indexOf('<!-- NAV TABS -->');

console.log('sIdx:', sIdx, 'eIdx:', eIdx);
console.log('--- CONTEÚDO ATUAL ENTRE COUPONS E NAV TABS ---');
console.log(html.slice(sIdx, eIdx));
