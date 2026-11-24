const fs = require('fs');
const path = require('path');

const dirs = [
  'C:/Users/Dell/Downloads/stone_shop_clone',
  'C:/Users/Dell/Downloads/ds'
];

dirs.forEach(baseDir => {
  if (!fs.existsSync(baseDir)) return;
  console.log('--- Processando diretório:', baseDir, '---');

  // 1. Arquivos na raiz
  ['index.html', 'real.html', 'stone.html'].forEach(f => {
    const p = path.join(baseDir, f);
    if (fs.existsSync(p)) {
      let content = fs.readFileSync(p, 'utf8');
      if (!content.includes('anti-clone-guard.js')) {
        content = content.replace(/<head>/i, '<head>\n<script src="/js/anti-clone-guard.js?v=20261020"></script>');
        fs.writeFileSync(p, content, 'utf8');
        console.log('✅ Injetado em:', f);
      } else {
        console.log('ℹ️ Já continha em:', f);
      }
    }
  });

  // 2. Arquivos em pages/
  const pagesDir = path.join(baseDir, 'pages');
  if (fs.existsSync(pagesDir)) {
    const files = fs.readdirSync(pagesDir).filter(f => f.endsWith('.html'));
    let count = 0;
    files.forEach(f => {
      const p = path.join(pagesDir, f);
      let content = fs.readFileSync(p, 'utf8');
      if (!content.includes('anti-clone-guard.js')) {
        content = content.replace(/<head>/i, '<head>\n<script src="/js/anti-clone-guard.js?v=20261020"></script>');
        fs.writeFileSync(p, content, 'utf8');
        count++;
      }
    });
    console.log(`✅ Injetado em ${count}/${files.length} páginas em pages/`);
  }
});
