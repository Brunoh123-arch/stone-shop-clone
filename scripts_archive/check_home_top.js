const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('principais-produtos-section');
const eIdx = html.indexOf('recommended-grid');
console.log(html.slice(sIdx, eIdx));
