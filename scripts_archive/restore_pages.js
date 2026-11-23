const fs = require('fs');
const path = require('path');
const https = require('https');

const auth = JSON.parse(fs.readFileSync(process.env.APPDATA + '/com.vercel.cli/Data/auth.json', 'utf8'));
const token = auth.token;
const DEPLOY_ID = 'dpl_EPjHPAnJaBKadnPBG2qZ92Xv8Zdp';

function apiGet(urlPath) {
  return new Promise(resolve => {
    https.get('https://api.vercel.com' + urlPath, {
      headers: { 'Authorization': 'Bearer ' + token }
    }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try { resolve(JSON.parse(d)); } catch(e) { resolve(null); }
      });
    });
  });
}

function downloadFile(fileUid, destPath) {
  return new Promise((resolve) => {
    const dir = path.dirname(destPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    const f = fs.createWriteStream(destPath);
    https.get(`https://api.vercel.com/v8/deployments/${DEPLOY_ID}/files/${fileUid}`, {
      headers: { 'Authorization': 'Bearer ' + token }
    }, res => {
      if (res.statusCode === 200) {
        res.pipe(f);
        f.on('finish', () => {
          f.close();
          resolve(true);
        });
      } else {
        f.close();
        resolve(false);
      }
    }).on('error', () => {
      f.close();
      resolve(false);
    });
  });
}

function flatten(node, p = '') {
  let l = [];
  if (Array.isArray(node)) node.forEach(n => l = l.concat(flatten(n, p)));
  else if (node.type === 'directory' && node.children) {
    const np = p ? p + '/' + node.name : node.name;
    node.children.forEach(c => l = l.concat(flatten(c, np)));
  } else if (node.type === 'file' && node.uid) {
    l.push({ path: (p ? p + '/' + node.name : node.name), uid: node.uid, name: node.name });
  }
  return l;
}

async function run() {
  console.log('Fetching files list...');
  const tree = await apiGet('/v6/deployments/' + DEPLOY_ID + '/files');
  const all = flatten(tree);
  
  // Filtrar arquivos de pages/
  const pageFiles = all.filter(f => f.path.includes('pages/'));
  console.log(`Found ${pageFiles.length} files in pages/`);

  for (const f of pageFiles) {
    // Normalizar destino: se começa com "src/pages/...", salva em "pages/..."
    let rel = f.path;
    if (rel.startsWith('src/')) rel = rel.substring(4);
    const dest = path.join(__dirname, rel);
    
    process.stdout.write(`Downloading ${rel}... `);
    const ok = await downloadFile(f.uid, dest);
    console.log(ok ? 'OK' : 'FAILED');
  }

  console.log('ALL PAGES RESTORED!');
}

run();
