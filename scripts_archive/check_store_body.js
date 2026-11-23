const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('<div class="store-section">');
console.log('sIdx:', sIdx);
console.log(html.slice(sIdx, sIdx + 2000));
