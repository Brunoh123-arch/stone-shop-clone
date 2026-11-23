const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('id="subfilter-produtos-bar"');
console.log('Posição de subfilter-produtos-bar:', sIdx);
console.log(html.slice(sIdx - 150, sIdx + 400));
