const fs = require('fs');
const path = require('path');

// 1. CORRIGIR pages/produto-104.html
const p104Path = path.join(__dirname, 'pages', 'produto-104.html');
let p104 = fs.readFileSync(p104Path, 'utf8');

// Extrair descrição
const descRegex = /<!-- DESCRIÇÃO DO PRODUTO -->[\s\S]*?<div class="description-section">[\s\S]*?<\/div>\s*<\/div>/;
const descMatch = p104.match(descRegex);

if (descMatch) {
  const descBlock = descMatch[0];
  // Remove descrição de onde está
  p104 = p104.replace(descRegex, '');

  // Inserir descrição DEPOIS de avaliações (antes de <!-- PRODUTOS RELACIONADOS --> ou <div class="related-section">)
  const relatedAnchor = '<!-- PRODUTOS RELACIONADOS -->';
  if (p104.includes(relatedAnchor)) {
    p104 = p104.replace(relatedAnchor, descBlock + '\n\n      ' + relatedAnchor);
  } else {
    p104 = p104.replace('<div class="related-section">', descBlock + '\n\n      <div class="related-section">');
  }

  // Garantir que creators-section fique ANTES de avaliações
  const creatorsRegex = /<!-- VÍDEOS DE CRIADORES OFICIAL TIKTOK SHOP -->[\s\S]*?<div id="creators-section" class="creators-section"><\/div>/;
  const creatorsMatch = p104.match(creatorsRegex);
  if (creatorsMatch) {
    const creatorsBlock = creatorsMatch[0];
    p104 = p104.replace(creatorsRegex, '');
    
    // Inserir antes de <!-- AVALIAÇÕES -->
    const revAnchor = '<!-- AVALIAÇÕES -->';
    if (p104.includes(revAnchor)) {
      p104 = p104.replace(revAnchor, creatorsBlock + '\n\n      ' + revAnchor);
    }
  }

  fs.writeFileSync(p104Path, p104, 'utf8');
  console.log('✅ produto-104.html corrigido: Vídeos de criadores -> Avaliações -> Descrição -> Relacionados');

  // Sincronizar com ds/
  const ds104 = path.join('C:', 'Users', 'Dell', 'Downloads', 'ds', 'produto-chinelo-tiktok.html');
  if (fs.existsSync(ds104)) {
    fs.writeFileSync(ds104, p104, 'utf8');
    console.log('✅ ds/produto-chinelo-tiktok.html sincronizado!');
  }
} else {
  console.error('❌ Não encontrou bloco de descrição em produto-104.html');
}

// 2. VERIFICAR SE HÁ OUTRAS PÁGINAS COM DESCRIÇÃO ANTES DE AVALIAÇÃO
const pagesDir = path.join(__dirname, 'pages');
const allPages = fs.readdirSync(pagesDir).filter(f => f.startsWith('produto-') && f.endsWith('.html'));

let fixedOthers = 0;
allPages.forEach(file => {
  if (file === 'produto-104.html') return;
  const filePath = path.join(pagesDir, file);
  let html = fs.readFileSync(filePath, 'utf8');

  const dIdx = html.indexOf('class="description-section"');
  const rIdx = html.indexOf('class="reviews-section"');

  if (dIdx !== -1 && rIdx !== -1 && dIdx < rIdx) {
    // Descrição está antes da avaliação, vamos reordenar
    const dMatch = html.match(/(?:<!-- Descrição[^>]*-->\s*)?<div[^>]*class="[^"]*description-section[^"]*"[^>]*>[\s\S]*?<\/div>\s*<\/div>/i);
    if (dMatch) {
      const dBlock = dMatch[0];
      html = html.replace(dBlock, '');
      const relAnchor = html.includes('class="related-section"') ? '<div class="related-section"' : '</body>';
      html = html.replace(relAnchor, dBlock + '\n\n      ' + relAnchor);
      fs.writeFileSync(filePath, html, 'utf8');
      fixedOthers++;
    }
  }
});

console.log(`✅ Outras páginas corrigidas: ${fixedOthers}`);
