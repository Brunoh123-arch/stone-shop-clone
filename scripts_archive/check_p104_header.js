const fs = require('fs');
const html = fs.readFileSync('pages/produto-104.html', 'utf8');

const sIdx = html.indexOf('<header');
const eIdx = html.indexOf('</header>');
if (sIdx !== -1) {
  console.log(html.slice(sIdx, eIdx + 10));
}
