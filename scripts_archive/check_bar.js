const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const barIdx = html.indexOf('subfilter-produtos-bar');
if (barIdx !== -1) {
  console.log('--- subfilter-produtos-bar encontrado ---');
  console.log(html.slice(barIdx - 100, barIdx + 800));
} else {
  console.log('subfilter-produtos-bar NÃO encontrado no HTML!');
}
