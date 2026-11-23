const fs = require('fs');

const html = fs.readFileSync('real.html', 'utf8');

const matches = html.match(/src=["']([^"']+)["']/gi) || [];
const imgs = matches.map(m => m.match(/src=["']([^"']+)["']/)[1]);
const localImgs = imgs.filter(u => !u.startsWith('http') && !u.startsWith('//') && !u.startsWith('data:') && !u.endsWith('.js'));

console.log('LOCAL IMGS:', [...new Set(localImgs)]);
