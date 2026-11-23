const fs = require('fs');
const path = require('path');
const https = require('https');

const auth = JSON.parse(fs.readFileSync(process.env.APPDATA + '/com.vercel.cli/Data/auth.json', 'utf8'));
const token = auth.token;
const DEPLOY_ID = 'dpl_EPjHPAnJaBKadnPBG2qZ92Xv8Zdp';

function apiGet(urlPath) {
  return new Promise((resolve, reject) => {
    https.get('https://api.vercel.com' + urlPath, {
      headers: { 'Authorization': 'Bearer ' + token }
    }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch(e) {
          resolve(data);
        }
      });
    }).on('error', reject);
  });
}

function downloadBinary(fileUid, destPath) {
  return new Promise((resolve, reject) => {
    const dir = path.dirname(destPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    const file = fs.createWriteStream(destPath);
    https.get(`https://api.vercel.com/v6/deployments/${DEPLOY_ID}/files/${fileUid}`, {
      headers: { 'Authorization': 'Bearer ' + token }
    }, res => {
      if (res.statusCode !== 200) {
        console.error('Failed to download', destPath, res.statusCode);
        file.close();
        return resolve(false);
      }
      res.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve(true);
      });
    }).on('error', err => {
      file.close();
      reject(err);
    });
  });
}

function flattenFiles(node, currentPath = '') {
  let list = [];
  if (Array.isArray(node)) {
    for (const item of node) {
      list = list.concat(flattenFiles(item, currentPath));
    }
  } else if (node.type === 'directory' && node.children) {
    const nextPath = currentPath ? `${currentPath}/${node.name}` : node.name;
    for (const child of node.children) {
      list = list.concat(flattenFiles(child, nextPath));
    }
  } else if (node.type === 'file' && node.uid) {
    const filePath = currentPath ? `${currentPath}/${node.name}` : node.name;
    list.push({ path: filePath, uid: node.uid, name: node.name });
  }
  return list;
}

async function main() {
  console.log('1. Fetching file tree from deployment...');
  const tree = await apiGet(`/v6/deployments/${DEPLOY_ID}/files`);
  const allFiles = flattenFiles(tree);
  console.log(`Found ${allFiles.length} total files in deployment.`);

  // Filtramos os arquivos que não sejam vídeos pesados de 50MB a menos que necessário
  // Prioridade absoluta: css, js, json, imagens
  const staticFiles = allFiles.filter(f => !f.path.startsWith('out/api'));

  console.log(`Found ${staticFiles.length} static assets to restore.`);

  let downloaded = 0;
  for (const f of staticFiles) {
    // Limpa prefixos como "src/" se houver
    let relativeDest = f.path;
    if (relativeDest.startsWith('src/')) {
      relativeDest = relativeDest.substring(4);
    }

    // Não sobrescrever o admin.html ou real.html se já modificamos
    if (relativeDest === 'admin.html' || relativeDest === 'real.html' || relativeDest === 'vercel.json') {
      console.log('Skipping modified file:', relativeDest);
      continue;
    }

    const targetDest = path.join(__dirname, relativeDest);
    process.stdout.write(`Downloading: ${relativeDest}... `);
    const ok = await downloadBinary(f.uid, targetDest);
    if (ok) {
      downloaded++;
      console.log('OK');
    }
  }

  console.log(`\nDONE! Restored ${downloaded} assets successfully.`);
}

main().catch(console.error);
