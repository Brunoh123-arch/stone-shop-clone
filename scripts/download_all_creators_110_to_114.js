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
    console.log(`[TikWM] Buscando: ${tiktokUrl}`);
    const data = await fetchTikwm(tiktokUrl);
    if (!data.play) throw new Error('Sem play URL');
    console.log(`[Download] Baixando video para: ${path.basename(videoDest)}`);
    await downloadStream(data.play, videoDest);
    console.log(`[FFmpeg] Extraindo frame 00:00:00.2 para: ${path.basename(posterDest)}`);
    execSync(`ffmpeg -y -ss 00:00:00.2 -i "${videoDest}" -vframes 1 -q:v 2 "${posterDest}"`, { stdio: 'ignore' });
    
    // Baixar avatar do criador se houver
    let avatarPath = '';
    if (data.author && data.author.avatar) {
      const avatarFilename = `avatar-${data.author.unique_id || 'creator'}.jpg`;
      avatarPath = path.join(__dirname, '..', 'img', 'creators-auto', avatarFilename);
      try {
        await downloadStream(data.author.avatar, avatarPath);
      } catch (e) {
        avatarPath = '';
      }
    }

    return {
      title: data.title || '',
      name: data.author ? (data.author.nickname || data.author.unique_id) : 'Criador',
      user: data.author ? data.author.unique_id : 'criador',
      avatar: avatarPath ? `../img/creators-auto/${path.basename(avatarPath)}` : '../img/reviews-avatars/review-user-1.jpg',
      likes: data.digg_count || 14200,
      comments: data.comment_count || 184,
      shares: data.share_count || 320,
      videoFile: path.basename(videoDest),
      posterFile: path.basename(posterDest)
    };
  } catch (err) {
    console.error(`[FALHA] ${tiktokUrl}:`, err.message);
    return null;
  }
}

const PRODUCTS_MAP = {
  111: [
    'https://www.tiktok.com/@gabriel.mattoos/video/7704711329843662132',
    'https://www.tiktok.com/@maya.shopcreator/video/7687006150843223317',
    'https://www.tiktok.com/@terapiaepapel/video/7563349300609174802',
    'https://www.tiktok.com/@mariannegimenes/video/7564548016607153429'
  ],
  112: [
    'https://www.tiktok.com/@alicinhaebianca/video/7681421989856349447',
    'https://www.tiktok.com/@lojadoguza/video/7594612712857013522',
    'https://www.tiktok.com/@meninogesse/video/7660974734796180756'
  ],
  110: [
    'https://www.tiktok.com/@entrecafeesonhos/video/7662455446317321493',
    'https://www.tiktok.com/@radardedescontosml/video/7695930560375426325',
    'https://www.tiktok.com/@clayton_achadinhos/video/7699256658870029589'
  ],
  113: [
    'https://www.tiktok.com/@lojamimers/video/7672884933446192402',
    'https://www.tiktok.com/@familinhadegato/video/7652882761245625607'
  ],
  114: [
    'https://www.tiktok.com/@alucinatus.games/video/7691706535130565895',
    'https://www.tiktok.com/@eletro.retro.game/video/7688784436460227860'
  ]
};

async function main() {
  const vidDir = path.join(__dirname, '..', 'videosprodutos');
  const postersDir = path.join(vidDir, 'posters');
  if (!fs.existsSync(postersDir)) fs.mkdirSync(postersDir, { recursive: true });

  const allMetas = {};

  for (const [prodId, urls] of Object.entries(PRODUCTS_MAP)) {
    console.log(`\n========================================`);
    console.log(`PROCESSANDO CRIADORES DO PRODUTO ${prodId}`);
    console.log(`========================================`);
    allMetas[prodId] = [];

    for (let i = 0; i < urls.length; i++) {
      const suffix = i === 0 ? '' : `-criadora${i+1}`;
      const vidPath = path.join(vidDir, `video-produto-${prodId}${suffix}.mp4`);
      const posPath = path.join(postersDir, `poster-produto-${prodId}${suffix}.jpg`);

      const meta = await processVideo(urls[i], vidPath, posPath);
      if (meta) {
        allMetas[prodId].push(meta);
      }
    }
  }

  const outJson = path.join(__dirname, 'creators_metas_110_to_114.json');
  fs.writeFileSync(outJson, JSON.stringify(allMetas, null, 2), 'utf-8');
  console.log(`\n[SUCESSO] Metas salvas em ${outJson}`);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
