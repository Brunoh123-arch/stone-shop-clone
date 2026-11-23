const https = require('https');
const fs = require('fs');
const path = require('path');

const url = "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o4IaxqAFiP6in1BEA3uHAEB2gYXVQqB2nii7V/?a=1988&bti=ODszNWYuMDE6&&bt=1036&ft=-Csk_mrMPD12NNv6En-Ux~tFPY6e3wv25DcAp&mime_type=video_mp4&rc=NTplNTo0PGZmOWc3ZjlmZkBpanF0d3E5cmR4ZDMzODczNEBhMzAtNWE1NWMxLmI2LTQyYSMwMWleMmQ0LmhhLS1kMTFzcw%3D%3D&expire=1792148400&l=202610141859148A06299C879FF61E0E5C&ply_type=2&policy=2&signature=0d8b1a6807aee7df6156a6fc325446da&tk=tt_chain_token&btag=e00048000";

const dest = path.join(__dirname, 'img', 'video-chinelo-kethellen-stream.mp4');
const file = fs.createWriteStream(dest);

console.log('Downloading Kethellen stream...');

const req = https.get(url, {
  headers: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.tiktok.com/',
    'Range': 'bytes=0-'
  }
}, (res) => {
  console.log('Status:', res.statusCode);
  if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
    https.get(res.headers.location, (r2) => {
      r2.pipe(file);
      file.on('finish', () => {
        file.close();
        console.log('Done redirect! Size:', fs.statSync(dest).size);
      });
    });
  } else {
    res.pipe(file);
    file.on('finish', () => {
      file.close();
      console.log('Done! Size:', fs.statSync(dest).size);
    });
  }
});
req.on('error', e => console.error(e));
