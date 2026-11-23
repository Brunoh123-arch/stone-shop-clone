const fs = require('fs');
const html = fs.readFileSync('real.html', 'utf8');

const matches = [];
const regex = /<a class="product-card-rec[^"]*"[^>]*href="pages\/produto-(\d+)\.html"[^>]*>([\s\S]*?)<\/a>/gi;
let m;
while ((m = regex.exec(html)) !== null) {
  const id = m[1];
  const block = m[2];
  const title = block.match(/<h3 class="product-name">([\s\S]*?)<\/h3>/)?.[1]?.trim() || '';
  const current = block.match(/<span class="current-price">([\s\S]*?)<\/span>/)?.[1]?.replace(/<[^>]+>/g, '').trim() || '';
  const old = block.match(/<span class="old-price">([\s\S]*?)<\/span>/)?.[1]?.trim() || '';
  matches.push({ id, title: title.slice(0, 40), current, old });
}

console.log('TOTAL PRODUCTS IN HOME:', matches.length);
matches.forEach(p => console.log(`#${p.id} [${p.current}] (${p.old}) ${p.title}`));
