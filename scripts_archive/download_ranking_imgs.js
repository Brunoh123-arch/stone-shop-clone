const https = require('https');
const fs = require('fs');
const path = require('path');

const imgs = [
  {
    url: 'https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/ef0c4879de7a44f4955799ce3a17e13e~tplv-o3syd03w52-resize-jpeg:800:800.jpeg',
    dest: 'img/ranking-top1.jpg'
  },
  {
    url: 'https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/66d3a87ec7e8424b94f06ddfd71bc391~tplv-o3syd03w52-resize-jpeg:800:800.jpeg',
    dest: 'img/ranking-top2.jpg'
  },
  {
    url: 'https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/218cb51a37c34fca92f1683be83c4b9a~tplv-o3syd03w52-resize-jpeg:800:800.jpeg',
    dest: 'img/ranking-top3.jpg'
  },
  {
    url: 'https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/5135cb7416344aa18e950ceee9ff304d~tplv-o3syd03w52-resize-jpeg:800:800.jpeg',
    dest: 'img/ranking-novo.jpg'
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
        fs.unlinkSync(dest);
        reject(new Error(`Status ${res.statusCode}`));
      }
    }).on('error', err => reject(err));
  });
}

(async () => {
  for (const item of imgs) {
    try {
      await download(item.url, item.dest);
      console.log('✅ Baixou:', item.dest);
    } catch (e) {
      console.log('❌ Erro ao baixar', item.url, e.message);
    }
  }
})();
