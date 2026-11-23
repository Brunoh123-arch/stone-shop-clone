const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('function switchTab');
console.log(html.slice(sIdx, sIdx + 1200));

// Ver onde termina produtos-recomendados-section
const recIdx = html.indexOf('id="produtos-recomendados-section"');
console.log('--- AO REDOR DE PRODUTOS RECOMENDADOS ---');
console.log(html.slice(recIdx, recIdx + 800));

// Ver o final do arquivo index.html
console.log('--- FINAL DO BODY ---');
console.log(html.slice(html.length - 2000));
