const fs = require('fs');
const https = require('https');
const path = require('path');
const { execSync } = require('child_process');

const videosToProcess = [
  {
    index: 1,
    url: "https://www.tiktok.com/@raysscalazans/video/7537080199381388600",
    videoFile: "criador-6-1.mp4",
    posterFile: "poster-criador-6-1.jpg",
    defaultName: "Rayssa Calazans",
    defaultUser: "raysscalazans",
    defaultDesc: "Gente, testei minha bike ergométrica em casa e me surpreendeu demais! Pedal super suave e silencioso! 🚴‍♀️✨"
  },
  {
    index: 2,
    url: "https://www.tiktok.com/@amoreamoras/video/7557401811271814412",
    videoFile: "criador-6-2.mp4",
    posterFile: "poster-criador-6-2.jpg",
    defaultName: "Evelise Marques",
    defaultUser: "amoreamoras",
    defaultDesc: "Tudo que você precisa saber antes de comprar a bike ergométrica de spinning! Tira todas as dúvidas reais de treino! 🔥💪"
  },
  {
    index: 3,
    url: "https://www.tiktok.com/@paula.raysa/video/7646535609242176776",
    videoFile: "criador-6-3.mp4",
    posterFile: "poster-criador-6-3.jpg",
    defaultName: "Paula | Tech & Fitness",
    defaultUser: "paula.raysa",
    defaultDesc: "Unboxing e montagem completa da bike spinning! Estrutura de aço reforçado, monitor digital e 10 níveis de resistência! 📦🚴‍♂️"
  }
];

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

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
  const vidDir = path.join(__dirname, '..', 'videosprodutos');
  const imgDir = path.join(__dirname, '..', 'img');
  const avatarDir = path.join(imgDir, 'creators-auto');
  if (!fs.existsSync(vidDir)) fs.mkdirSync(vidDir, { recursive: true });
  if (!fs.existsSync(imgDir)) fs.mkdirSync(imgDir, { recursive: true });
  if (!fs.existsSync(avatarDir)) fs.mkdirSync(avatarDir, { recursive: true });

  const results = [];

  for (const item of videosToProcess) {
    console.log(`\n========================================`);
    console.log(`[${item.index}/3] Processando: ${item.url}`);
    
    let data;
    try {
      data = await fetchTikwm(item.url);
    } catch (e) {
      console.warn(`TikWM error: ${e.message}, aguardando 2s para retry...`);
      await sleep(2000);
      data = await fetchTikwm(item.url);
    }

    const videoDest = path.join(vidDir, item.videoFile);
    console.log(`Baixando vídeo limpo para: ${videoDest}`);
    await downloadStream(data.play, videoDest);
    console.log(`Vídeo baixado (${fs.statSync(videoDest).size} bytes)`);

    const posterDest = path.join(imgDir, item.posterFile);
    console.log(`Gerando poster no frame 00:00:00.2: ${posterDest}`);
    execSync(`ffmpeg -y -ss 00:00:00.2 -i "${videoDest}" -vframes 1 -q:v 2 "${posterDest}"`, { stdio: 'ignore' });
    console.log(`Poster gerado (${fs.statSync(posterDest).size} bytes)`);

    // Baixar avatar
    let avatarRel = '';
    if (data.author && data.author.avatar) {
      const avatarFileName = `avatar-criador-6-${item.index}.jpg`;
      const avatarDest = path.join(avatarDir, avatarFileName);
      try {
        await downloadStream(data.author.avatar, avatarDest);
        avatarRel = `../img/creators-auto/${avatarFileName}`;
      } catch (err) {
        console.warn('Erro ao baixar avatar:', err.message);
        avatarRel = `../img/creators-tech/creator-${item.index}.jpg`;
      }
    } else {
      avatarRel = `../img/creators-tech/creator-${item.index}.jpg`;
    }

    const resultObj = {
      name: (data.author && data.author.nickname) ? data.author.nickname : item.defaultName,
      username: (data.author && data.author.unique_id) ? data.author.unique_id : item.defaultUser,
      avatar: avatarRel,
      poster: `../img/${item.posterFile}`,
      video: `../videosprodutos/${item.videoFile}`,
      startTime: 0.2,
      desc: item.defaultDesc
    };

    results.push(resultObj);
    console.log('Criador processado com sucesso:', resultObj);
    await sleep(2000);
  }

  const jsonDest = path.join(__dirname, 'product_6_creators.json');
  fs.writeFileSync(jsonDest, JSON.stringify(results, null, 2), 'utf-8');
  console.log(`\nSalvo JSON final em: ${jsonDest}`);
}

main().catch(err => {
  console.error('ERRO FATAL:', err);
  process.exit(1);
});
