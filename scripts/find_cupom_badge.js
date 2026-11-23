const fs = require('fs');
const path = require('path');

function searchInDir(dir) {
  const files = fs.readdirSync(dir);
  for (const f of files) {
    const full = path.join(dir, f);
    const stat = fs.statSync(full);
    if (stat.isDirectory() && !full.includes('node_modules') && !full.includes('.git')) {
      searchInDir(full);
    } else if (/\.(html|js|css)$/.test(f)) {
      const content = fs.readFileSync(full, 'utf8');
      if (content.includes('product-cupom-badge-row')) {
        console.log(`Found in: ${full}`);
      }
    }
  }
}

searchInDir('.');
