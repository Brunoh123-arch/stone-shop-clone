const fs = require('fs');
const path = require('path');

console.log('===========================================================');
console.log('🔄 SINCRONIZADOR STONE SHOP & WORKSPACE DS (BRUNO CTO)');
console.log('===========================================================');

const baseDir = __dirname;
const dsDir = 'C:\\Users\\Dell\\Downloads\\ds';
const cacheBuster = '1111_v22_tiktokaddress';

// 1. Atualizar cache buster de style.css em real.html
let realHtml = fs.readFileSync(path.join(baseDir, 'real.html'), 'utf8');
realHtml = realHtml.replace(/href=["']css\/style\.css(\?v=[^"']*)?["']/g, `href="css/style.css?v=${cacheBuster}"`);
realHtml = realHtml.replace(/src=["']js\/app\.js(\?v=[^"']*)?["']/g, `src="js/app.js?v=${cacheBuster}"`);
fs.writeFileSync(path.join(baseDir, 'real.html'), realHtml, 'utf8');
fs.writeFileSync(path.join(baseDir, 'index.html'), realHtml, 'utf8');
fs.writeFileSync(path.join(baseDir, 'stone.html'), realHtml, 'utf8');
console.log('✅ index.html, real.html e stone.html sincronizados como LOJA OFICIAL');

// 2. api/stone_content.js e api/fake_content.js
const fakeHtml = fs.readFileSync(path.join(baseDir, 'fake.html'), 'utf8');
const apiDir = path.join(baseDir, 'api');
if (!fs.existsSync(apiDir)) fs.mkdirSync(apiDir, { recursive: true });
fs.writeFileSync(path.join(apiDir, 'stone_content.js'), `module.exports = ${JSON.stringify(realHtml)};\n`, 'utf8');
fs.writeFileSync(path.join(apiDir, 'fake_content.js'), `module.exports = ${JSON.stringify(fakeHtml)};\n`, 'utf8');
console.log('✅ api/stone_content.js e api/fake_content.js sincronizados');

// 3. Atualizar cache buster de style.css em pages/*.html
const pagesDir = path.join(baseDir, 'pages');
if (fs.existsSync(pagesDir)) {
  const pages = fs.readdirSync(pagesDir).filter(p => p.endsWith('.html'));
  pages.forEach(p => {
    const filePath = path.join(pagesDir, p);
    let content = fs.readFileSync(filePath, 'utf8');
    if (content.includes('app.js')) {
      content = content.replace(/src=["']\.\.\/js\/app\.js(\?v=[^"']*)?["']/g, `src="../js/app.js?v=${cacheBuster}"`);
    }
    if (content.includes('style.css')) {
      content = content.replace(/href=["']\.\.\/css\/style\.css(\?v=[^"']*)?["']/g, `href="../css/style.css?v=${cacheBuster}"`);
    }
    if (!content.includes('decalque-oferta.jpg') && content.includes('</head>')) {
      const preloads = '  <link rel="preload" as="image" href="../decalque/decalque-oferta.jpg?v=1111" fetchpriority="high">\n  <link rel="preload" as="image" href="../img/banner-1111-modal.webp" fetchpriority="high">\n</head>';
      content = content.replace('</head>', preloads);
    }
    fs.writeFileSync(filePath, content, 'utf8');
  });
  console.log(`✅ Cache buster aplicado em ${pages.length} páginas de produtos`);
}

// 4. Sincronização com o Workspace DS (se existir)
if (fs.existsSync(dsDir)) {
  fs.writeFileSync(path.join(dsDir, 'index.html'), realHtml, 'utf8');
  fs.writeFileSync(path.join(dsDir, 'real.html'), realHtml, 'utf8');
  fs.writeFileSync(path.join(dsDir, 'stone.html'), realHtml, 'utf8');
  fs.writeFileSync(path.join(dsDir, 'fake.html'), fakeHtml, 'utf8');

  const dsApi = path.join(dsDir, 'api');
  if (!fs.existsSync(dsApi)) fs.mkdirSync(dsApi, { recursive: true });
  fs.writeFileSync(path.join(dsApi, 'stone_content.js'), `module.exports = ${JSON.stringify(realHtml)};\n`, 'utf8');
  fs.writeFileSync(path.join(dsApi, 'fake_content.js'), `module.exports = ${JSON.stringify(fakeHtml)};\n`, 'utf8');

  // Sincronizar páginas de produto
  const dsPages = path.join(dsDir, 'pages');
  if (!fs.existsSync(dsPages)) fs.mkdirSync(dsPages, { recursive: true });

  const allProductPages = fs.readdirSync(path.join(baseDir, 'pages')).filter(p => p.endsWith('.html'));
  for (const pageName of allProductPages) {
    const srcPage = path.join(baseDir, 'pages', pageName);
    fs.copyFileSync(srcPage, path.join(dsPages, pageName));
  }
  console.log(`✅ ${allProductPages.length} páginas copiadas para ds/pages/`);

  // Scripts centrais
  const dsJs = path.join(dsDir, 'js');
  if (!fs.existsSync(dsJs)) fs.mkdirSync(dsJs, { recursive: true });
  ['anti-clone-guard.js', 'videos-criadores.js', 'catalogo.js', 'app.js', 'roleta-tiktok.js'].forEach(jsFile => {
    const srcJs = path.join(baseDir, 'js', jsFile);
    if (fs.existsSync(srcJs)) {
      fs.copyFileSync(srcJs, path.join(dsJs, jsFile));
      console.log(`✅ js/${jsFile} sincronizado para ds/js/`);
    }
  });

  // CSS e Decalques
  const dsCss = path.join(dsDir, 'css');
  if (!fs.existsSync(dsCss)) fs.mkdirSync(dsCss, { recursive: true });
  const srcCss = path.join(baseDir, 'css', 'style.css');
  if (fs.existsSync(srcCss)) {
    fs.copyFileSync(srcCss, path.join(dsCss, 'style.css'));
    console.log(`✅ css/style.css sincronizado para ds/css/`);
  }

  const dsDecalque = path.join(dsDir, 'decalque');
  if (!fs.existsSync(dsDecalque)) fs.mkdirSync(dsDecalque, { recursive: true });
  ['decalque-oferta.jpg', 'decalque-oferta.png', 'decalque-1111.png', 'banner-1111-modal.png'].forEach(imgFile => {
    const srcImg = path.join(baseDir, 'decalque', imgFile);
    if (fs.existsSync(srcImg)) {
      fs.copyFileSync(srcImg, path.join(dsDecalque, imgFile));
    }
  });
  console.log(`✅ decalque sincronizado para ds/decalque/`);

  const dsImg = path.join(dsDir, 'img');
  if (!fs.existsSync(dsImg)) fs.mkdirSync(dsImg, { recursive: true });
  ['banner-1111-modal.png', 'banner-1111-modal.webp'].forEach(imgFile => {
    const srcImg = path.join(baseDir, 'img', imgFile);
    if (fs.existsSync(srcImg)) {
      fs.copyFileSync(srcImg, path.join(dsImg, imgFile));
    }
  });
  console.log('✅ img sincronizado para ds/img/');
}

console.log('\n🎉 Sincronização finalizada com sucesso!');
