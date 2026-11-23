const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const matches = [...html.matchAll(/class="[^"]*divider-home-rec[^"]*"/g)];
console.log('Ocorrências de divider-home-rec:', matches.length);
matches.forEach((m, i) => console.log(i + 1, m.index));
