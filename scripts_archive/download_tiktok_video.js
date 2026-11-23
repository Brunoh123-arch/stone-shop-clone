const https = require('https');
const fs = require('fs');
const path = require('path');

const videoUrl = 'https://v16m-default.tiktokcdn.com/01d33b346519f245cecab0d9b92ffc66/6acf9d7b/video/tos/alisg/tos-alisg-v-f466fc-sg/o4dQfECVX7pDrEc9GLicBi1CFB7BlgvQcIfjOQ/?a=0&bti=PDM8QDI2M2A%3D&&bt=1013&ft=cApXJCz7ThWH.fJSLGZmo0P&mime_type=video_mp4&rc=PDVkNDc3ZTZoNTs8ZjllOkBpampqa3U5cmR5OjMzODRmNEAuMy5eMC8xNS8xLmMxYTBgYSNpcGdmMmRzY19hLS1kLy1zcw%3D%3D&vvpl=1&l=202610141719041A7FC14FDDDF22009A82&btag=e00078000';

const dest = path.join(__dirname, 'img', 'video-chinelo-oficial.mp4');
console.log('Downloading to:', dest);

const file = fs.createWriteStream(dest);

https.get(videoUrl, {
  headers: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://shop.tiktok.com/'
  }
}, (res) => {
  console.log('Status code:', res.statusCode);
  if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
    console.log('Redirecting to:', res.headers.location);
    https.get(res.headers.location, (redirectRes) => {
      redirectRes.pipe(file);
      file.on('finish', () => {
        file.close();
        console.log('Download completed via redirect. File size:', fs.statSync(dest).size);
      });
    });
  } else {
    res.pipe(file);
    file.on('finish', () => {
      file.close();
      console.log('Download completed. File size:', fs.statSync(dest).size);
    });
  }
}).on('error', (err) => {
  console.error('Error:', err);
});
