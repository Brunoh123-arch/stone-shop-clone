const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const tIdx = html.indexOf('Recomendado para você');
console.log(html.slice(tIdx - 700, tIdx));
