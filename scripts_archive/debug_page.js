const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const matches = [...html.matchAll(/coupons-container/g)];
console.log('Ocorrências de coupons-container:', matches.length);
matches.forEach((m, idx) => {
  console.log(`\n=== Ocorrência ${idx + 1} (pos ${m.index}) ===`);
  console.log(html.slice(m.index - 50, m.index + 1200));
});
