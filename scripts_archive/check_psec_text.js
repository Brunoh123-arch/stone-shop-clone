const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const pStart = html.indexOf('id="principais-produtos-section"');
const pEnd = html.indexOf('id="novos-lancamentos-section"');

console.log(html.slice(pStart, pEnd));
