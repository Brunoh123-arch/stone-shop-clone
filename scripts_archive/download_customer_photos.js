const https = require('https');
const fs = require('fs');
const path = require('path');

const base = 'C:/Users/Dell/Downloads/stone_shop_clone/img';

const photos = [
  { name: 'foto-pe-caramelo.webp', url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/79bf69882ab7434bb96ad7521ba36aa3~tplv-aphluv4xwc-crop-webp:600:600.webp' },
  { name: 'foto-mao-caramelo.webp', url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/3d4600770ace47a6a81fa34b7f8d70c1~tplv-aphluv4xwc-crop-webp:600:600.webp' },
  { name: 'foto-pe-branco.webp', url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/5fd57c49dd214ea78ba2ecadcb597049~tplv-aphluv4xwc-crop-webp:600:600.webp' },
  { name: 'foto-caixa-unboxing.webp', url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/15612787b5b243ad82b29474b3bb26cc~tplv-aphluv4xwc-crop-webp:600:600.webp' },
  { name: 'foto-preta-oficial.webp', url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/7467bc2b64a44c34a35c7d38357e6e63~tplv-aphluv4xwc-resize-webp:800:800.webp' },
  { name: 'foto-sol-branco.webp', url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/8667cc75644a42699b19811c462b10a6~tplv-aphluv4xwc-crop-webp:600:600.webp' }
];

let pending = photos.length;
for (const p of photos) {
  const dest = path.join(base, p.name);
  const file = fs.createWriteStream(dest);
  https.get(p.url, (res) => {
    res.pipe(file);
    file.on('finish', () => {
      file.close();
      console.log(`Baixado: ${p.name} (${fs.statSync(dest).size} bytes)`);
      if (--pending === 0) console.log('Todas as fotos baixadas!');
    });
  }).on('error', err => console.error(err));
}
