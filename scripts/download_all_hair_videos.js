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

async function processVideo(tiktokUrl, videoDest, posterDest) {
  try {
    console.log(`Buscando no TikWM: ${tiktokUrl}`);
    const data = await fetchTikwm(tiktokUrl);
    if (!data.play) throw new Error('Sem play URL');
    console.log(`Baixando MP4 para: ${videoDest}`);
    await downloadStream(data.play, videoDest);
    console.log(`Gerando poster via FFmpeg: ${posterDest}`);
    execSync(`ffmpeg -y -ss 00:00:00.2 -i "${videoDest}" -vframes 1 -q:v 2 "${posterDest}"`, { stdio: 'ignore' });
    console.log(`[OK] Video e poster prontos: ${path.basename(videoDest)}`);
    return {
      title: data.title || '',
      author: data.author ? (data.author.nickname || data.author.unique_id) : 'Criador',
      handle: data.author ? `@${data.author.unique_id}` : '@criador',
      avatar: data.author ? data.author.avatar : ''
    };
  } catch (err) {
    console.error(`[ERRO] Falha ao processar ${tiktokUrl}:`, err.message);
    return null;
  }
}

async function main() {
  const vidDir = path.join(__dirname, '..', 'videosprodutos');
  const postersDir = path.join(vidDir, 'posters');
  if (!fs.existsSync(postersDir)) fs.mkdirSync(postersDir, { recursive: true });

  const escovaLinks = [
    'https://www.tiktok.com/@dailykarenm/video/7691738826082995474',
    'https://www.tiktok.com/@danielefogassa/video/7507727376885747000',
    'https://www.tiktok.com/@dicascomjaque/video/7636122455630777608',
    'https://www.tiktok.com/@marcellaromero/video/7478484251223149879'
  ];

  const curlerLinks = [
    'https://www.tiktok.com/@gabimodestoo/video/7692967645297118471',
    'https://www.tiktok.com/@achadinhos.daluah/video/7572945674036088071',
    'https://www.tiktok.com/@yasmin.aoliveira/video/7514383110021090616',
    'https://www.tiktok.com/@samara_fontele/video/7513689241570905349'
  ];

  console.log('--- 1. PROCESSANDO VÍDEOS ESCOVA 5 EM 1 (108) ---');
  const escovaMetas = [];
  for (let i = 0; i < escovaLinks.length; i++) {
    const suffix = i === 0 ? '' : `-criadora${i+1}`;
    const vidPath = path.join(vidDir, `video-produto-108${suffix}.mp4`);
    const posPath = path.join(postersDir, `poster-produto-108${suffix}.jpg`);
    const meta = await processVideo(escovaLinks[i], vidPath, posPath);
    if (meta) escovaMetas.push(meta);
  }

  console.log('\n--- 2. PROCESSANDO VÍDEOS MODELADOR DE CACHOS (109) ---');
  const curlerMetas = [];
  for (let i = 0; i < curlerLinks.length; i++) {
    const suffix = i === 0 ? '' : `-criadora${i+1}`;
    const vidPath = path.join(vidDir, `video-produto-109${suffix}.mp4`);
    const posPath = path.join(postersDir, `poster-produto-109${suffix}.jpg`);
    const meta = await processVideo(curlerLinks[i], vidPath, posPath);
    if (meta) curlerMetas.push(meta);
  }

  fs.writeFileSync(path.join(__dirname, 'video_metas_108_109.json'), JSON.stringify({
    escova: escovaMetas,
    curler: curlerMetas
  }, null, 2), 'utf-8');

  console.log('\n✅ TODOS OS VÍDEOS REAIS E POSTERS SINCRONIZADOS COM SUCESSO!');
}

main();
