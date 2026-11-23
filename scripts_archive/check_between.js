const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const pStart = html.indexOf('id="principais-produtos-section"');
const rStart = html.indexOf('id="recommended-grid"');

console.log('--- ENTRE PRINCIPAIS E RECOMMENDED GRID ---');
console.log(html.slice(pStart, rStart + 100));
