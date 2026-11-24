const fs = require('fs');
const path = require('path');

const baseDir = path.resolve(__dirname);
const archiveDir = path.join(baseDir, 'scripts_archive');

if (!fs.existsSync(archiveDir)) {
  fs.mkdirSync(archiveDir, { recursive: true });
}

// Arquivos vitais que DEVEM ficar na raiz da Stone Shop
const coreFiles = new Set([
  'index.html',
  'real.html',
  'stone.html',
  'admin.html',
  'painel.html',
  'safe.html',
  'aramis.html',
  'server.js',
  'tracker.js',
  'vercel.json',
  'package.json',
  'package-lock.json',
  '.gitignore',
  '.env.local',
  'setup_ambiente.bat',
  'iniciar_loja.bat',
  'README.md',
  'COMO_USAR_FLUXO_TIKTOK.md',
  'GEMINI.md',
  'logo.png',
  // Scripts do pipeline oficial Stone Shop
  'pipeline_tiktok_shop.js',
  'download_and_extract_tiktok_videos.js',
  'add_cache_buster.js',
  'copy_assets.js',
  'sync_all.js',
  'deploy_to_vercel.js',
  'organize_stone.js' // Este próprio script
]);

const items = fs.readdirSync(baseDir);
let movedCount = 0;

for (const item of items) {
  const itemPath = path.join(baseDir, item);
  const stat = fs.statSync(itemPath);

  if (stat.isFile()) {
    if (!coreFiles.has(item)) {
      const destPath = path.join(archiveDir, item);
      fs.renameSync(itemPath, destPath);
      movedCount++;
    }
  }
}

console.log(`✅ Organização concluída! ${movedCount} arquivos temporários movidos para scripts_archive/`);
