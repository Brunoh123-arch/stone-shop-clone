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

async function main() {
  const postersDir = path.join(__dirname, '..', 'videosprodutos', 'posters');
  if (!fs.existsSync(postersDir)) fs.mkdirSync(postersDir, { recursive: true });

  console.log('1. Fetching Mini Aspirador video...');
  const aspData = await fetchTikwm('https://www.tiktok.com/@tikshoop7/video/7537545517534858552');
  const aspVideoPath = path.join(__dirname, '..', 'videosprodutos', 'video-produto-107.mp4');
  console.log('Downloading aspirador video from:', aspData.play);
  await downloadStream(aspData.play, aspVideoPath);
  console.log('Downloaded video-produto-107.mp4');

  const aspPosterPath = path.join(postersDir, 'poster-produto-107.jpg');
  execSync(`ffmpeg -y -ss 00:00:00.2 -i "${aspVideoPath}" -vframes 1 -q:v 2 "${aspPosterPath}"`, { stdio: 'inherit' });
  console.log('Generated poster-produto-107.jpg');

  console.log('2. Fetching Body Modelador video...');
  const bodyData = await fetchTikwm('https://www.tiktok.com/@ttitashop/video/7672393833333738773');
  const bodyVideoPath = path.join(__dirname, '..', 'videosprodutos', 'video-produto-106.mp4');
  console.log('Downloading body modelador video from:', bodyData.play);
  await downloadStream(bodyData.play, bodyVideoPath);
  console.log('Downloaded video-produto-106.mp4');

  const bodyPosterPath = path.join(postersDir, 'poster-produto-106.jpg');
  execSync(`ffmpeg -y -ss 00:00:00.2 -i "${bodyVideoPath}" -vframes 1 -q:v 2 "${bodyPosterPath}"`, { stdio: 'inherit' });
  console.log('Generated poster-produto-106.jpg');

  console.log('ALL VIDEOS AND POSTERS READY!');
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
