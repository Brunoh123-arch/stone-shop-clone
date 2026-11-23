const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('.produtos-layout-list {');
if (sIdx !== -1) {
  console.log(html.slice(sIdx - 50, sIdx + 1500));
} else {
  console.log('Não achou .produtos-layout-list {');
  // procurar onde aparece .produtos-layout-list
  let pos = 0;
  while ((pos = html.indexOf('produtos-layout-list', pos)) !== -1) {
    console.log('Match at ' + pos + ':\n' + html.slice(pos - 20, pos + 200));
    pos += 20;
  }
}
