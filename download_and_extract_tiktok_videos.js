const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const args = process.argv.slice(2);

const defaultBatch = [
  {
    id: 'kethellen1',
    tiktokUrl: 'https://www.tiktok.com/@kethellenshop/video/7669129001549532424',
    name: 'video-chinelo-kethellen1.mp4',
    poster: 'poster-chinelo-kethellen1.jpg',
    author: 'Kethellen Jade',
    desc: 'Meninas, calçando nos pés pra vocês verem como fica perfeita! Super macia e o strass brilha muito! 👡✨'
  },
  {
    id: 'kethellen2',
    tiktokUrl: 'https://www.tiktok.com/@kethellenshop/video/7685922250947693842',
    name: 'video-chinelo-kethellen2.mp4',
    poster: 'poster-chinelo-kethellen2.jpg',
    author: 'Kethellen Jade',
    desc: 'Comprei primeiro a caramelo e fiquei tão apaixonada que comprei a preta, a branca e a nude também! Perfeitas! 💖'
  },
  {
    id: 'juju',
    tiktokUrl: 'https://www.tiktok.com/@jujuvariedades_/video/7638006622249323783',
    name: 'video-chinelo-juju.mp4',
    poster: 'poster-chinelo-juju.jpg',
    author: 'Juju Variedades',
    desc: 'Olha os detalhes desse chinelo de strass com nó luxo! Acabamento impecável e conforto absurdo! 💎'
  }
];

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
      });
    }).on('error', reject);
  });
}

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    const req = https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        https.get(res.headers.location, (r2) => {
          r2.pipe(file);
          file.on('finish', () => { file.close(); resolve(); });
        }).on('error', reject);
      } else if (res.statusCode === 200) {
        res.pipe(file);
        file.on('finish', () => { file.close(); resolve(); });
      } else {
        reject(new Error(`Falha no download (HTTP ${res.statusCode})`));
      }
    });
    req.on('error', reject);
  });
}

async function processVideo(tiktokUrl, videoFilename, posterFilename) {
  const baseImg = path.join(__dirname, 'img');
  if (!fs.existsSync(baseImg)) fs.mkdirSync(baseImg, { recursive: true });

  console.log(`\n🔍 Consultando API TikWM para: ${tiktokUrl}`);
  const apiUrl = `https://www.tikwm.com/api/?url=${encodeURIComponent(tiktokUrl)}`;
  const data = await fetchJson(apiUrl);

  if (data.code === 0 && data.data && data.data.play) {
    const playUrl = data.data.play;
    const author = data.data.author?.nickname || 'Criador TikTok';
    const title = data.data.title || 'Vídeo sem título';
    console.log(`👤 Autor: ${author}`);
    console.log(`📝 Título: ${title}`);

    const destVideo = path.join(baseImg, videoFilename);
    console.log(`⬇️ Baixando vídeo sem marca d'água para: ${videoFilename}...`);
    await downloadFile(playUrl, destVideo);

    const size = fs.statSync(destVideo).size;
    console.log(`✅ Vídeo baixado com sucesso! Tamanho: ${(size / 1024 / 1024).toFixed(2)} MB`);

    const destPoster = path.join(baseImg, posterFilename);
    console.log(`🖼️ Extraindo frame inicial exato (00:00:00.2) para poster: ${posterFilename}...`);
    try {
      execSync(`ffmpeg -y -ss 00:00:00.2 -i "${destVideo}" -vframes 1 -q:v 2 "${destPoster}"`, { stdio: 'pipe' });
      console.log(`✅ Poster ${posterFilename} sincronizado com perfeição cirúrgica!`);
    } catch (e) {
      console.warn(`⚠️ Aviso FFmpeg: certifique-se de que o ffmpeg está instalado no PATH.`);
    }

    return {
      author,
      title,
      video: videoFilename,
      poster: posterFilename
    };
  } else {
    throw new Error(`Erro ao obter vídeo no TikWM: ${data.msg || 'URL inválida ou indisponível'}`);
  }
}

async function run() {
  console.log('===========================================================');
  console.log('🎬 TIKTOK VIDEO EXTRACTOR & POSTER SYNC (BRUNO CTO)');
  console.log('===========================================================');

  if (args.length > 0) {
    const tiktokUrl = args[0];
    const timestamp = Date.now();
    const videoName = args[1] || `video-tiktok-${timestamp}.mp4`;
    const posterName = args[2] || `poster-tiktok-${timestamp}.jpg`;

    await processVideo(tiktokUrl, videoName, posterName);
    console.log('\n🎉 Extração concluída!');
  } else {
    console.log('Modo lote padrão: baixando e verificando vídeos cadastrados...\n');
    for (const item of defaultBatch) {
      await processVideo(item.tiktokUrl, item.name, item.poster);
    }
    console.log('\n🎉 Todos os vídeos do lote padrão foram baixados e sincronizados!');
  }
}

run().catch(err => {
  console.error('\n❌ Erro durante a execução:', err.message);
  process.exit(1);
});
