const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('id="principais-produtos-section"');
const eIdx = html.indexOf('id="recommended-grid"', sIdx);
console.log('sIdx:', sIdx, 'eIdx:', eIdx);
if (sIdx !== -1 && eIdx !== -1) {
  console.log(html.slice(sIdx, eIdx + 100));
}
