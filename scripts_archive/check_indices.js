const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('principais-produtos-section');
const eIdx = html.indexOf('recommended-grid');
console.log('sIdx:', sIdx, 'eIdx:', eIdx);
if (sIdx !== -1) {
  console.log(html.slice(sIdx, sIdx + 1000));
}
