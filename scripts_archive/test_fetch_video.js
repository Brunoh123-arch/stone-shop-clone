const fs = require('fs');
const path = require('path');

const url = 'https://v16-webapp.tiktok.com/e6a05792ce5b633e054187c56c942b82/6ad1f48f/video/tos/alisg/tos-alisg-pv-0037/599a0a6ea1dd45e1b716f35b81401e02/?a=1988&bti=ODszNWYuMDE6&&bt=2565&ft=IecA0oKyD12NvYC6ezIxRvJjHlBF-UjNSfopiX&mime_type=video_mp4&rc=cnF8b2hsc2d3SkBwaHIxaDFybndmamdvbnM5cmtuPDMzODczNEBpamdvbnM5cmtuPDMzODczNEBjRl5Nc3FePmJKYSNvYF90aHFmOiMzbWlhMmRrNHJhLS1kMTFzYSMzbWlhMmRrNHJhLS1kMTFzcw%3D%3D&l=2026101417551518D204D98A8EAB1E6D14&btag=e00070000';

async function run() {
  console.log('Fetching without range header...');
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.tiktok.com/'
      }
    });
    console.log('Status:', res.status);
    console.log('Headers content-length:', res.headers.get('content-length'));
    console.log('Headers content-type:', res.headers.get('content-type'));
    const buffer = await res.arrayBuffer();
    console.log('Buffer byteLength:', buffer.byteLength);
    if (buffer.byteLength > 10000) {
      const dest = path.join(__dirname, 'img', 'video-chinelo-tiktok-2.mp4');
      fs.writeFileSync(dest, Buffer.from(buffer));
      console.log('Saved to', dest, 'Size:', fs.statSync(dest).size);
    }
  } catch(e) {
    console.error('Fetch error:', e);
  }
}

run();
