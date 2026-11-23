const https = require('https');
const fs = require('fs');
const path = require('path');

const url = "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/o0gfRAGFGp4fAGGn7LfuejFqUzpRRILAwY0qFl/?a=1988&bti=ODszNWYuMDE6&&bt=976&ft=-Csk_mrMPD12NAJHEn-Ux_LvNY6e3wv25WcAp&mime_type=video_mp4&rc=aGY0NGhmNzdpOztpZTo2ZUBpajtyaHQ5cnR0OjMzODczNEAzLzFfXjVeXl4xNC8wNC5eYSNuYGljMmQ0YHNhLS1kMWBzcw%3D%3D&expire=1792147983&l=2026101418524013CDBFE5A9C61420ED8B&ply_type=2&policy=2&signature=2f1f13a18b0dd043a3b4c45001b6193e&tk=tt_chain_token&btag=e000b8000";

const dest = path.join(__dirname, 'img', 'video-chinelo-juju.mp4');
const file = fs.createWriteStream(dest);

console.log('Downloading video 1 from TikTok CDN...');

const headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Referer': 'https://www.tiktok.com/'
};

https.get(url, { headers }, (res) => {
  console.log('Status code:', res.statusCode);
  if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
    console.log('Following redirect to:', res.headers.location);
    https.get(res.headers.location, { headers }, (r2) => {
      r2.pipe(file);
      file.on('finish', () => {
        file.close();
        console.log('Download complete. File size:', fs.statSync(dest).size);
      });
    });
  } else {
    res.pipe(file);
    file.on('finish', () => {
      file.close();
      console.log('Download complete. File size:', fs.statSync(dest).size);
    });
  }
}).on('error', err => console.error('Download error:', err));
