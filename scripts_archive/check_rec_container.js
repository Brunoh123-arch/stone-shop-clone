const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const gIdx = html.indexOf('id="recommended-grid"');
console.log(html.slice(gIdx - 400, gIdx + 400));
