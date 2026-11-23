const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('<div class="store-section">');
const eIdx = html.indexOf('id="recommended-grid"');

console.log('Distância em chars:', eIdx - sIdx);
console.log(html.slice(sIdx, sIdx + 2000));
console.log('--- MEIO ---');
console.log(html.slice(sIdx + 2000, eIdx + 100));
