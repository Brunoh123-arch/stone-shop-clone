const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const recStart = html.indexOf('id="produtos-recomendados-section"');
// Procurar onde fecham as divs de produtos-recomendados-section
// Vamos ver os scripts no final do body
const bodyEnd = html.indexOf('</body>');
console.log('Caracteres antes de </body>:');
console.log(html.slice(bodyEnd - 800, bodyEnd));
