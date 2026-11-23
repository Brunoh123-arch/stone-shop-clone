const https = require('https');

const videoUrl = 'https://www.tiktok.com/@kethellenshop/video/7669129001549532424';
const apiUrl = `https://www.tikwm.com/api/?url=${encodeURIComponent(videoUrl)}`;

https.get(apiUrl, (res) => {
  let body = '';
  res.on('data', c => body += c);
  res.on('end', () => {
    try {
      const data = JSON.parse(body);
      console.log('Code:', data.code);
      if (data.data) {
        console.log('Title:', data.data.title);
        console.log('Author:', data.data.author ? data.data.author.nickname : 'N/A');
        console.log('Play URL (no watermark):', data.data.play);
        console.log('Cover:', data.data.cover);
      }
    } catch(e) {
      console.error(e);
    }
  });
}).on('error', console.error);
