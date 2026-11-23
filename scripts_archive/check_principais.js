const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('id="principais-produtos-section"');
console.log(html.slice(sIdx, sIdx + 2000));
