const fs = require('fs');
const https = require('https');
const path = require('path');
const { execSync } = require('child_process');

function fetchTikwm(url) {
  return new Promise((resolve, reject) => {
    https.get(`https://www.tikwm.com/api/?url=${encodeURIComponent(url)}`, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.code === 0 && json.data) {
            resolve(json.data);
          } else {
            reject(new Error(json.msg || 'Erro TikWM'));
          }
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

function downloadStream(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return downloadStream(res.headers.location, dest).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) return reject(new Error('Status ' + res.statusCode));
      res.pipe(file);
      file.on('finish', () => { file.close(); resolve(); });
    }).on('error', reject);
  });
}

async function test() {
  console.log('Testando download de Gabriel Mattos (Projetor 111)...');
  const d = await fetchTikwm('https://www.tiktok.com/@gabriel.mattoos/video/7704711329843662132');
  console.log('Play URL:', d.play);
  console.log('Author:', d.author ? d.author.unique_id : 'null');
  console.log('Title:', d.title);
  
  const dest = path.join(__dirname, '..', 'videosprodutos', 'video-produto-111.mp4');
  await downloadStream(d.play, dest);
  console.log('Video salvo em:', dest, 'Tamanho:', fs.statSync(dest).size);

  const posterDest = path.join(__dirname, '..', 'videosprodutos', 'posters', 'poster-produto-111.jpg');
  execSync(`ffmpeg -y -ss 00:00:00.2 -i "${dest}" -vframes 1 -q:v 2 "${posterDest}"`);
  console.log('Poster gerado em:', posterDest);
}

test().catch(e => console.error('Erro:', e));
