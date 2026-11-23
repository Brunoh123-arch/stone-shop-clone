const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, '..', 'data', 'produtos');
const files = fs.readdirSync(dir)
  .filter((f) => /^produto-\d+\.json$/.test(f))
  .sort((a, b) => Number(a.match(/\d+/)[0]) - Number(b.match(/\d+/)[0]));

const lines = [
  '// AUTO-GERADO por scripts/gerar-indice-produtos.js',
  '// Lazy require estático garante 100% de empacotamento na Vercel sem estourar memória.',
  'module.exports = {',
  ...files.map((f) => {
    const id = f.match(/\d+/)[0];
    return `  '${id}': () => require('./${f}'),`;
  }),
  '};',
  '',
];

fs.writeFileSync(path.join(dir, 'index.js'), lines.join('\n'), 'utf8');
console.log(`✅ Índice atualizado com ${files.length} produtos em data/produtos/index.js`);
