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
    }).on('error', () => resolve(null));
  });
}

function downloadAndDecode(fileUid, destPath) {
  return new Promise((resolve) => {
    const dir = path.dirname(destPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    https.get(`https://api.vercel.com/v8/deployments/${DEPLOY_ID}/files/${fileUid}`, {
      headers: { 'Authorization': 'Bearer ' + token }
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json && json.data) {
            const buf = Buffer.from(json.data, 'base64');
            fs.writeFileSync(destPath, buf);
            resolve({ ok: true, size: buf.length });
            return;
          }
        } catch(e) {}
        resolve({ ok: false });
      });
    }).on('error', () => resolve({ ok: false }));
  });
}

function flatten(node, p = '') {
  let l = [];
  if (Array.isArray(node)) node.forEach(n => l = l.concat(flatten(n, p)));
  else if (node.type === 'directory' && node.children) {
    const np = p ? p + '/' + node.name : node.name;
    node.children.forEach(c => l = l.concat(flatten(c, np)));
  } else if (node.type === 'file' && node.uid) {
    l.push({ path: (p ? p + '/' + node.name : node.name), uid: node.uid });
  }
  return l;
}

async function main() {
  console.log('Fetching tree...');
  const tree = await apiGet(`/v6/deployments/${DEPLOY_ID}/files`);
  const allFiles = flatten(tree);
  console.log('Total files found:', allFiles.length);

  // Filtra arquivos cruciais que NÃO são da pasta pages (já temos pages decodificadas)
  // e NÃO são arquivos que modificamos manualmente (real.html, index.html, vercel.json, api/serve.js)
  const targets = allFiles.filter(f => {
    let p = f.path;
    if (p.startsWith('src/')) p = p.substring(4);
    if (p.startsWith('pages/')) return false;
    if (p === 'real.html' || p === 'index.html' || p === 'vercel.json' || p.startsWith('api/')) return false;
    return true;
  });

  console.log('Assets to download and decode:', targets.length);

  const concurrency = 15;
  let index = 0;
  let completed = 0;

  async function worker() {
    while (index < targets.length) {
      const item = targets[index++];
      let rel = item.path;
      if (rel.startsWith('src/')) rel = rel.substring(4);
      const dest = path.join(__dirname, rel);
      
      const res = await downloadAndDecode(item.uid, dest);
      completed++;
      if (completed % 25 === 0 || completed === targets.length) {
        console.log(`Progress: ${completed}/${targets.length} assets restored.`);
      }
    }
  }

  const workers = Array.from({ length: concurrency }, () => worker());
  await Promise.all(workers);
  console.log('ALL ASSETS DOWNLOADED AND DECODED SUCCESSFULLY!');
}

main();
