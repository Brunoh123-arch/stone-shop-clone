const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

console.log('=== SWITCH TAB FUNCTION ===');
const sIdx = html.indexOf('function switchTab');
if (sIdx !== -1) {
  console.log(html.slice(sIdx, sIdx + 1500));
}

console.log('\n=== CATEGORIAS SECTION ===');
const catIdx = html.indexOf('id="categorias-section"');
if (catIdx !== -1) {
  console.log(html.slice(catIdx - 20, catIdx + 1500));
}

console.log('\n=== BUSCA POR NOVOS LANÇAMENTOS NOS ARQUIVOS ANTIGOS ===');
const files = ['original_principais.html', 'safe.html', 'loja.html', 'real.html', 'painel.html'];
for (const f of files) {
  if (fs.existsSync(f)) {
    const c = fs.readFileSync(f, 'utf8');
    if (c.includes('Novos lançamentos') || c.includes('novos lançamentos') || c.includes('novos lancamentos')) {
      console.log(`Encontrado em ${f}!`);
    }
  }
}
