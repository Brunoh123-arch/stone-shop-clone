const fs = require('fs');

function countCardsInFile(f) {
  if (!fs.existsSync(f)) return;
  const content = fs.readFileSync(f, 'utf8');
  const count = (content.match(/class="product-card-rec"/g) || []).length;
  console.log(`${f}: ${count} cards com class product-card-rec (tamanho total do arquivo: ${content.length})`);
}

const files = ['index.html', 'real.html', 'stone.html', 'safe.html', 'admin.html', 'painel.html'];
files.forEach(countCardsInFile);

// Verificar arquivos em ds/
const dsFiles = ['../ds/index.html', '../ds/loja.html', '../ds/real.html', '../ds/stone.html'];
dsFiles.forEach(countCardsInFile);
