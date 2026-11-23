const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('action-y2k-container');
console.log('--- CSS action-y2k-container ---');
if (sIdx !== -1) {
  console.log(html.slice(sIdx - 50, sIdx + 1500));
}
