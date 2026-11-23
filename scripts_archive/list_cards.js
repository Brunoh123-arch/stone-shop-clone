const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const prods = [...html.matchAll(/class="product-card-rec"[^>]*href="([^"]+)"/g)];
console.log('Cards encontrados:', prods.length);
prods.forEach(p => console.log(p[1]));
