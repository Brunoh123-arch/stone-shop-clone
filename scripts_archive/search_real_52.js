const fs = require('fs');

const real = fs.readFileSync('real.html', 'utf8');

const matches = [];
const lines = real.split('\n');
lines.forEach((l, i) => {
  if (l.includes('52') || l.includes('produto-') || l.includes('/pages/')) {
    matches.push({ line: i, text: l.trim().slice(0, 150) });
  }
});

console.log('Matches in real.html:', matches.length);
matches.slice(0, 40).forEach(m => console.log(`${m.line}: ${m.text}`));
