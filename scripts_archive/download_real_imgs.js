const https = require('https');
const fs = require('fs');

const items = [
  {
    url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/ad55abb03d5c4c37957422c69ecd7d65~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my3&from=3376456192',
    dest: 'img/ranking-top1.webp'
  },
  {
    url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/b294c65a791547c998610fb3a12805e4~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my3&from=3376456192',
    dest: 'img/ranking-top2.webp'
  },
  {
    url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/937eda3788b14961af3dc12028a4c886~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my3&from=3376456192',
    dest: 'img/ranking-top3.webp'
  },
  {
    url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/7467bc2b64a44c34a35c7d38357e6e63~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my3&from=3376456192',
    dest: 'img/ranking-novo.webp'
  }
];

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' } }, (res) => {
      if (res.statusCode === 200) {
        res.pipe(file);
        file.on('finish', () => { file.close(); resolve(true); });
      } else {
        file.close();
        if (fs.existsSync(dest)) fs.unlinkSync(dest);
        reject(new Error(`Status ${res.statusCode}`));
      }
    }).on('error', err => reject(err));
  });
}

(async () => {
  for (const item of items) {
    try {
      await download(item.url, item.dest);
      console.log('✅ Baixado com sucesso:', item.dest);
    } catch (e) {
      console.log('❌ Erro:', item.dest, e.message);
    }
  }
})();
