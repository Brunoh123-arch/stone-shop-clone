const fs = require('fs');
const html = fs.readFileSync('C:/Users/Dell/Downloads/stone_shop_clone/pages/resumo.html', 'utf8');
const lines = html.split('\n');
console.log(lines.slice(1210, 1370).join('\n'));
