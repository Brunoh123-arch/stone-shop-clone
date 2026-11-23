const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const eIdx = html.indexOf('<!-- NAV TABS -->');
console.log(html.slice(eIdx, eIdx + 1500));
