const fs = require('fs');
const path = require('path');

const base = 'C:/Users/Dell/Downloads/stone_shop_clone';
const pagesDir = path.join(base, 'pages');
const videosDir = path.join(base, 'videosprodutos');

const files = fs.readdirSync(pagesDir).filter(f => f.startsWith('produto-') && f.endsWith('.html'));
const availableVideos = fs.existsSync(videosDir) ? fs.readdirSync(videosDir) : [];

console.log(`Total de páginas de produto: ${files.length}`);
console.log(`Total de vídeos específicos em videosprodutos/: ${availableVideos.length}`);

const matching = [];
const missing = [];

for (const f of files) {
  const match = f.match(/produto-(\d+)\.html/);
  if (match) {
    const id = match[1];
    const vid = `video-produto-${id}.mp4`;
    if (availableVideos.includes(vid)) {
      matching.push(f);
    } else {
      missing.push(f);
    }
  }
}

console.log(`Produtos COM vídeo dedicado em videosprodutos/: ${matching.length}`);
console.log(`Produtos SEM vídeo dedicado: ${missing.length}`);
console.log('Exemplos de produtos sem vídeo:', missing.slice(0, 10));
