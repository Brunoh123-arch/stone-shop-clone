const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const matches = [...html.matchAll(/\.produtos-layout-list[\s\S]*?\{[\s\S]*?\}/g)];
console.log('Total de regras .produtos-layout-list:', matches.length);
matches.forEach((m, i) => {
  console.log(`[Regra ${i + 1}]:\n${m[0]}\n`);
});
