const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('<!-- COUPONS CONTAINER -->');
console.log(html.slice(sIdx, sIdx + 3000));
