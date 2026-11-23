const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const matches = [...html.matchAll(/function switchTab/g)];
console.log('Total de ocorrências de function switchTab:', matches.length);
matches.forEach((m, i) => console.log(i + 1, m.index));
