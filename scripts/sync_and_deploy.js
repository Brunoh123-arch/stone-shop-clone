const fs = require('fs');
const path = require('path');

const ts = Date.now();
console.log('New cache buster timestamp:', ts);

function processDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (['node_modules', '.git', '.vercel', 'scripts'].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      processDir(full);
    } else if (entry.name.endsWith('.html')) {
      let html = fs.readFileSync(full, 'utf8');
      let changed = false;

      // Update style.css
      if (html.includes('style.css')) {
        html = html.replace(/style\.css(\?v=[^"'\s>]+)?/g, `style.css?v=${ts}`);
        changed = true;
      }

      // Update app.js
      if (html.includes('app.js')) {
        html = html.replace(/app\.js(\?v=[^"'\s>]+)?/g, `app.js?v=${ts}`);
        changed = true;
      }

      // Update videos-criadores.js
      if (html.includes('videos-criadores.js')) {
        html = html.replace(/videos-criadores\.js(\?v=[^"'\s>]+)?/g, `videos-criadores.js?v=${ts}`);
        changed = true;
      }

      if (changed) {
        fs.writeFileSync(full, html, 'utf8');
      }
    }
  }
}

processDir('pages');
processDir('.');

// Sync api/stone_content.js, real.html, stone.html
if (fs.existsSync('index.html')) {
  const idx = fs.readFileSync('index.html', 'utf8');
  if (fs.existsSync('api/stone_content.js')) {
    fs.writeFileSync('api/stone_content.js', 'module.exports = ' + JSON.stringify(idx) + ';', 'utf8');
  }
  if (fs.existsSync('real.html')) fs.writeFileSync('real.html', idx, 'utf8');
  if (fs.existsSync('stone.html')) fs.writeFileSync('stone.html', idx, 'utf8');
}

console.log('Syncing to stone_shop_clone...');

const srcDir = 'c:\\\\Users\\\\Dell\\\\Downloads\\\\ds';
const destDir = 'c:\\\\Users\\\\Dell\\\\Downloads\\\\stone_shop_clone';

function copyRecursive(src, dest) {
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    if (['node_modules', '.git', '.vercel', 'scripts'].includes(entry.name)) continue;
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyRecursive(srcPath, destPath);
    } else {
      let shouldCopy = true;
      if (fs.existsSync(destPath)) {
        const srcStat = fs.statSync(srcPath);
        const destStat = fs.statSync(destPath);
        if (srcStat.mtimeMs <= destStat.mtimeMs && srcStat.size === destStat.size) {
          shouldCopy = false;
        }
      }
      if (shouldCopy) {
        fs.copyFileSync(srcPath, destPath);
      }
    }
  }
}

copyRecursive(srcDir, destDir);
console.log('Sync to stone_shop_clone complete!');
