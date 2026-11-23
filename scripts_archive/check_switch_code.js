const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

console.log(html.slice(496555, 496555 + 2000));
