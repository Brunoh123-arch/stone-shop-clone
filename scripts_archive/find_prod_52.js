const fs = require('fs');

const cat = fs.readFileSync('js/catalogo.js', 'utf8');

// Procurar por 52
const matches = [];
const lines = cat.split('\n');
lines.forEach((l, i) => {
  if (l.includes('52') || l.includes('produto') || l.includes('pages/')) {
    matches.push({ line: i, text: l.trim() });
  }
});

console.log('Matches count:', matches.length);
matches.slice(0, 30).forEach(m => console.log(`${m.line}: ${m.text}`));
