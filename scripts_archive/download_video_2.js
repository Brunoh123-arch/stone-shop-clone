const https = require('https');
const fs = require('fs');
const path = require('path');

const videoUrl = 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/ogIacGQAovAFaEUhjjjayfflIPD7DCDI5geU26/?a=1988&bti=ODszNWYuMDE6&&bt=1128&ft=I~da4oKyD12NvYC6ezIxRvJjHlBF-UjNSfopiX&mime_type=video_mp4&rc=cnF8b2hsc2d3SkBwaHIxaDFybndmNmRkZzRmN2U2NWQ7ZjlkZkBpamdvbnM5cmtuPDMzODczNEBjRl5Nc3FePmJKYSNvYF90aHFmOiMzY2ExYjBhXjExMl5gMzY1YSMzbWlhMmRrNHJhLS1kMTFzcw%3D%3D&expire=1792144527&l=2026101417551518D204D98A8EAB1E6D14&ply_type=2&policy=2&signature=22c7ce5d0d3141dea21b0a11a91417e6&tk=tt_chain_token&btag=e000b0000';
const coverUrl = 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/oE7DP8DsFBaGfh6eLjkaAC5I2yaQQoEfAUUlME~tplv-tiktokx-origin.image?dr=14575&x-expires=1792141200&x-signature=q%2BDttg72IX2BcDdpaLim3lL1mmM%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2';

const base = 'C:/Users/Dell/Downloads/stone_shop_clone';
const videoDest = path.join(base, 'img', 'video-chinelo-tiktok-2.mp4');
const coverDest = path.join(base, 'img', 'poster-chinelo-tiktok-2.jpg');

function download(url, dest, cb) {
  const file = fs.createWriteStream(dest);
  https.get(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Referer': 'https://www.tiktok.com/'
    }
  }, (res) => {
    if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
      https.get(res.headers.location, (r2) => {
        r2.pipe(file);
        file.on('finish', () => { file.close(); cb(); });
      });
    } else {
      res.pipe(file);
      file.on('finish', () => { file.close(); cb(); });
    }
  }).on('error', (err) => console.error(err));
}

download(videoUrl, videoDest, () => {
  console.log('Video 2 baixado com sucesso! Tamanho:', fs.statSync(videoDest).size);
});

download(coverUrl, coverDest, () => {
  console.log('Cover 2 baixado com sucesso! Tamanho:', fs.statSync(coverDest).size);
});
