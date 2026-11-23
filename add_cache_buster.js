const fs = require('fs');
const path = require('path');

const version = process.argv[2] || `v_${Date.now()}`;
console.log(`Aplicando cache buster: ${version}`);

const dir = path.join(__dirname, 'pages');
if (fs.existsSync(dir)) {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
  let count = 0;
  for (const f of files) {
    const p = path.join(dir, f);
    let content = fs.readFileSync(p, 'utf-8');
    if (content.includes('videos-criadores.js')) {
      content = content.replace(/videos-criadores\.js(?:\?[^"]*)?/g, `videos-criadores.js?v=${version}`);
      fs.writeFileSync(p, content, 'utf-8');
      count++;
    }
  }
  console.log(`✅ Cache buster (${version}) atualizado em ${count} páginas.`);
}
