const fs = require('fs');

function checkFile(name) {
  if (!fs.existsSync(name)) return;
  const content = fs.readFileSync(name, 'utf8');
  console.log('=== FILE: ' + name + ' (len: ' + content.length + ') ===');
  
  // Procurar seções chave
  const hasNovos = content.includes('Novos lançamentos') || content.includes('novos lançamentos') || content.includes('novos-lancamentos');
  const hasVerMais = content.includes('Ver mais');
  const hasBottomBar = content.includes('home-bottom-bar') || content.includes('bottom-bar');
  const hasHeaderIcons = content.includes('bi-cart') || content.includes('cart') || content.includes('share');
  
  console.log({
    hasNovos,
    hasVerMais,
    hasBottomBar,
    hasHeaderIcons
  });
}

const files = ['index.html', 'real.html', 'stone.html', 'safe.html', 'admin.html', 'original_principais.html'];
files.forEach(checkFile);
