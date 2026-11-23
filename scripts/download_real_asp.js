const fs = require('fs');
const https = require('https');
const path = require('path');

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, res => {
      if (res.statusCode !== 200) return reject(new Error('Status ' + res.statusCode));
      res.pipe(file);
      file.on('finish', () => { file.close(); resolve(); });
    }).on('error', reject);
  });
}

async function main() {
  const dir = path.join(__dirname, 'temp_asp');
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  const urls = [
    'https://ae-pic-a1.aliexpress-media.com/kf/S2d5fa008515b46d287ccd4a094480b2al.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/Sf024a589df5d445a84b88f4a2c275650R.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/S11f9a5cc23324b7ab1fc7614cd409be52.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/Sb1b8f764f9dc4ca69d6b5331ea55f65fe.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/S7044c6c4e41b4c2e9b28949da1fe6571V.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/Sd92bcba81ca44ca18cef0a6f6e5d0ca2V.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/Se0f2482634d249ff8810830ca500941di.jpg'
  ];

  for (let i = 0; i < urls.length; i++) {
    const dest = path.join(dir, `real_asp_${i + 1}.jpg`);
    await download(urls[i], dest);
    console.log('Saved real_asp_' + (i + 1));
  }
}

main();
