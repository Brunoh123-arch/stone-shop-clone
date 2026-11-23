const fs = require('fs');
const path = require('path');
const https = require('https');

const imgs = [
  'img/share-arrow.png',
  'logo.png',
  'esteirafotos/esteiraprimeirafoto.PNG',
  'imagemscooterpreta/D_NQ_NP_2X_712059-MLA99509048862_112025-F.webp',
  'img/portugal/7.png'
];

async function download(rel) {
  return new Promise(resolve => {
    const full = path.join(__dirname, rel);
    fs.mkdirSync(path.dirname(full), { recursive: true });
    const f = fs.createWriteStream(full);
    https.get('https://stoneshopclone.vercel.app/' + rel, res => {
      if (res.statusCode === 200) {
        res.pipe(f);
        f.on('finish', () => {
          f.close();
          console.log('Saved', rel, fs.statSync(full).size, 'bytes');
          resolve();
        });
      } else {
        f.close();
        console.log('Missing/Status', rel, res.statusCode);
        resolve();
      }
    });
  });
}

(async () => {
  for (const i of imgs) await download(i);
  console.log('IMGS DOWNLOAD CHECK COMPLETE!');
})();
