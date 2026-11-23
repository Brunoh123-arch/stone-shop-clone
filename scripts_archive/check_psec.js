const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const pIdx = html.indexOf('id="principais-produtos-section"');
const pEnd = html.indexOf('id="novos-lancamentos-section"');

console.log('Posição pIdx:', pIdx, 'pEnd:', pEnd);
console.log(html.slice(pIdx - 50, pEnd));
