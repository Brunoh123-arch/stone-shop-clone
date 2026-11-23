const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

console.log(html.slice(25204, 25204 + 2000));
