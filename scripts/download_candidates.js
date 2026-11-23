const fs = require('fs');
const https = require('https');
const http = require('http');
const { execSync } = require('child_process');
const path = require('path');

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const proto = url.startsWith('https') ? https : http;
    const file = fs.createWriteStream(dest);
    proto.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    }, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return downloadFile(res.headers.location, dest).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) {
        return reject(new Error('Status ' + res.statusCode));
      }
      res.pipe(file);
      file.on('finish', () => { file.close(); resolve(); });
    }).on('error', reject);
  });
}

async function run() {
  const tmpDir = path.join(__dirname, 'temp_images');
  if (!fs.existsSync(tmpDir)) fs.mkdirSync(tmpDir, { recursive: true });

  const bodyModeladorUrls = [
    'https://ae-pic-a1.aliexpress-media.com/kf/Sd48ab5da54a24c0e83a2ab3ad4c97cd4g.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/Sb0008f2b97164fc9860fbde5fb8cb304G.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/S7163c2f938e8473b9bafe57710f215c0P.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/Saf11651e27c9488e81e8a4694c6cabfab.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/S93cd218e91884f7fae32f655f1423769w.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/S1d0b60f50608473f82441becc9aa1c97w.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/S81280d0fce9a48309b44aa9a931c3716L.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/S50881fbc413346358557e8c044d4392fs.jpg'
  ];

  const aspiradorUrls = [
    'https://ae-pic-a1.aliexpress-media.com/kf/S05b949cd1ef9462d926b73bccabd748c5.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/Sf9e5aa30c50c44ba90d36dc83f71d0abu.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/Sf3dcfc6615bd4198b333fafd7f5a4c63L.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/S56fe21402403424db0f2492aaec7c0c9H.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/Sc9a91e0670134a678165177b69cd966fo.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/S97cfb49686184b9ba8f9ba26338e6a32Q.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/S303080edf726433aa71d60d863bcdb86v.jpg',
    'https://ae-pic-a1.aliexpress-media.com/kf/S61bc83e8ed4d422c8459b8540309652cf.jpg'
  ];

  console.log('Downloading body modelador images...');
  for (let i = 0; i < bodyModeladorUrls.length; i++) {
    const dest = path.join(tmpDir, `body_${i + 1}.jpg`);
    try {
      await downloadFile(bodyModeladorUrls[i], dest);
      console.log(`Saved body_${i + 1}.jpg`);
    } catch (e) {
      console.error(`Failed body_${i + 1}:`, e.message);
    }
  }

  console.log('Downloading aspirador images...');
  for (let i = 0; i < aspiradorUrls.length; i++) {
    const dest = path.join(tmpDir, `asp_${i + 1}.jpg`);
    try {
      await downloadFile(aspiradorUrls[i], dest);
      console.log(`Saved asp_${i + 1}.jpg`);
    } catch (e) {
      console.error(`Failed asp_${i + 1}:`, e.message);
    }
  }
}

run();
