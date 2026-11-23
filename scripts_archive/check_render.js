const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Procurar se catalogo.js é chamado em index.html
console.log('Chama catalogo.js?', html.includes('catalogo.js'));

// Procurar por renderProducts ou similar
const scripts = html.match(/<script[\s\S]*?<\/script>/gi) || [];
console.log('Total de scripts:', scripts.length);
scripts.forEach((s, idx) => {
  if (s.includes('recommended-grid') || s.includes('catalogo') || s.includes('render')) {
    console.log(`Script ${idx} menciona grid/catalogo:`);
    console.log(s.slice(0, 500));
  }
});
