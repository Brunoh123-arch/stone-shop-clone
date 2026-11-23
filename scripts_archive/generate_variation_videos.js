const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const dir = 'C:/Users/Dell/Downloads/stone_shop_clone/img';

const tasks = [
  {
    img: 'foto-pe-caramelo.webp',
    video: 'video-chinelo-caramelo-pe.mp4',
    poster: 'poster-chinelo-caramelo-pe.jpg',
    // Zoom in suave de 1.0 para 1.15
    filter: "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0008,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=180:s=540x960:fps=30"
  },
  {
    img: 'foto-pe-branco.webp',
    video: 'video-chinelo-branco-pe.mp4',
    poster: 'poster-chinelo-branco-pe.jpg',
    // Pan vertical suave
    filter: "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih*0.3':d=180:s=540x960:fps=30"
  },
  {
    img: 'foto-caixa-unboxing.webp',
    video: 'video-chinelo-unboxing.mp4',
    poster: 'poster-chinelo-unboxing.jpg',
    // Zoom in no produto na caixa
    filter: "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0009,1.18)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=180:s=540x960:fps=30"
  },
  {
    img: 'foto-preta-oficial.webp',
    video: 'video-chinelo-preto.mp4',
    poster: 'poster-chinelo-preto.jpg',
    // Zoom in no modelo preto
    filter: "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0007,1.14)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=180:s=540x960:fps=30"
  },
  {
    img: 'foto-mao-caramelo.webp',
    video: 'video-chinelo-caramelo-mao.mp4',
    poster: 'poster-chinelo-caramelo-mao.jpg',
    // Zoom in no strass na mão
    filter: "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0008,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=180:s=540x960:fps=30"
  }
];

for (const t of tasks) {
  const imgPath = path.join(dir, t.img);
  const vidPath = path.join(dir, t.video);
  const posterPath = path.join(dir, t.poster);

  console.log(`Gerando ${t.video}...`);
  const cmd = `ffmpeg -y -loop 1 -i "${imgPath}" -vf "${t.filter}" -c:v libx264 -t 6 -pix_fmt yuv420p "${vidPath}"`;
  execSync(cmd, { stdio: 'inherit' });

  // Extrai o poster exatamente do frame 0
  const cmdPoster = `ffmpeg -y -ss 00:00:00 -i "${vidPath}" -vframes 1 -update 1 "${posterPath}"`;
  execSync(cmdPoster, { stdio: 'inherit' });

  console.log(`✅ ${t.video} e ${t.poster} gerados com sucesso!`);
}
console.log('Todos os vídeos de variações reais foram gerados com perfeição!');
