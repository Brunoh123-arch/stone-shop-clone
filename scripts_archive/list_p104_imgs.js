const fs = require('fs');
const html = fs.readFileSync('pages/produto-104.html', 'utf8');

const imgs = [...html.matchAll(/src="([^"]+)"/g)].map(m => m[1]);
console.log('Total de imagens em p104:', imgs.length);
console.log(imgs.slice(0, 10));
