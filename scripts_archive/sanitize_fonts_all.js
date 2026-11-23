const fs = require('fs');
const path = require('path');

const targetStack = '-apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "TikTok Sans", "Plus Jakarta Sans", "Inter", sans-serif';

function sanitizeFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  let changed = false;

  // Replace hardcoded font-family that uses Segoe UI or Roboto
  const regex = /font-family:\s*['"]?-apple-system[^;'"]*['"]?;?/gi;
  if (regex.test(content)) {
    content = content.replace(regex, (match) => {
      // If it's already using Plus Jakarta Sans or TikTok Sans, leave it or normalize
      if (match.includes('TikTok Sans') || match.includes('Plus Jakarta Sans')) {
        return match;
      }
      changed = true;
      return `font-family: var(--font-main, ${targetStack});`;
    });
  }

  // Also replace any standalone font-family: Roboto or Segoe UI
  const regexGeneric = /font-family:\s*['"]?(Segoe UI|Roboto|Helvetica Neue|Arial)['"][^;'"]*;/gi;
  if (regexGeneric.test(content)) {
    content = content.replace(regexGeneric, () => {
      changed = true;
      return `font-family: var(--font-main, ${targetStack});`;
    });
  }

  if (changed) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✅ Atualizado: ${path.relative(process.cwd(), filePath)}`);
  }
}

// Scan pages/
const pagesDir = path.join(__dirname, 'pages');
if (fs.existsSync(pagesDir)) {
  const files = fs.readdirSync(pagesDir).filter(f => f.endsWith('.html'));
  files.forEach(f => sanitizeFile(path.join(pagesDir, f)));
}

// Scan root html
['index.html', 'real.html', 'stone.html', 'admin.html'].forEach(f => {
  const p = path.join(__dirname, f);
  if (fs.existsSync(p)) sanitizeFile(p);
});

console.log('Sanitização de fontes concluída com perfeição!');
