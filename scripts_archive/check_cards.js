const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const rStart = html.indexOf('id="recommended-grid"');
const rEnd = html.indexOf('<!-- FOOTER', rStart);

const section = html.slice(rStart, rEnd !== -1 ? rEnd : rStart + 15000);

// Contar quantos cards existem
const cards = section.match(/<a class="product-card-rec"[\s\S]*?<\/a>/g) || [];
console.log('Total de cards em recommended-grid:', cards.length);

cards.slice(0, 5).forEach((c, i) => {
  const titleM = c.match(/<h3[\s\S]*?>([\s\S]*?)<\/h3>/i) || c.match(/class="product-name"[\s\S]*?>([\s\S]*?)<\//i);
  const hrefM = c.match(/href="([^"]+)"/i);
  console.log(`Card ${i + 1}:`, {
    href: hrefM ? hrefM[1] : null,
    title: titleM ? titleM[1].trim() : null
  });
});
