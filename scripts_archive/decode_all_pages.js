const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'pages');

function processDir(d) {
  const entries = fs.readdirSync(d, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(d, e.name);
    if (e.isDirectory()) {
      processDir(full);
    } else {
      try {
        const raw = fs.readFileSync(full);
        // Tenta ver se é JSON com "data"
        const text = raw.toString('utf8');
        if (text.startsWith('{"data":"') || text.startsWith('{\n  "data":')) {
          const parsed = JSON.parse(text);
          if (parsed.data) {
            const buf = Buffer.from(parsed.data, 'base64');
            fs.writeFileSync(full, buf);
            console.log('Decoded base64:', full, buf.length, 'bytes');
          }
        }
      } catch(err) {
        // Ignora se não for json
      }
    }
  }
}

processDir(dir);
console.log('ALL FILES IN pages/ DECODED TO NATIVE CONTENT!');
