const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const startIdx = html.indexOf('principais-produtos-section');
console.log('--- principais-produtos-section ---');
if (startIdx !== -1) {
  console.log(html.slice(startIdx, startIdx + 1500));
} else {
  console.log('Não encontrado id principais-produtos-section');
}

const navIdx = html.indexOf('nav-tabs');
console.log('--- nav-tabs e arredores ---');
if (navIdx !== -1) {
  console.log(html.slice(navIdx - 50, navIdx + 1200));
}
