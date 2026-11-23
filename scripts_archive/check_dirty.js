const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('<!-- COUPONS CONTAINER -->');
const eIdx = html.indexOf('class="nav-tabs"');

console.log('--- TRECHO ENTRE COUPONS E NAV-TABS ---');
console.log(html.slice(sIdx, eIdx + 50));
