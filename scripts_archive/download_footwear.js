const https = require('https');
const fs = require('fs');

// As 4 fotos oficiais da galeria do chinelo do TikTok Shop
const galleryImgs = [
  // Foto 1: Chinelo caramelo / glitter
  {
    url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/d1225a0ba7b9492683401953c5c4bf02~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my3&from=3376456192',
    dest: 'img/ranking-top1.webp'
  },
  // Foto 2: Chinelo branco
  {
    url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/cbc47b24541346dcb1a7af5fa1fa17cc~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my3&from=3376456192',
    dest: 'img/ranking-top2.webp'
  },
  // Foto 3: Chinelo branco strass luxo na mão
  {
    url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/937eda3788b14961af3dc12028a4c886~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my3&from=3376456192',
    dest: 'img/ranking-top3.webp'
  },
  // Foto 4: Chinelo preto no pé
  {
    url: 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/53bf5449455446aa903aef80462557b0~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my3&from=3376456192',
    dest: 'img/ranking-novo.webp'
  }
];

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
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
  for (const item of galleryImgs) {
    try {
      await download(item.url, item.dest);
      console.log('✅ Baixado chinelo oficial:', item.dest);
    } catch (e) {
      console.log('❌ Erro:', item.dest, e.message);
    }
  }
})();
