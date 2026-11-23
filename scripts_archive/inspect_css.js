const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('.produtos-layout-list');
console.log('--- CSS .produtos-layout-list ---');
if (sIdx !== -1) {
  console.log(html.slice(sIdx, sIdx + 1800));
}
